

import json
import time

import cv2
from matplotlib import pyplot as plt
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
            scale_factors = self.__calculate_scale_factors(image)
            height, width = image.shape

            height_fraction = height // 5
            width_fraction = width // 7
            roi_height_start = height_fraction * 4
            roi_width_start = width_fraction * 3

            roi = image[height_fraction*4:, width_fraction*3:width_fraction*4]

            template = cv2.imread("assets/img/templates/play_button.png")
            template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
            template = cv2.resize(template, (0, 0), fx=scale_factors[1], fy=scale_factors[0])
            w, h = template.shape[::-1]
            result = ImageProcessor.match_template(roi, template, cv2.TM_CCORR_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            print("[PLAY] Confidence:", max_val)
            cv2.rectangle(roi, max_loc, (max_loc[0] + w, max_loc[1] + h), 255, 2)
            cv2.imshow("roi", roi)
            cv2.waitKey(1)
            if max_val > 0.90:
                print("Found play button with confidence:", max_val)
                # calculate the location of the button (max_loc + height // 2, max_loc + width // 2)
                button_pos = (max_loc[0] + w // 2, max_loc[1] + h // 2)
                button_pos = (button_pos[0] + roi_width_start, button_pos[1] + roi_height_start)
                print("Returning coordinates:", button_pos)
                time.sleep(2)
                return CLICK_PLAY, button_pos
            return SKIP, None
        
        if current_state == PLAYING:
            scale_factors = self.__calculate_scale_factors(image)
            height, width = image.shape
            height_fraction = height // 5
            width_fraction = width // 5
            relevant_height_start = height_fraction * 4
            relevant_width_start = width_fraction * 4
            roi = image[relevant_height_start:, relevant_width_start:]

            template = cv2.imread("assets/img/templates/collect_rewards.png")
            template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
            template = cv2.resize(template, (0, 0), fx=scale_factors[1], fy=scale_factors[0])
            w, h = template.shape[::-1]
            result = ImageProcessor.match_template(roi, template, cv2.TM_CCORR_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            print("[REWARDS] Confidence:", max_val)
            cv2.rectangle(roi, max_loc, (max_loc[0] + w, max_loc[1] + h), 255, 2)
            cv2.imshow("roi", roi)
            cv2.waitKey(1)
            if max_val > 0.95:
                print("Found collect rewards button with confidence:", max_val)
                # calculate the location of the button (max_loc + height // 2, max_loc + width // 2)
                button_pos = (max_loc[0] + w // 2, max_loc[1] + h // 2)
                button_pos = (button_pos[0] + relevant_width_start, button_pos[1] + relevant_height_start)
                print("Returning coordinates:", button_pos)
                time.sleep(2)
                return CLICK_LOWER_RIGHT, button_pos
            return SKIP, None
            
        
        if current_state == REWARDS_OVERVIEW:
            scale_factors = self.__calculate_scale_factors(image)
            height, width = image.shape
            height_fraction = height // 5
            width_fraction = width // 5
            relevant_height_start = height_fraction * 4
            relevant_width_start = width_fraction * 4
            roi = image[relevant_height_start:, relevant_width_start:]

            template = cv2.imread("assets/img/templates/next_button.png")
            template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
            template = cv2.resize(template, (0, 0), fx=scale_factors[1], fy=scale_factors[0])
            w, h = template.shape[::-1]
            result = ImageProcessor.match_template(roi, template, cv2.TM_CCORR_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            print("[NEXT] Confidence:", max_val)
            cv2.rectangle(roi, max_loc, (max_loc[0] + w, max_loc[1] + h), 255, 2)
            cv2.imshow("roi", roi)
            cv2.waitKey(1)
            if max_val > 0.95:
                print("Found next button with confidence:", max_val)
                # calculate the location of the button (max_loc + height // 2, max_loc + width // 2)
                button_pos = (max_loc[0] + w // 2, max_loc[1] + h // 2)
                button_pos = (button_pos[0] + relevant_width_start, button_pos[1] + relevant_height_start)
                print("Returning coordinates:", button_pos)
                time.sleep(2)
                return CLICK_LOWER_RIGHT, button_pos
            return SKIP, None

    def __calculate_scale_factors(self, image):
        template_resolution = json.load(open("assets/img/templates/resolution.json", "r"))
        image_resolution = image.shape
        scale_factors = (image_resolution[0] / template_resolution["height"], image_resolution[1] / template_resolution["width"])
        return scale_factors

    def __make_decision_with_template_matching(self, template_path: str, image, threshold: float):
        template = cv2.imread(template_path)
        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        w, h = template.shape[::-1]
        result = ImageProcessor.match_template(image, template, cv2.TM_CCORR_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if max_val > threshold:
            return max_val
        return 0.0
    
