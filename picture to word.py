from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
import cv2
import mediapipe as mp
import math
import pyautogui
import numpy as np
filepath = r'D:\project\good.JPG'

img = Image.open(filepath)
text = pytesseract.image_to_string(img, lang='chi_tra')
print(text)