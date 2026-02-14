#!/usr/bin/env python3
from flask import Flask, render_template, request, send_file, jsonify
from pathlib import Path
import os
import tempfile
import zipfile
import atexit
import shutil

from pdf2docx import Converter
from docx2pdf import convert as docx_to_pdf
import img2pdf
from pdf2image import convert_from_path

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

temp_files = []

def cleanup():
    for f in temp_files:
        try:
            if os.path.exists(f):
                os.unlink(f)
        except:
            pass

atexit.register(cleanup)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    conversion_type = request.form.get('type')
    files = request.files.getlist('file')
    
    if not files or not files[0].filename:
        return jsonify({'error': 'No file selected'}), 400
    
    try:
        if conversion_type == 'pdf_to_word':
            file = files[0]
            tmp_in = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
            file.save(tmp_in.name)
            tmp_in.close()
            
            output = tempfile.NamedTemporaryFile(delete=False, suffix='.docx').name
            cv = Converter(tmp_in.name)
            cv.convert(output)
            cv.close()
            
            temp_files.extend([tmp_in.name, output])
            return send_file(output, as_attachment=True, download_name=f"{Path(file.filename).stem}.docx")
        
        elif conversion_type == 'word_to_pdf':
            file = files[0]
            tmp_in = tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix)
            file.save(tmp_in.name)
            tmp_in.close()
            
            output = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf').name
            docx_to_pdf(tmp_in.name, output)
            
            temp_files.extend([tmp_in.name, output])
            return send_file(output, as_attachment=True, download_name=f"{Path(file.filename).stem}.pdf")
        
        elif conversion_type == 'image_to_pdf':
            img_files = []
            for f in files:
                tmp = tempfile.NamedTemporaryFile(delete=False, suffix=Path(f.filename).suffix)
                f.save(tmp.name)
                tmp.close()
                img_files.append(tmp.name)
            
            output = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf').name
            with open(output, "wb") as out:
                out.write(img2pdf.convert(img_files))
            
            temp_files.extend(img_files + [output])
            return send_file(output, as_attachment=True, download_name="converted.pdf")
        
        elif conversion_type == 'pdf_to_images':
            file = files[0]
            tmp_in = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
            file.save(tmp_in.name)
            tmp_in.close()
            
            images = convert_from_path(tmp_in.name)
            
            zip_path = tempfile.NamedTemporaryFile(delete=False, suffix='.zip').name
            with zipfile.ZipFile(zip_path, 'w') as zf:
                for i, img in enumerate(images):
                    img_path = tempfile.NamedTemporaryFile(delete=False, suffix='.png').name
                    img.save(img_path, 'PNG')
                    zf.write(img_path, f"page_{i+1}.png")
                    temp_files.append(img_path)
            
            temp_files.extend([tmp_in.name, zip_path])
            return send_file(zip_path, as_attachment=True, download_name=f"{Path(file.filename).stem}_images.zip")
        
        return jsonify({'error': 'Invalid conversion type'}), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    os.makedirs('templates', exist_ok=True)
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
