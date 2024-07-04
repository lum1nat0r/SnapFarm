import numpy as np
import cv2
import pytesseract

class ImageProcessor:
    @staticmethod
    def process_image(image, reduced_mode: bool = False):
        # Preprocess the image using OpenCV
        # Apply grayscale filter
        numpy_image = np.array(image)
        # Convert RGB to BGR (OpenCV uses BGR)
        numpy_image = numpy_image[:, :, ::-1].copy()
        gray_image = cv2.cvtColor(numpy_image, cv2.COLOR_BGR2GRAY)

        if reduced_mode:
            return gray_image
        
        # Apply thresholding
        ret, threshold_image = cv2.threshold(gray_image, 155, 255, cv2.THRESH_BINARY)

        # Apply dilation and erosion to reduce noise
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        dilated_image = cv2.dilate(threshold_image, kernel, iterations=1)

        return dilated_image
    
    @staticmethod
    def find_text(image, text: str, config: str = "--oem 3 --psm 6"):
        # Find the text in the image using Tesseract OCR
        # pytesseract requires the image to be in RGB format
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        text_found = pytesseract.image_to_string(image_rgb, config=config)
        return text.lower() in text_found.lower()
    
    @staticmethod
    def warp_next_button(image):
        tl = (int(image.shape[1] * 0.25), int(image.shape[0] * 0.45))
        bl = (int(image.shape[1] * 0.20), int(image.shape[0] * 0.65))
        tr = (int(image.shape[1] * 0.65), int(image.shape[0] * 0.45))
        br = (int(image.shape[1] * 0.75), int(image.shape[0] * 0.85))

        pts1 = np.float32([tl, tr, bl, br])
        pts2 = np.float32([[bl[0], tr[1]], [tr[0], tr[1]], [bl[0]*0.9, br[1]*0.8], [br[0]*1.1, br[1]]])

        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        result = cv2.warpPerspective(image, matrix, (image.shape[1], image.shape[0]))

        # Crop the image to the relevant area (inside the markings)
        x_min = min(tl[0], bl[0])
        x_max = max(tr[0], br[0])
        y_min = min(tl[1], tr[1])
        y_max = max(bl[1], br[1])
        result = result[y_min:y_max, x_min:x_max]

        return result
    
    @staticmethod
    def erode_image(image, kernel_size: tuple = (1, 1), iterations: int = 1):
        kernel = np.ones(kernel_size, np.uint8)
        eroded_image = cv2.erode(image, kernel, iterations=iterations)
        return eroded_image
    
    @staticmethod
    def dilate_image(image, kernel_size: tuple = (1, 1), iterations: int = 1):
        kernel = np.ones(kernel_size, np.uint8)
        dilated_image = cv2.dilate(image, kernel, iterations=iterations)
        return dilated_image
    
    @staticmethod
    def match_template(image, template, method=cv2.TM_SQDIFF_NORMED):
        result = cv2.matchTemplate(image, template, method)
        return result