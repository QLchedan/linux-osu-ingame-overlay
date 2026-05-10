import os
import sys

if 'LD_PRELOAD' not in os.environ:
    os.environ['LD_PRELOAD'] = '/usr/lib/libgtk4-layer-shell.so'
    os.execvp(sys.argv[0], sys.argv)

from dbus.mainloop.glib import DBusGMainLoop
import overlay_window

print("-------------------------------------------------")
print("osu-ingame-overlay v1.0.2 created by qlchedan 2026.5")
print("Github: https://github.com/QLchedan/linux-osu-ingame-overlay")
print("osu! Profile: https://osu.ppy.sh/users/15522107")
print("Press Ctrl+C to exit.")
print("-------------------------------------------------")

if __name__ == "__main__":
    DBusGMainLoop(set_as_default=True)
    app = overlay_window.GameOverlay()
    app.run()
