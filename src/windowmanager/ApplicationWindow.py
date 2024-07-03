import pyautogui
from pywinauto import Application
import numpy as np
from windowmanager.WindowManager import WindowManager

class ApplicationWindow(WindowManager):
    """Encapsulates some calls to pywinauto for window management"""
    def __init__(self, process_id):
        super().__init__(process_id)
        self._handle = None
    
    def find_window(self, window_name=None):
        """find a window by its class_name"""
        self._handle = Application(backend="uia").connect(process=self._process_id)
        if window_name:
            self._handle = self._handle.window(title_re=window_name)

    def set_foreground(self):
        """put the window in the foreground"""
        self._handle.set_focus()
        
    def get_window_location(self) -> tuple:
        """get the window location"""
        rect = self._handle.rectangle()
        return rect
    
    def capture_window_screenshot(self) -> np.ndarray:
        screenshot = pyautogui.screenshot()
        # Crop the screenshot to the window location
        numpy_image = np.array(screenshot)
        location = self.get_window_location()
        cropped_image = numpy_image[location.top:location.bottom, location.left:location.right]
        return cropped_image
    
    def click_play_button(self):
        window_location = self.get_window_location()
        play_button_x = window_location.left + ((window_location.right - window_location.left) // 2)
        play_button_y = window_location.top + ((window_location.bottom - window_location.top) // 6 * 5)
        pyautogui.moveTo(play_button_x, play_button_y)
        pyautogui.click()

    def click_lower_right_button(self):
        window_location = self.get_window_location()
        lower_right_button_x = window_location.right * 0.9
        lower_right_button_y = window_location.bottom * 0.9
        pyautogui.moveTo(lower_right_button_x, lower_right_button_y)
        pyautogui.click()