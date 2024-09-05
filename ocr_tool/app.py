from flask import Flask, request, jsonify
from PIL import Image
import pytesseract
import io
import cv2
import numpy as np
import logging

app = Flask(__name__)

# Specify the path to tesseract.exe (update if installed elsewhere)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Configure logging
logging.basicConfig(filename='ocr_log.log', level=logging.INFO)

# Define the languages to support (English, Spanish, French, Hindi, Bengali, Tamil, etc.)
languages = 'eng+spa+fra+hin+ben+tam+tel+pan+mar+iku'

# Endpoint to handle file upload and OCR processing
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        app.logger.error('No file part in the request')
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        app.logger.error('No file selected for uploading')
        return jsonify({'error': 'No file selected'}), 400

    try:
        # Ensure the file is an image
        if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            app.logger.error('Invalid file type uploaded')
            return jsonify({'error': 'Invalid file type. Only PNG, JPG, and JPEG are allowed.'}), 400

        # Convert the file to an image
        image = Image.open(file.stream)

        # Convert PIL image to OpenCV format
        open_cv_image = np.array(image.convert('RGB')) 
        open_cv_image = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2BGR)

        # Preprocess the image (grayscale, denoise, and threshold)
        gray_image = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian Blur to reduce noise
        denoised_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

        # Apply Otsu's thresholding to improve text contrast
        _, thresholded_image = cv2.threshold(denoised_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Perform OCR with support for multiple languages
        ocr_text = pytesseract.image_to_string(thresholded_image, lang=languages)

        # Log the processed file and result
        app.logger.info(f'Processed file: {file.filename}, extracted text: {ocr_text[:50]}...')

        return jsonify({'extracted_text': ocr_text})
    
    except Exception as e:
        app.logger.error(f"Error processing file: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
