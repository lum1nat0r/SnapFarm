import cv2
import pytesseract
from src.image.ImageProcessor import ImageProcessor
import numpy as np

# load image from file
image = cv2.imread("collect_rewards.png")
image = ImageProcessor.process_image(image, reduced_mode=True)

height, width = image.shape
one_tenth_height = height // 5
one_tenth_width = width // 5
relevant_part = image[one_tenth_height*4:, one_tenth_width*4:]

image = relevant_part

tl = (int(image.shape[1] * 0.25), int(image.shape[0] * 0.45))
bl = (int(image.shape[1] * 0.20), int(image.shape[0] * 0.65))
tr = (int(image.shape[1] * 0.65), int(image.shape[0] * 0.45))
br = (int(image.shape[1] * 0.75), int(image.shape[0] * 0.85))

cv2.imshow("inverted", image)

pts1 = np.float32([tl, tr, bl, br])
pts2 = np.float32([[bl[0], tr[1]], [tr[0], tr[1]], [bl[0]*0.9, br[1]*0.8], [br[0]*1.1, br[1]]])

matrix = cv2.getPerspectiveTransform(pts1, pts2)
result = cv2.warpPerspective(image, matrix, (image.shape[1], image.shape[0]))

cv2.imshow("result", result)

# Crop the image to the relevant area (inside the markings)
x_min = min(tl[0], bl[0])
x_max = max(tr[0], br[0])
y_min = min(tl[1], tr[1])
y_max = max(bl[1], br[1])
cropped = result[y_min:y_max, x_min:x_max]

cv2.imshow("cropped", cropped)

kernel = np.ones((3, 3), np.uint8)
erosion = cv2.erode(cropped, kernel, iterations=1)
kernel = np.ones((2,2),np.uint8)
dilation = cv2.dilate(erosion,kernel,iterations = 1)
cv2.imshow("eroded", erosion)

cv2.waitKey(0)
cv2.destroyAllWindows()

custom_config = r'--oem 3 --psm 6'
text = pytesseract.image_to_string(erosion, config=custom_config)
print(text)
