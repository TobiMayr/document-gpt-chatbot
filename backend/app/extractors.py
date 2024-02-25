import os

import fitz
import pytesseract
from PIL import Image
from docx import Document
import io

from app.config import DOCUMENT_LANGUAGES


def extract_text(path):
    extension = os.path.splitext(path)[1]
    if extension == '.pdf':
        return extract_text_from_pdf(path)
    elif extension == '.docx':
        return extract_text_from_docx(path)
    elif extension in ['.jpg']:
        return extract_text_from_image(path)
    else:
        return open(path, "r").read()


def extract_text_from_pdf(pdf_path):
    text = ''

    with fitz.open(pdf_path) as pdf:
        for page_num in range(len(pdf)):
            page = pdf[page_num]
            text += page.get_text()

            for image_index, img in enumerate(page.get_images(full=True)):
                xref = img[0]
                base_image = pdf.extract_image(xref)
                image_bytes = base_image['image']

                image_text = extract_text_from_image_bytes(image_bytes)
                text += image_text

    return text


def extract_text_from_docx(docx_path):
    doc = Document(docx_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    for rel in doc.part.rels.values():
        if "image" in rel.reltype:
            image_bytes = rel.target_part.blob
            image_text = extract_text_from_image_bytes(image_bytes)
            full_text.append(image_text)

    return '\n'.join(full_text)


def extract_text_from_image(image_path):
    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()
        return extract_text_from_image_bytes(image_bytes)


def extract_text_from_image_bytes(image_bytes):
    image_stream = io.BytesIO(image_bytes)
    image_obj = Image.open(image_stream)
    return pytesseract.image_to_string(image_obj, lang=DOCUMENT_LANGUAGES)
