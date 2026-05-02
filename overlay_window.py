import os
import gi
import cairo
import time
import subprocess
gi.require_version('Gtk', '4.0')
gi.require_version('WebKit', '6.0')
gi.require_version('Gtk4LayerShell', '1.0')
from gi.repository import Gtk, Gdk, WebKit, GLib
from gi.repository import Gtk4LayerShell
from dbus.service import BusName, Object, signal, method
from dbus import SessionBus

def get_screen_resolution():
    cmd = ['xrandr']
    output = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0].decode('utf-8')
    width = output.split('\n')[0].split(',')[1].split(' ')[2]
    height = output.split('\n')[0].split(',')[1].split(' ')[4]
    return (width, height)

class OverlayService(Object):
    def __init__(self, overlay):
        self.overlay = overlay
        bus_name = BusName('com.qlcd.OverlayService', bus=SessionBus())
        super().__init__(bus_name, '/')

    @method(dbus_interface='com.qlcd.OverlayService.ipc', signature='iiiii')
    def adjust_window(self, is_active, x, y, width, height):
        print(time.time(), is_active, x, y, width, height)
        try:
            GLib.idle_add(self._apply_adjustment, is_active, x, y, width, height)
        except Exception as e:
            print('idle_add failed:', e)

    def _apply_adjustment(self, is_active, x, y, width, height):
        try:
            if is_active == 1:
                self.overlay._show_overlay()
                allocation = self.overlay.webview.get_allocation()
                x_ = allocation.x
                y_ = allocation.y
                h = self.overlay.webview.get_height()
                w = self.overlay.webview.get_width()
                if w != width or h != height or x != x_ or y != y_:
                    self.overlay.fixed.move(self.overlay.webview, x, y)
                    self.overlay.webview.set_size_request(width, height)
                    try:
                        zoom = min(width / self.overlay.screen_width, height / self.overlay.screen_height)
                        self.overlay.webview.set_zoom_level(zoom)
                    except Exception as e:
                        print('set_zoom_level failed:', e)
            else:
                self.overlay._hide_overlay()
        except Exception as e:
            print('apply_adjustment error:', e)
        # return False so the idle callback runs only once
        return False
        


class GameOverlay(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="com.qlcd.tosuoverlay")
        self.connect('activate', self.on_activate)
        self.visible = True
        self.dbus_service = None

    def on_activate(self, app):
        self.win = Gtk.ApplicationWindow(application=app, title="tosuoverlay")
        self.fixed = Gtk.Fixed()
        self.win.set_child(self.fixed)
        self.win.set_decorated(False)
        display = Gdk.Display.get_default()

        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(b"""
            window {
                background-color: transparent;
            }
        """)
        Gtk.StyleContext.add_provider_for_display(
            display,
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        
        # create a webview container
        self.webview = WebKit.WebView()
        self.webview.set_background_color(Gdk.RGBA(0.0, 0.0, 0.0, 0.0))
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src/index.html")
        uri = GLib.filename_to_uri(path, None)
        self.webview.load_uri(uri)
        screen_res = get_screen_resolution()
        try:
            self.screen_width = screen_res[0]
            self.screen_height = screen_res[1]
            self.webview.set_size_request(screen_res[0], screen_res[1])
            self.win.set_default_size(screen_res[0], screen_res[1])
        except Exception as e:
            self.screen_width = 1920
            self.screen_height = 1080
            self.webview.set_size_request(1920, 1080)
            self.win.set_default_size(1920, 1080)
        self.fixed.put(self.webview, 0, 0)
        self.win.set_child(self.webview)

        # setting up layer shell
        Gtk4LayerShell.init_for_window(self.win)
        Gtk4LayerShell.set_layer(self.win, Gtk4LayerShell.Layer.OVERLAY)
        
        # ensure the window cannot be interacted
        Gtk4LayerShell.set_keyboard_mode(self.win, Gtk4LayerShell.KeyboardMode.NONE)
        self.dbus_service = OverlayService(self)
        print("Overlay Service is running...")
        self.win.connect('realize', self._on_window_realize)
        #GLib.timeout_add(500, self._check_window) # check if the osu window is active
        self.win.show()
        self.hold()
        
    def _on_window_realize(self, window):
        surface = window.get_surface()
        if surface is not None:
            try:
                empty_region = cairo.Region()
                surface.set_input_region(empty_region)
            except Exception as e:
                print(e)

    def _hide_overlay(self):
        # hide the overlay
        if self.win:
            self.win.set_visible(False)
            self.visible = False

    def _show_overlay(self):
        # show the overlay
        if self.win:
            if not self.win.get_realized():
                 self.win.show()
            else:
                 self.win.set_visible(True)
            self.visible = True
