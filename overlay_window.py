import os
import gi
import cairo
gi.require_version('Gtk', '4.0')
gi.require_version('WebKit', '6.0')
gi.require_version('Gtk4LayerShell', '1.0')
from gi.repository import Gtk, Gdk, WebKit, GLib
from gi.repository import Gtk4LayerShell

from check_window_state import check_window_state

class GameOverlay(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="com.qlcd.tosuoverlay")
        self.connect('activate', self.on_activate)
        self.visible = True

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
        info = check_window_state()
        try:
            self.screen_width = int(info[5])
            self.screen_height = int(info[6])
            self.webview.set_size_request(int(info[5]), int(info[6]))
            self.win.set_default_size(int(info[5]), int(info[6]))
        except Exception as e:
            print(e)
            self.webview.set_size_request(1920, 1080)
            self.win.set_default_size(1920, 1080)
        self.fixed.put(self.webview, 0, 0)
        self.win.set_child(self.webview)

        # setting up layer shell
        Gtk4LayerShell.init_for_window(self.win)
        Gtk4LayerShell.set_layer(self.win, Gtk4LayerShell.Layer.OVERLAY)
        
        # ensure the window cannot be interacted
        Gtk4LayerShell.set_keyboard_mode(self.win, Gtk4LayerShell.KeyboardMode.NONE)

        self.win.connect('realize', self._on_window_realize)
        GLib.timeout_add(500, self._check_window) # check if the osu window is active
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

    def _check_window(self):
        window_state = check_window_state()
        try:
            if self.visible and window_state[0] == "false":
                self._hide_overlay()
            if not self.visible and window_state[0] == "true":
                self._show_overlay()
            h = self.webview.get_height()
            w = self.webview.get_width()
            allocation = self.webview.get_allocation()
            x = allocation.x
            y = allocation.y
            if w != int(window_state[3]) or h != int(window_state[4]) or x != int(window_state[1]) or y != int(window_state[2]):
                self.fixed.move(self.webview, int(window_state[1]), int(window_state[2]))
                self.webview.set_size_request(int(window_state[3]), int(window_state[4]))
                self.webview.set_zoom_level(min(int(window_state[3]) / self.screen_width, int(window_state[4]) / self.screen_height))
        except Exception as e:
            print(e)
        return True

