import pdfplumber
import docx
import pathlib
import os
import mimetypes

def parse_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        return "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])

def parse_docx(file_path):
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def parse_file(path):
    mime, _ = mimetypes.guess_type(path)
    ext = pathlib.Path(path).suffix.lower()

    if mime == "application/pdf" or ext == ".pdf":
        return parse_pdf(path)
    if mime in (
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/msword",
    ) or ext == ".docx":
        return parse_docx(path)

    raise ValueError(f"Unsupported file: {mime or ext}")