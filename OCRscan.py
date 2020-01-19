from PIL import Image
import pytesseract
import cv2
import numpy as np


im = cv2.imread("prenkist.jpeg")
gray = cv2.imread(im, cv2.IMREAD_GRAYSCALE)
cv2.imwrite("prenkistprenk.jpeg", graycv2.imshow("prenks", gray)

cv2.waitKey(0)
cv2.destroyAllWindows()

text = pytesseract.image_to_string(im, lang = 'eng')
