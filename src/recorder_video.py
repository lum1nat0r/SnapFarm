import os
import cv2
import numpy as np
import psutil
from pywinauto import Application
import mss
import time

# Find the SNAP process
snap_process = None
for proc in psutil.process_iter(['name']):
    if proc.info['name'] == "SNAP.exe":
        snap_process = proc
        break

if snap_process is None:
    raise Exception("SNAP.exe process not found")

# Connect to the SNAP window
window = Application(backend="uia").connect(process=snap_process.pid)
window = window.window(title_re="SNAP")
window.set_focus()

# Ensure the "videos" folder exists
if not os.path.exists('videos'):
    os.makedirs('videos')

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
timestamp = int(time.time())
file_path = os.path.join('videos', f'{timestamp}.avi')
frame_rate = 30  # frames per second
video_writer = None

sct = mss.mss()
monitor = {
    "top": window.rectangle().top, 
    "left": window.rectangle().left, 
    "width": window.rectangle().right - window.rectangle().left, 
    "height": window.rectangle().bottom - window.rectangle().top
}

try:
    while True:
        last_time = time.time()
        
        # Take a screenshot
        screenshot = sct.grab(monitor)

        # Convert the screenshot to a numpy array
        numpy_image = np.array(screenshot)

        # Convert BGRA to BGR
        numpy_image = cv2.cvtColor(numpy_image, cv2.COLOR_BGRA2BGR)

        # Initialize the video writer object with the correct frame size
        if video_writer is None:
            height, width, _ = numpy_image.shape
            video_writer = cv2.VideoWriter(file_path, fourcc, frame_rate, (width, height))

        # Write the frame to the video file
        video_writer.write(numpy_image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        fps = 1 / (time.time() - last_time)
        # Calculate and print the frame rate
        print(f"Frame rate: {fps:.2f} fps")


except KeyboardInterrupt:
    # Graceful exit on Ctrl+C
    pass
finally:
    if video_writer is not None:
        video_writer.release()
    cv2.destroyAllWindows()
