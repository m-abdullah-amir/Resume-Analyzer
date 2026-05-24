"""
resume_parser.py — Extracts clean text from PDF and DOCX resume files.
Handles edge cases like scanned PDFs and empty documents.
"""

import io
import pdfplumber
from docx import Document


def extract_text(uploaded_file) -> str:
    """
    Extract text from an uploaded PDF or DOCX file.
    
    Args:
        uploaded_file: Streamlit UploadedFile object
        
    Returns:
        Cleaned text string, or an error message if extraction fails.
    """
    filename = uploaded_file.name.lower()

    if filename.endswith(".pdf"):
        return _extract_from_pdf(uploaded_file)
    elif filename.endswith(".docx"):
        return _extract_from_docx(uploaded_file)
    else:
        return "❌ Unsupported file format. Please upload a PDF or DOCX file."


def _extract_from_pdf(uploaded_file) -> str:
    """Extract text from a PDF file using pdfplumber."""
    try:
        text_parts = []
        with pdfplumber.open(io.BytesIO(uploaded_file.read())) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
        
        # Reset file pointer for potential re-reads
        uploaded_file.seek(0)

        if not text_parts:
            return (
                "❌ This PDF appears to be scanned or image-based. "
                "No readable text was found. Please upload a text-based PDF, "
                "or copy-paste your resume text into a DOCX file."
            )

        return _clean_text("\n".join(text_parts))

    except Exception as e:
        uploaded_file.seek(0)
        return f"❌ Error reading PDF: {str(e)}"


def _extract_from_docx(uploaded_file) -> str:
    """Extract text from a DOCX file using python-docx."""
    try:
        doc = Document(io.BytesIO(uploaded_file.read()))
        text_parts = [para.text for para in doc.paragraphs if para.text.strip()]
        
        # Reset file pointer for potential re-reads
        uploaded_file.seek(0)

        if not text_parts:
            return "❌ The DOCX file appears to be empty. Please upload a resume with content."

        return _clean_text("\n".join(text_parts))

    except Exception as e:
        uploaded_file.seek(0)
        return f"❌ Error reading DOCX: {str(e)}"


def _clean_text(text: str) -> str:
    """Remove excessive whitespace and blank lines from extracted text."""
    # Replace multiple newlines with a single newline
    lines = [line.strip() for line in text.splitlines()]
    # Remove empty lines but keep single line breaks for structure
    cleaned_lines = []
    prev_empty = False
    for line in lines:
        if not line:
            if not prev_empty:
                cleaned_lines.append("")
                prev_empty = True
        else:
            cleaned_lines.append(line)
            prev_empty = False
    
    return "\n".join(cleaned_lines).strip()
