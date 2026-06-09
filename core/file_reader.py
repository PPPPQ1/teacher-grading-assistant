from __future__ import annotations

from io import BytesIO
from pathlib import Path
from typing import BinaryIO

from docx import Document
from pypdf import PdfReader


def read_uploaded_file(uploaded_file: BinaryIO) -> str:
    filename = getattr(uploaded_file, "name", "")
    suffix = Path(filename).suffix.lower()
    file_bytes = uploaded_file.getvalue()

    if suffix == ".txt":
        return read_txt(file_bytes)
    if suffix == ".docx":
        return read_docx(file_bytes)
    if suffix == ".pdf":
        return read_pdf(file_bytes)

    raise ValueError("仅支持 txt、docx、pdf 文件。")


def read_txt(file_bytes: bytes) -> str:
    for encoding in ("utf-8", "utf-8-sig", "gb18030"):
        try:
            return file_bytes.decode(encoding)
        except UnicodeDecodeError:
            continue
    raise ValueError("文本编码无法识别，请转换为 UTF-8 后重试。")


def read_docx(file_bytes: bytes) -> str:
    document = Document(BytesIO(file_bytes))
    paragraphs = [paragraph.text.strip() for paragraph in document.paragraphs if paragraph.text.strip()]
    return "\n".join(paragraphs)


def read_pdf(file_bytes: bytes) -> str:
    reader = PdfReader(BytesIO(file_bytes))
    pages = []
    for page in reader.pages:
        text = page.extract_text() or ""
        if text.strip():
            pages.append(text.strip())
    return "\n\n".join(pages)
