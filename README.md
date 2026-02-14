# Universal Document Converter

A simple GUI application for converting between different document formats.

## Features

- **PDF to Word** - Convert PDF files to editable DOCX format
- **Word to PDF** - Convert DOCX/DOC files to PDF
- **Image to PDF** - Combine multiple images into a single PDF
- **PDF to Images** - Extract pages from PDF as PNG images

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. For PDF to Images conversion on Linux, install poppler:
```bash
sudo apt-get install poppler-utils
```

## Usage

Run the application:
```bash
python converter_app.py
```

1. Select the conversion type
2. Click "Select File & Convert"
3. Choose your input file(s)
4. The converted file will be saved in the same directory (or choose location for multi-file conversions)

## Notes

- Word to PDF conversion requires Microsoft Word on Windows or LibreOffice on Linux
- Large PDF files may take time to convert
- Image to PDF supports JPG, PNG, BMP, and GIF formats
