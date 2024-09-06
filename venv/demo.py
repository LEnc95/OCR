import pytesseract
import cv2
from PIL import Image
import os
import numpy as np

# Set the path to Tesseract executable within the virtual environment
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Luke\Documents\GitHub\OCR\venv\Lib\tesseract\tesseract.exe'

def ocr_core(image_path):
    # Read the image using PIL
    img = Image.open(image_path)
    
    # Convert image to grayscale
    gray = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)
    
    # Use Tesseract to do OCR on the image
    text = pytesseract.image_to_string(gray)
    
    return text

# Example usage
# image_path = r'.\img\Capture1.PNG'
image_path = r'C:\\Users\\914476\\Documents\\Github\\OCR\\venv\\img\\Capture1.PNG'
image_path = os.path.abspath(image_path)
extracted_text = ocr_core(image_path)
print(extracted_text)
