import wmi, psutil, re
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from collections import defaultdict

import subprocess

def set_volume(level: int):

    ps_script = f"""
    $wshShell = New-Object -ComObject WScript.Shell
    for ($i=0; $i -lt 50; $i++) {{ $wshShell.SendKeys([char]174) }}  # mute/volume down
    for ($i=0; $i -lt {level // 2}; $i++) {{ $wshShell.SendKeys([char]175) }}  # volume up
    """
    subprocess.run(["powershell", "-Command", ps_script])

PROCESS_MAP = {}

def get_process_list():
    global PROCESS_MAP
    PROCESS_MAP = {}

    grouped = defaultdict(int)

    for proc in psutil.process_iter(['pid', 'name', 'username', 'exe']):
        try:
            name = proc.info['name'] or ""
            username = proc.info['username'] or ""
            exe = proc.info['exe'] or ""
            if not username or "SYSTEM" in username.upper():
                continue
            if exe.startswith(("C:\\Windows", "C:\\Program Files\\WindowsApps")):
                continue

            if name.lower() in [
                "svchost.exe", "services.exe", "lsass.exe",
                "wininit.exe", "csrss.exe", "msedgewebview2.exe"
            ]:
                continue
            grouped[name] += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    lines = []
    for i, (name, count) in enumerate(grouped.items(), 1):
        PROCESS_MAP[i] = name

        if count == 1:
            lines.append(f"{i}. {name}")
        else:
            lines.append(f"{i}. {name} ({count})")

    return "\n".join(lines)

def task_killer(number: int):
    name = PROCESS_MAP.get(number)
    if not name:
        return False

    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'] == name:
                proc.terminate()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return True
    import wmi

def get_devices():
    c = wmi.WMI()
    seen = set()
    devices = []
    EXTERNAL_PNP_CLASSES = {
        "Mouse", "Keyboard", "HIDClass", "USB", "Bluetooth",
        "Net", "Image", "Camera", "AudioEndpoint", "MEDIA",
        "Printer", "DiskDrive", "Monitor", "CDROM"
    }

    for device in c.Win32_PnPEntity():
        name = device.Name
        pnp_class = device.PNPClass
        if not name or not pnp_class:
            continue
        if pnp_class not in EXTERNAL_PNP_CLASSES:
            continue

        clean_name = re.sub(
            r'\s*\((майкрософт|microsoft)\)',
            '',
            name.strip(),
            flags=re.IGNORECASE
        ).strip()
        if clean_name in seen:
            continue

        seen.add(clean_name)
        devices.append(f"{clean_name} | {device.Status}")

    return "\n".join(devices)