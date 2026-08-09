from pypdf import PdfReader
from docx import Document
from pathlib import Path

class resume_parser:
    @staticmethod
    def extract_file(file_path):
        path = Path(file_path)
        file_extension = path.suffix.lower()
        resume_text = ""

        if file_extension == ".pdf":
            reader = PdfReader(path)
            for i, page in enumerate(reader.pages):
                resume_text += page.extract_text() + "\n"
        elif file_extension == ".docx":
            reader = Document(path)
            for para in reader.paragraphs:
                resume_text += para.text + "\n"
        else:
            print(f"Unsupported file format: {file_extension}")

        return resume_text