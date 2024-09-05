# OCR Application

This is a Flask-based web application that allows users to upload images for text extraction using Tesseract OCR. It supports image preview, text extraction, and the ability to download the extracted text or copy it to the clipboard.

## Features

- Single image processing for OCR.
- Image preview before processing.
- Download extracted text as a `.txt` file.
- Copy extracted text to clipboard.
- File size validation (max 5MB).

## Planned Features

- Batch processing for multiple images.
- Azure deployment for cloud-based OCR processing.
- Large Language Model (LLM) integration for text accuracy improvements.
- Multi-language OCR support.

## Prerequisites

To run this application, you will need to have the following installed on your system:

### 1. **Tesseract OCR**
Tesseract is the engine used for Optical Character Recognition (OCR). You need to install Tesseract and ensure it is accessible via the system PATH.

- **Windows**: Download and install Tesseract from [here](https://github.com/UB-Mannheim/tesseract/wiki).
- **Linux (Ubuntu)**:
  ```bash
  sudo apt update
  sudo apt install tesseract-ocr
  sudo apt install libtesseract-dev
  ```

### 2. **Python 3.x**

Ensure Python 3.x is installed. You can download Python from the official website: [Python Downloads](https://www.python.org/downloads/)

### 3. **Tesseract Language Data (Optional)**
For multi-language support (currently disabled), download and place the necessary `.traineddata` files in your `tessdata` folder.

## Environment Setup

Clone the repository and install the required dependencies:

```bash
git clone <repository-url>
cd <repository-folder>
pip install -r requirements.txt
```

Alternatively, if `requirements.txt` isn't present, manually install the dependencies:

```bash
pip install flask pillow pytesseract opencv-python numpy
```

## Configuration

1. **Set TESSDATA_PREFIX** (Important):

- **Windows**:
  - Go to System Properties -> Advanced -> Environment Variables.
  - Add a new system variable:
    - **Variable Name**: `TESSDATA_PREFIX`
    - **Variable Value**: `C:\Program Files\Tesseract-OCR\` (or the path where Tesseract is installed).

- **Linux**:
  Add this to your `~/.bashrc` or run it before starting the app:
  ```bash
  export TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00/tessdata/
  ```

2. **Check Language Packs** (Optional):
   - Ensure that the required language files (e.g., `eng.traineddata` for English) are present in the `tessdata` folder.

## Running the Application

After setting up the environment, you can run the application locally:

```bash
python app.py
```

The app will be available at: `http://127.0.0.1:5000/`

## Deployment (Optional)

For production deployment, consider using Gunicorn:

```bash
gunicorn --bind 0.0.0.0:5000 app:app
```

### Deploy to Azure (Planned)
The application can be deployed to Azure for scalable cloud-based OCR processing. Follow Azure’s Python Flask deployment guide for more information.

## File Upload Instructions

- **File Format**: The application supports `.png`, `.jpg`, and `.jpeg` image formats.
- **Max File Size**: The maximum file size is 5MB.

## Current Known Issues

- Multi-language OCR support is currently disabled due to language pack availability. Ensure `eng.traineddata` exists in the `tessdata` folder for English OCR.

## License

This project is licensed under the MIT License.

---

Let me know if you need further customization for the README or any additional sections!
