import os
import docx
import PyPDF2

def extract_text_from_document(file_path):
    """Extract text from various document formats"""
    _, file_extension = os.path.splitext(file_path)
    
    if file_extension.lower() == '.txt':
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    
    elif file_extension.lower() == '.docx':
        doc = docx.Document(file_path)
        return ' '.join([paragraph.text for paragraph in doc.paragraphs])
    
    elif file_extension.lower() == '.pdf':
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page_num in range(len(pdf_reader.pages)):
                text += pdf_reader.pages[page_num].extract_text()
        return text
    
    else:
        return ""