from typing import Any
import mss
import pyautogui
from pywinauto import Application, WindowSpecification
import numpy as np
from windowmanager.WindowManager import WindowManager

class ApplicationWindow(WindowManager):
    """Encapsulates some calls to pywinauto for window management"""
    def __init__(self, process_id):
        self.sct = mss.mss()
        super().__init__(process_id)
        self._handle: WindowSpecification
        self.window_position = None
    
    def find_window(self, window_name: str):
        """find a window by its class_name"""
        app = Application(backend="uia").connect(process=self._process_id)
        self._handle = app.window(title_re=window_name)

    def set_foreground(self):
        """put the window in the foreground"""
        self._handle.set_focus()
        
    def get_window_location(self) -> tuple:
        """get the window location"""
        rect = self._handle.rectangle()
        return rect
    
    def capture_window_screenshot(self) -> np.ndarray:
        #screenshot = pyautogui.screenshot()
        # Crop the screenshot to the window location
        #numpy_image = np.array(screenshot)
        if self.window_position is None:
            self.window_position = self.get_window_location()
        location = self.window_position # type: ignore
        monitor = {
            "top": location.top, # type: ignore
            "left": location.left, # type: ignore
            "width": location.right - location.left, # type: ignore
            "height": location.bottom - location.top # type: ignore
        }
        screenshot = self.sct.grab(monitor)
        numpy_image = np.array(screenshot)
        return numpy_image

    def click_inside_window(self, coordinates: tuple):
        window_pos = self.get_window_location()
        click_coordinates_x = window_pos.left + coordinates[0] # type: ignore
        click_coordinates_y = window_pos.top + coordinates[1] # type: ignore
        pyautogui.moveTo(click_coordinates_x, click_coordinates_y)
        pyautogui.click()