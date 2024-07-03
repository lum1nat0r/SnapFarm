import cv2
import os

import pyautogui

from windowmanager.WindowManager import WindowManager


class VideoWindow(WindowManager):
    def __init__(self, video_url):
        super().__init__(video_url)
        self._handle = None
    
    def find_window(self, window_name=None):
        # check if video_url does exist
        if not self._process_id:
            raise ValueError("Video URL not found.")
        # check if file exists
        if not os.path.exists(self._process_id):
            raise FileNotFoundError(f"Video file {self._process_id} not found.")
    
    def set_foreground(self):
        # Open the video file
        self._handle = cv2.VideoCapture(self._process_id)
        if not self._handle.isOpened():
            raise ValueError("Error: Could not open video file.")

    def get_window_location(self) -> tuple:
        # get the video properties
        width = int(self._handle.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self._handle.get(cv2.CAP_PROP_FRAME_HEIGHT))
        return 0, 0, width, height

    def capture_window_screenshot(self):
        # Read the next frame
        if self._handle is None:
            raise ValueError("Error: Video handle is not initialized. Call set_foreground first.")

        ret, frame = self._handle.read()
        if not ret:
            print("Error reading frame or end of video reached.")
            return None

        cv2.imshow('frame', frame)
        cv2.waitKey(1)
        return frame
    
    def click_play_button(self):
        window_location = self.get_window_location()
        play_button_x = window_location[2] // 2
        play_button_y = window_location[3] // 6 * 5
        pyautogui.moveTo(play_button_x, play_button_y)
        print("Clicking play button on position:", play_button_x, play_button_y)
    
    def click_lower_right_button(self):
        window_location = self.get_window_location()
        lower_right_button_x = window_location[2] * 0.9
        lower_right_button_y = window_location[3] * 0.9
        pyautogui.moveTo(lower_right_button_x, lower_right_button_y)
        print("Clicking lower right button on position:", lower_right_button_x, lower_right_button_y)