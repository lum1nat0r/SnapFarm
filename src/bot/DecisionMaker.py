

import time
from bot.Actions import CLICK_LOWER_RIGHT, CLICK_PLAY, SKIP
from bot.States import PLAYING, REWARDS_OVERVIEW, START_SCREEN
from image.ImageProcessor import ImageProcessor


class DecisionMaker:
    def __init__(self, game_mode: str = "ranked") -> None:
        self.game_mode = game_mode

    def make_decision(self, image, current_state: int):
        if self.game_mode == "ranked":
            return self.__make_ranked_decision(image, current_state)
        return SKIP
    
    def __make_ranked_decision(self, image, current_state: int):
        if current_state == START_SCREEN:
            height, width = image.shape
            one_quarter_height = height // 4
            one_third_width = width // 3
            relevant_part = image[one_quarter_height*3:, one_third_width:one_third_width*2]
            roi = relevant_part[:, relevant_part.shape[1]//3:(relevant_part.shape[1]//3)*2]
            play_text_found = ImageProcessor.find_text(roi, "Play", config="--psm 6")
            if play_text_found:
                return CLICK_PLAY
            return SKIP
        if current_state == PLAYING:
            height, width = image.shape
            one_tenth_height = height // 5
            one_tenth_width = width // 5
            relevant_part = image[one_tenth_height*4:, one_tenth_width*4:]
            warped_next_button = ImageProcessor.warp_next_button(relevant_part)
            eroded_next_button = ImageProcessor.erode_image(warped_next_button, kernel_size=(3, 3), iterations=1)
            dilated_next_button = ImageProcessor.dilate_image(eroded_next_button, kernel_size=(2, 2), iterations=1)
            collect_text_found = ImageProcessor.find_text(dilated_next_button, "Collect", config="--psm 6 --oem 3")
            rewards_text_found = ImageProcessor.find_text(dilated_next_button, "Rewards", config="--psm 6 --oem 3")
            if collect_text_found or rewards_text_found:
                # sleep for 3 seconds, to make sure the button is clickable
                time.sleep(3)
                return CLICK_LOWER_RIGHT
            return SKIP
        if current_state == REWARDS_OVERVIEW:
            height, width = image.shape
            one_tenth_height = height // 5
            one_tenth_width = width // 5
            relevant_part = image[one_tenth_height*4:, one_tenth_width*4:]
            warped_next_button = ImageProcessor.warp_next_button(relevant_part)
            eroded_next_button = ImageProcessor.erode_image(warped_next_button, kernel_size=(3, 3), iterations=1)
            dilated_next_button = ImageProcessor.dilate_image(eroded_next_button, kernel_size=(2, 2), iterations=1)
            next_text_found = ImageProcessor.find_text(relevant_part, "Next", config="--psm 6 --oem 3")
            if next_text_found:
                # sleep for 3 seconds, to make sure the button is clickable
                time.sleep(3)
                return CLICK_LOWER_RIGHT
            return SKIP