import time
import psutil
from bot.Actions import CLICK_LOWER_RIGHT, CLICK_PLAY
from bot.DecisionMaker import DecisionMaker
from bot.States import PLAYING, REWARDS_OVERVIEW, START_SCREEN
from image.ImageProcessor import ImageProcessor
from windowmanager.WindowManager import WindowManager

class Bot:
    def __init__(self):
        self.current_state = START_SCREEN
        self.window_manager: WindowManager
        self.decision_maker: DecisionMaker = DecisionMaker()
    
    def get_process_id(self, process_name: str) -> int:
        print("Starting bot...")
        print("Please make sure the game is running and it is NOT running in fullscreen mode (can be changed in the settings).")
        self.snap_process = self.__get_process(process_name)
        if self.snap_process is None:
            print(f"Process {process_name} not found.")
            print("Please start the game and try again.")
            raise Exception(f"Process {process_name} not found.")
        return self.snap_process.pid

    def run(self, window_manager: WindowManager, window_title: str):
        self.window_manager = window_manager
        self.window_manager.find_window(window_title)
        self.window_manager.set_foreground()
        time.sleep(1)

        self.__start_bot()
    
    def __get_process(self, process_name):
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] == process_name:
                return proc
        return None
    
    def __start_bot(self):
        print("Bot started...")
        while True:
            screenshot = self.window_manager.capture_window_screenshot()
            processed_image = ImageProcessor.process_image(screenshot, reduced_mode=True)
            decision, coordinates = self.decision_maker.make_decision(processed_image, self.current_state) # type: ignore
            new_state = self.__execute_decision(decision, coordinates) # type: ignore
            self.__update_state(new_state)
            time.sleep(0.5)
    
    def __execute_decision(self, decision: str, coordinates_inside_window: tuple):
        if decision == CLICK_PLAY:
            self.window_manager.click_inside_window(coordinates_inside_window)
            return PLAYING
        if decision == CLICK_LOWER_RIGHT:
            self.window_manager.click_inside_window(coordinates_inside_window)
            if self.current_state == PLAYING:
                return REWARDS_OVERVIEW
            return START_SCREEN
        return self.current_state

    def __update_state(self, new_state):
        if new_state != self.current_state:
            self.current_state = new_state
            print(f"State changed to {self.current_state}")
            time.sleep(3)