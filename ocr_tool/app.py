from flask import Flask, request, jsonify, render_template
from PIL import Image
import pytesseract
import cv2
import numpy as np
import logging
from symspellpy.symspellpy import SymSpell, Verbosity
from transformers import T5ForConditionalGeneration, T5Tokenizer
import pkg_resources

app = Flask(__name__)

# Initialize SymSpell for spelling corrections
symspell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)

# Load dictionary for SymSpell
dictionary_path = pkg_resources.resource_filename(
    "symspellpy", "frequency_dictionary_en_82_765.txt"
)
if not symspell.load_dictionary(dictionary_path, term_index=0, count_index=1):
    logging.error("SymSpell dictionary file not found")

# Set max file size to 5MB (adjust as needed)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB limit

# Load the T5 model for grammar and spelling correction
model_name = "flexudy/t5-small-wav2vec2-grammar-fixer"
logging.info("Loading model...")
model = T5ForConditionalGeneration.from_pretrained(model_name)
tokenizer = T5Tokenizer.from_pretrained(model_name)
logging.info("Model loaded successfully!")

def correct_spelling(text):
    suggestions = symspell.lookup_compound(text, max_edit_distance=2)
    if suggestions:
        return suggestions[0].term  # Return the corrected spelling
    return text  # Return the original text if no corrections found

def revise_text_with_t5(text):
    try:
        logging.info(f"Original text for revision: {text}")
        
        # Refine the input prompt to focus on correcting grammar and structure after spelling corrections
        input_text = f"Fix any grammatical errors in this text: {text}"
        
        # Encode the input, truncating if necessary
        inputs = tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True)

        # Generate the corrected text
        outputs = model.generate(inputs, max_length=512, num_return_sequences=1)
        corrected_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

        logging.info(f"Revised text: {corrected_text}")
        return corrected_text
    except Exception as e:
        logging.error(f"Error during LLM revision: {str(e)}")
        return text  # Return the original text if there's an issue with the LLM

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

        # Preprocess the image (grayscale, denoise, and threshold)
        gray_image = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
        denoised_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
        _, thresholded_image = cv2.threshold(denoised_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Perform OCR on the preprocessed image (extracted text is returned unchanged)
        ocr_text = pytesseract.image_to_string(thresholded_image)

        logging.info(f"OCR extracted text: {ocr_text}")

        return jsonify({'extracted_text': ocr_text})

    except Exception as e:
        app.logger.error(f"Error processing file: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

# This route is triggered when the "Revise Text" button is clicked
@app.route('/revise-text', methods=['POST'])
def revise_text():
    data = request.get_json()
    extracted_text = data.get('text', '')

    if not extracted_text:
        return jsonify({'error': 'No text provided for revision'}), 400

    # First, correct the spelling using SymSpell
    spelling_corrected_text = correct_spelling(extracted_text)

    # Then, revise the text for grammar using the LLM
    revised_text = revise_text_with_t5(spelling_corrected_text)

    return jsonify({'revised_text': revised_text})

if __name__ == '__main__':
    app.run(debug=True)
