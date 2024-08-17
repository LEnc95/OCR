from fastapi import FastAPI, File, UploadFile, HTTPException
from PIL import Image, ImageEnhance, ImageOps
import pytesseract
import cv2
import numpy as np
import io

app = FastAPI()


def preprocess_image(image: Image.Image) -> Image.Image:

    # Convert PIL Image to a NumPy array
    image_np = np.array(image)

    # Convert to grayscale (if not already)
    if len(image_np.shape) == 3:
        image_np = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)

    # Normalize the image to the range [0, 255]
    image_np = cv2.normalize(image_np, None, 0, 255, cv2.NORM_MINMAX)

    # Apply thresholding
    _, image_np = cv2.threshold(image_np, 100, 255, cv2.THRESH_BINARY)

    # Apply Gaussian Blur
    image_np = cv2.GaussianBlur(image_np, (1, 1), 0)

    # Convert back to a PIL Image
    processed_image = Image.fromarray(image_np)

    return processed_image


@app.post("/ocr/")
async def perform_ocr(file: UploadFile = File(...)):
    try:
        # Read the uploaded image
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data))

        # Preprocess the image
        processed_image = preprocess_image(image)

        # Perform OCR using Tesseract with specific configurations
        '''
        oem - OCR Engine Mode
            0 = Original Tesseract only.
            1 = Neural nets LSTM only.
            2 = Tesseract + LSTM.
            3 = Default, based on what is available.
        psm - Page Segmentation Mode
            0 = Orientation and script detection (OSD) only.
            1 = Automatic page segmentation with OSD.
            2 = Automatic page segmentation, but no OSD, or OCR. (not implemented)
            3 = Fully automatic page segmentation, but no OSD. (Default)
            4 = Assume a single column of text of variable sizes.
            5 = Assume a single uniform block of vertically aligned text.
            6 = Assume a single uniform block of text.
            7 = Treat the image as a single text line.
            8 = Treat the image as a single word.
            9 = Treat the image as a single word in a circle.
            10 = Treat the image as a single character.
            11 = Sparse text. Find as much text as possible in no particular order.
            12 = Sparse text with OSD.
            13 = Raw line. Treat the image as a single text line,
                bypassing hacks that are Tesseract-specific.
        '''
        custom_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(processed_image, config=custom_config)
        print(text)
        return {"extracted_text": text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error performing OCR: {str(e)}")