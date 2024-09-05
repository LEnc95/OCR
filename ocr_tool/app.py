from flask import Flask, request, jsonify, render_template
from PIL import Image
import pytesseract
import cv2
import numpy as np
import logging

app = Flask(__name__)

# Set max file size to 5MB (adjust as needed)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB limit

# Route to serve the index.html page
@app.route('/')
def index():
    return render_template('index.html')

# Error handler for files that exceed the size limit
@app.errorhandler(413)
def file_too_large(e):
    return jsonify({'error': 'File too large. Maximum size allowed is 5MB.'}), 413

# Route to process a single image and perform OCR
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    try:
        # Validate file type
        if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            return jsonify({'error': 'Invalid file type. Only PNG, JPG, and JPEG are allowed.'}), 400

        # Convert the file to an image
        image = Image.open(file.stream)

        # Convert PIL image to OpenCV format
        open_cv_image = np.array(image.convert('RGB'))
        open_cv_image = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2BGR)

        # Preprocess the image (grayscale, denoise, and threshold)
        gray_image = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
        denoised_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
        _, thresholded_image = cv2.threshold(denoised_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Perform OCR on the preprocessed image
        ocr_text = pytesseract.image_to_string(thresholded_image)

        return jsonify({'extracted_text': ocr_text})

    except Exception as e:
        app.logger.error(f"Error processing file: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
