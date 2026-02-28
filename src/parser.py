import pdfplumber
from docx import Document
import os

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None

def parse_pdf(file_path):
    """
    Extract text from a PDF file using pdfplumber with a fallback to PyMuPDF.
    """
    text = ""
    # Try pdfplumber first
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"pdfplumber failed for {file_path}: {e}")

    # If text is still empty, try PyMuPDF
    if not text.strip() and fitz:
        try:
            doc = fitz.open(file_path)
            for page in doc:
                text += page.get_text()
            doc.close()
        except Exception as e:
            print(f"PyMuPDF failed for {file_path}: {e}")
            
    return text

def parse_docx(file_path):
    """
    Extract text from a DOCX file using python-docx.
    """
    text = ""
    try:
        doc = Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        print(f"Error parsing DOCX {file_path}: {e}")
    return text

def parse_resume(file_path):
    """
    Detect file type and parse accordingly.
    """
    _, ext = os.path.splitext(file_path)
    if ext.lower() == '.pdf':
        return parse_pdf(file_path)
    elif ext.lower() in ['.docx', '.doc']:
        return parse_docx(file_path)
    else:
        return ""
