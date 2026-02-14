#!/usr/bin/env python3
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
import threading

try:
    from pdf2docx import Converter
    from docx2pdf import convert as docx_to_pdf
    from PIL import Image
    import img2pdf
    from PyPDF2 import PdfMerger, PdfReader, PdfWriter
except ImportError:
    pass

class ConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Universal Document Converter")
        self.root.geometry("600x400")
        
        # Title
        title = tk.Label(root, text="Document Converter", font=("Arial", 20, "bold"))
        title.pack(pady=20)
        
        # Conversion type
        tk.Label(root, text="Select Conversion Type:", font=("Arial", 12)).pack(pady=10)
        
        self.conversion_type = tk.StringVar(value="pdf_to_word")
        conversions = [
            ("PDF to Word", "pdf_to_word"),
            ("Word to PDF", "word_to_pdf"),
            ("Image to PDF", "image_to_pdf"),
            ("PDF to Images", "pdf_to_images"),
        ]
        
        for text, value in conversions:
            tk.Radiobutton(root, text=text, variable=self.conversion_type, 
                          value=value, font=("Arial", 11)).pack(anchor=tk.W, padx=100)
        
        # Buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=30)
        
        tk.Button(btn_frame, text="Select File & Convert", command=self.convert,
                 bg="#4CAF50", fg="white", font=("Arial", 12), padx=20, pady=10).pack()
        
        # Status
        self.status = tk.Label(root, text="", font=("Arial", 10), fg="blue")
        self.status.pack(pady=10)
    
    def convert(self):
        conv_type = self.conversion_type.get()
        
        if conv_type == "pdf_to_word":
            file = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
            if file:
                threading.Thread(target=self.pdf_to_word, args=(file,)).start()
        
        elif conv_type == "word_to_pdf":
            file = filedialog.askopenfilename(filetypes=[("Word files", "*.docx *.doc")])
            if file:
                threading.Thread(target=self.word_to_pdf, args=(file,)).start()
        
        elif conv_type == "image_to_pdf":
            files = filedialog.askopenfilenames(filetypes=[("Images", "*.jpg *.jpeg *.png *.bmp *.gif")])
            if files:
                threading.Thread(target=self.image_to_pdf, args=(files,)).start()
        
        elif conv_type == "pdf_to_images":
            file = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
            if file:
                threading.Thread(target=self.pdf_to_images, args=(file,)).start()
    
    def pdf_to_word(self, pdf_file):
        self.status.config(text="Converting PDF to Word...")
        try:
            output = str(Path(pdf_file).with_suffix('.docx'))
            cv = Converter(pdf_file)
            cv.convert(output)
            cv.close()
            self.status.config(text=f"✓ Saved: {Path(output).name}", fg="green")
            messagebox.showinfo("Success", f"Converted to:\n{output}")
        except Exception as e:
            self.status.config(text="✗ Conversion failed", fg="red")
            messagebox.showerror("Error", str(e))
    
    def word_to_pdf(self, word_file):
        self.status.config(text="Converting Word to PDF...")
        try:
            output = str(Path(word_file).with_suffix('.pdf'))
            docx_to_pdf(word_file, output)
            self.status.config(text=f"✓ Saved: {Path(output).name}", fg="green")
            messagebox.showinfo("Success", f"Converted to:\n{output}")
        except Exception as e:
            self.status.config(text="✗ Conversion failed", fg="red")
            messagebox.showerror("Error", str(e))
    
    def image_to_pdf(self, image_files):
        self.status.config(text="Converting Images to PDF...")
        try:
            output = filedialog.asksaveasfilename(defaultextension=".pdf", 
                                                 filetypes=[("PDF files", "*.pdf")])
            if output:
                with open(output, "wb") as f:
                    f.write(img2pdf.convert([str(img) for img in image_files]))
                self.status.config(text=f"✓ Saved: {Path(output).name}", fg="green")
                messagebox.showinfo("Success", f"Converted to:\n{output}")
        except Exception as e:
            self.status.config(text="✗ Conversion failed", fg="red")
            messagebox.showerror("Error", str(e))
    
    def pdf_to_images(self, pdf_file):
        self.status.config(text="Converting PDF to Images...")
        try:
            from pdf2image import convert_from_path
            output_dir = filedialog.askdirectory(title="Select output folder")
            if output_dir:
                images = convert_from_path(pdf_file)
                base_name = Path(pdf_file).stem
                for i, img in enumerate(images):
                    img.save(f"{output_dir}/{base_name}_page_{i+1}.png", "PNG")
                self.status.config(text=f"✓ Saved {len(images)} images", fg="green")
                messagebox.showinfo("Success", f"Converted {len(images)} pages to images")
        except Exception as e:
            self.status.config(text="✗ Conversion failed", fg="red")
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = ConverterApp(root)
    root.mainloop()
