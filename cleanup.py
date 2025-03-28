import os
import sys
import platform
import winreg

def remove_from_startup():
    if platform.system() == "Windows":
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
            winreg.DeleteValue(key, "AsteroidGame")
            winreg.CloseKey(key)
            print("Removed from Windows startup.")
        except Exception as e:
            print(f"Error removing from startup: {e}")
    elif platform.system() == "Linux":
        startup_path = os.path.expanduser("~/.config/autostart/asteroid_game.desktop")
        if os.path.exists(startup_path):
            os.remove(startup_path)
            print("Removed from Linux autostart.")
        else:
            print("No autostart entry found.")

if __name__ == "__main__":
    remove_from_startup()
    input("Press Enter to exit...")  # Optional: keep console open to see result
    