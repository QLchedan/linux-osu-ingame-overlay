import overlay_window
from dbus.mainloop.glib import DBusGMainLoop

if __name__ == "__main__":
    DBusGMainLoop(set_as_default=True)
    
    app = overlay_window.GameOverlay()
    app.run()
