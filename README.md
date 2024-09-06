# OCR Application

This is a Flask-based web application that allows users to upload images for text extraction using Tesseract OCR. The application supports image preview, text extraction, download, clipboard copy, and text revision through an integrated Large Language Model (LLM) to correct OCR-induced errors and refine the extracted text.

## Features

- Single image processing for OCR.
- Image preview before processing.
- Download extracted text as a `.txt` file.
- Copy extracted text to the clipboard.
- **LLM integration** for text revision (grammar and spelling corrections).
- **SymSpell** integration for correcting common OCR-induced spelling mistakes (e.g., correcting "cukure" to "culture").
- File size validation (max 5MB).

## Planned Features

- Batch processing for multiple images.
- Azure deployment for cloud-based OCR processing.
- Multi-language OCR support (future integration).

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

Ensure Python 3.x is installed. You can download Python from the official website: [Python Downloads](https://www.python.org/downloads/).

### 3. **Windows Build Tools for C++**

For **Windows** users, you need to install the **C++ Build Tools** required by `symspellpy`. To install them, run the following command in **PowerShell** (as Administrator):

```bash
npm install --global --production windows-build-tools
```

Alternatively, download the build tools directly from [here](https://visualstudio.microsoft.com/visual-cpp-build-tools/) and install the **Desktop development with C++** workload.

### 4. **Tesseract Language Data (Optional)**
For multi-language support (currently disabled), download and place the necessary `.traineddata` files in your `tessdata` folder.

## New Dependencies

In addition to the basic dependencies like Flask, Pillow, and Pytesseract, the following libraries have been added to support text revision and spelling correction:

- **SymSpell**: A fast spelling correction library for fixing OCR errors.
- **Transformers**: Hugging Face library for the Large Language Model (LLM) used to improve text accuracy.
- **PyTorch**: Backend for running the T5 LLM model.

## Environment Setup

Clone the repository and install the required dependencies:

```bash
git clone <repository-url>
cd <repository-folder>
pip install -r requirements.txt
```

Alternatively, if `requirements.txt` isn't present, manually install the dependencies:

```bash
pip install flask pillow pytesseract opencv-python numpy symspellpy transformers torch
```

### Create `requirements.txt`
To generate the `requirements.txt` file for easier dependency management, run:

```bash
pip freeze > requirements.txt
```

## Configuration

### 1. Set TESSDATA_PREFIX

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

### 2. Check Language Packs (Optional)
   - Ensure that the required language files (e.g., `eng.traineddata` for English) are present in the `tessdata` folder.

## Running the Application

After setting up the environment, you can run the application locally:

```bash
python app.py
```

The app will be available at: `http://127.0.0.1:5000/`.

## New Features (Usage)

### 1. **Upload an Image**

- Drag and drop an image or click to upload a PNG, JPG, or JPEG file.
- Make sure the file size is below 5MB.

### 2. **Extract Text**

- Once the image is uploaded, the OCR will extract the text from the image and display it in the interface.

### 3. **Revise Text (New Feature)**

- Click the **Revise Text** button to apply spelling corrections using **SymSpell** and grammatical improvements using the **T5 LLM**.
- The revised text will then be displayed, and you can download or copy the revised text.

### 4. **Download or Copy Text**

- After extracting or revising the text, you can download the text as a `.txt` file or copy it directly to your clipboard.

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

## Known Issues

- Multi-language OCR support is currently disabled due to language pack availability. Ensure `eng.traineddata` exists in the `tessdata` folder for English OCR.
- LLM processing may take longer for large text outputs, and grammar corrections may vary in accuracy.

## License

This project is licensed under the MIT License.
