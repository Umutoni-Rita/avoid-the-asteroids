# cleanup.py
import os
import platform
import winreg

def remove_from_startup():
    if platform.system() == "Windows":
        try:
            key = winreg.OpenKey(winreg.HKCU, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
            winreg.DeleteValue(key, "AsteroidGame")
            winreg.CloseKey(key)
            print("Removed from Windows startup.")
        except:
            print("No startup entry found.")
    elif platform.system() == "Linux":
        startup_path = os.path.expanduser("~/.config/autostart/asteroid_game.desktop")
        if os.path.exists(startup_path):
            os.remove(startup_path)
            print("Removed from Linux autostart.")
        else:
            print("No autostart entry found.")

if __name__ == "__main__":
    remove_from_startup()