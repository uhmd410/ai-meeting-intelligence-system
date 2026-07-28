import io
from docx import Document
from fastapi import UploadFile, HTTPException

ALLOWED_EXTENSIONS = {".txt", ".docx"}

def extract_text_from_upload(file: UploadFile, raw_bytes: bytes) -> str:
    filename = file.filename or ""
    ext = "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ""

    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{ext}'. Only .txt and .docx are allowed."
        )

    if ext == ".txt":
        try:
            return raw_bytes.decode("utf-8")
        except UnicodeDecodeError:
            raise HTTPException(status_code=400, detail="Could not decode .txt file as UTF-8.")

    if ext == ".docx":
        try:
            doc = Document(io.BytesIO(raw_bytes))
            paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
            return "\n".join(paragraphs)
        except Exception:
            raise HTTPException(status_code=400, detail="Could not parse .docx file. Is it a valid Word document?")