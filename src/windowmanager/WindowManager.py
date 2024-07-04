from abc import ABC, abstractmethod
import numpy as np

class WindowManager(ABC):
    """Encapsulates some calls to pywinauto for window management"""
    def __init__(self, process_id):
        """Constructor"""
        self._process_id = process_id
        self._handle = None

    @abstractmethod
    def find_window(self, window_name=None):
        pass
    
    @abstractmethod
    def set_foreground(self):
        pass
        
    @abstractmethod
    def get_window_location(self) -> tuple:
        pass
    
    @abstractmethod
    def capture_window_screenshot(self) -> np.ndarray:
        pass

    @abstractmethod
    def click_inside_window(self, coordinates: tuple):
        pass