
import os
import cv2
import numpy as np
import psutil
from pywinauto import Application
import time
import pyautogui

snap_process = None
for proc in psutil.process_iter(['name']):
    if proc.info['name'] == "SNAP.exe":
        snap_process = proc
        break

# find window with title "SNAP"
window = Application(backend="uia").connect(process=snap_process.pid)
window = window.window(title_re="SNAP")
window.set_focus()

# Ensure the "screenshots" folder exists
if not os.path.exists('screenshots'):
    os.makedirs('screenshots')

while True:
    # Take a screenshot
    screenshot = pyautogui.screenshot()

    # Convert the screenshot to a numpy array
    numpy_image = np.array(screenshot)

    # Get the window rectangle (replace window.rectangle() with the actual way to get the rectangle)
    rect = window.rectangle()  # This line is just a placeholder; you need to define 'window'

    # Crop the image
    cropped_image = numpy_image[rect.top:rect.bottom, rect.left:rect.right]
    # Convert RGB to BGR (OpenCV uses BGR)
    cropped_image = cropped_image[:, :, ::-1].copy()

    # Save the cropped image with the current timestamp as name
    timestamp = int(time.time())
    file_path = os.path.join('screenshots', f'{timestamp}.png')
    cv2.imwrite(file_path, cropped_image)

    # Sleep for 1 second
    time.sleep(2)