from flask import Flask, request, jsonify, render_template
from PIL import Image
import pytesseract
import io
import cv2
import numpy as np
import logging

app = Flask(__name__)

# Set up logging for OCR process
logging.basicConfig(filename='ocr_log.log', level=logging.INFO)

# Path to Tesseract (if needed)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Route to render the index.html page
@app.route('/')
def index():
    return render_template('index.html')  # Serve index.html from the templates folder

# Error handler for files that exceed the size limit
@app.errorhandler(413)
def file_too_large(e):
    return jsonify({'error': 'File too large. Maximum size allowed is 5MB.'}), 413

# Batch upload route for processing multiple images
@app.route('/batch_upload', methods=['POST'])
def batch_upload():
    if 'files' not in request.files:
        app.logger.error('No files provided in the request')
        return jsonify({'error': 'No files provided'}), 400

    files = request.files.getlist('files')
    results = []

    for file in files:
        try:
            # Validate file type
            if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                app.logger.error(f'Invalid file type for file {file.filename}')
                results.append(f'Invalid file type for {file.filename}. Only PNG, JPG, and JPEG are allowed.')
                continue

            # Convert the file to an image for processing
            image = Image.open(file.stream)
            open_cv_image = np.array(image.convert('RGB'))  # Convert to OpenCV format
            open_cv_image = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2BGR)

            # Preprocess the image (grayscale, denoise, and threshold)
            gray_image = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
            denoised_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
            _, thresholded_image = cv2.threshold(denoised_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            # Perform OCR on the preprocessed image
            ocr_text = pytesseract.image_to_string(thresholded_image)

            # Log the processed file
            app.logger.info(f'Processed file: {file.filename}, extracted text: {ocr_text[:50]}...')
            results.append(ocr_text)

        except Exception as e:
            app.logger.error(f"Error processing file {file.filename}: {str(e)}")
            results.append(f"Error processing file {file.filename}: {str(e)}")

    return jsonify({'results': results})

if __name__ == '__main__':
    app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # Set max file size to 5MB
    app.run(debug=True)
