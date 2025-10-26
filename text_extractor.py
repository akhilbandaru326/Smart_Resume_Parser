# text_extractor.py
import fitz # PyMuPDF
from docx import Document

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file using PyMuPDF."""
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        return f"Error reading PDF: {e}"

def extract_text_from_docx(docx_path):
    """Extracts text from a DOCX file using python-docx."""
    try:
        document = Document(docx_path)
        text = '\n'.join([paragraph.text for paragraph in document.paragraphs])
        return text
    except Exception as e:
        return f"Error reading DOCX: {e}"

def extract_text(file_path, file_extension):
    """Calls the appropriate extractor based on file type."""
    file_extension = file_extension.lower()
    if file_extension == 'pdf':
        return extract_text_from_pdf(file_path)
    elif file_extension == 'docx':
        return extract_text_from_docx(file_path)
    else:
        return "Unsupported file type."