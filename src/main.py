import psutil
import time
import cv2
import pyautogui
import numpy as np
from PIL import Image
import pytesseract
from bot.Bot import Bot
from windowmanager.VideoWindow import VideoWindow
from windowmanager.ApplicationWindow import ApplicationWindow
from windowmanager.WindowManager import WindowManager

if __name__ == "__main__":
    print("Starting SNAPFarm")
    snap_bot = Bot()
    snap_process_id = snap_bot.get_process_id("SNAP.exe")
    window_title = "SNAP"
    # window_manager = VideoWindow("videos/Test_Run.avi")
    window_manager = ApplicationWindow(snap_process_id)
    snap_bot.run(window_manager, window_title)

