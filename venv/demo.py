import pytesseract
from PIL import Image
import cv2
import os

# Set the path to Tesseract executable within the virtual environment
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Luke\Documents\GitHub\OCR\venv\Lib\tesseract\tesseract.exe'

def ocr_core(image_path):
    # Read the image using OpenCV
    img = cv2.imread(image_path)
    
    # Convert image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Use Tesseract to do OCR on the image
    text = pytesseract.image_to_string(gray)
    
    return text

# Example usage
image_path = r'.\img\Capture1.PNG'
extracted_text = ocr_core(image_path)
print(extracted_text)
