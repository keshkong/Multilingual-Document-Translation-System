"""Create a Word document containing translated text."""
from pathlib import Path
from docx import Document

def save_translation_docx(translated_text, output_path, title=None, source_file=None):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc = Document()
    if title:
        doc.add_heading(title, level=1)
    if source_file:
        doc.add_paragraph(f"Source file: {source_file}")
    for paragraph in translated_text.splitlines():
        doc.add_paragraph(paragraph)
    doc.save(str(output_path))
    return output_path
