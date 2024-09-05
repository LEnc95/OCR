from flask import Flask, request, jsonify, render_template
from PIL import Image
import pytesseract
import cv2
import numpy as np
import logging
from transformers import pipeline

app = Flask(__name__)

# Set max file size to 5MB (adjust as needed)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB limit

# Load a local LLM model for text revision (using GPT-2 for example)
revision_model = pipeline("text-generation", model="gpt2")

def revise_text_with_llm(extracted_text):
    try:
        response = revision_model(extracted_text, max_length=500, num_return_sequences=1)[0]['generated_text']
        return response
    except Exception as e:
        logging.error(f"Error during LLM revision: {str(e)}")
        return extracted_text  # Return original if LLM revision fails

@app.route('/')
def index():
    return render_template('index.html')

@app.errorhandler(413)
def file_too_large(e):
    return jsonify({'error': 'File too large. Maximum size allowed is 5MB.'}), 413

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    try:
        if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            return jsonify({'error': 'Invalid file type. Only PNG, JPG, and JPEG are allowed.'}), 400

        image = Image.open(file.stream)
        open_cv_image = np.array(image.convert('RGB'))
        open_cv_image = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2BGR)

        gray_image = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
        denoised_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
        _, thresholded_image = cv2.threshold(denoised_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        ocr_text = pytesseract.image_to_string(thresholded_image)

        return jsonify({'extracted_text': ocr_text})

    except Exception as e:
        app.logger.error(f"Error processing file: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/revise-text', methods=['POST'])
def revise_text():
    data = request.get_json()
    extracted_text = data.get('text', '')

    if not extracted_text:
        return jsonify({'error': 'No text provided for revision'}), 400

    revised_text = revise_text_with_llm(extracted_text)
    return jsonify({'revised_text': revised_text})

if __name__ == '__main__':
    app.run(debug=True)
