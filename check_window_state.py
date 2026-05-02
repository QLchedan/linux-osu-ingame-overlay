import subprocess
import time
import os

def check_window_state(debug=False):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dbus_script = os.path.join(script_dir, "src/dbus_communication.js")
    load_cmd = ["qdbus", "org.kde.KWin", "/Scripting", "loadScript", dbus_script]
    
    try:
        result = subprocess.run(load_cmd, capture_output=True, text=True, check=True)
        num = result.stdout.replace('\n', '')
        
        start_time = time.time()
        subprocess.run(["qdbus", "org.kde.KWin", "/Scripting/Script" + num, "run"], check=True)
        
        log_cmd = ["journalctl", "_COMM=kwin_wayland", "-o", "cat", f"--since=@{int(start_time)}"]
        logs = subprocess.run(log_cmd, capture_output=True, text=True).stdout.removeprefix('\n').removesuffix('\n').split('\n')
        # logs is a list following this structure: [is_window_active, x_pos, y_pos, width, height, screen_width, screen_height]
        if debug:
            print(logs)
        return logs
    except Exception as e:
        return -1
    
# Return Code -1: error occurs during the window reading process

if __name__ == "__main__":
    print("Debug Mode")
    r = check_window_state(debug=True)
