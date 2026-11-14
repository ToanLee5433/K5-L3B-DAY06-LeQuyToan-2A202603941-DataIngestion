"""Read and normalize source data."""
import unicodedata
from pathlib import Path
import pypdf
from .models import DocumentPage


def get_section_from_page(page_num: int) -> str:
    """Map physical page number to logical document section."""
    if 3 <= page_num <= 6:
        return "admissions"
    elif 7 <= page_num <= 10:
        return "course_registration"
    elif 11 <= page_num <= 14:
        return "attendance_leave"
    elif 15 <= page_num <= 18:
        return "grading_gpa"
    elif 19 <= page_num <= 22:
        return "academic_standing"
    elif 23 <= page_num <= 26:
        return "academic_integrity"
    elif 27 <= page_num <= 30:
        return "graduation_honors"
    elif 31 <= page_num <= 35:
        return "tuition_scholarships"
    return "other"


def normalize_text(text: str) -> str:
    """Normalize Unicode and whitespace while preserving substantive structure."""
    if not text:
        return ""
    # NFC Unicode normalization
    text = unicodedata.normalize("NFC", text)
    # Normalize multiple newlines and carriage returns
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    # Clean whitespace per line but preserve paragraph breaks
    paragraphs = []
    for para in text.split("\n\n"):
        clean_para = " ".join(para.split())
        if clean_para:
            paragraphs.append(clean_para)
    return "\n\n".join(paragraphs)


def load_pdf(path: Path, document_id: str, source: str) -> list[DocumentPage]:
    """Extract each physical page; keep page number, section metadata, and filter non-content pages."""
    reader = pypdf.PdfReader(str(path))
    pages = []
    empty_pages = []

    for i, page in enumerate(reader.pages, 1):
        raw_text = page.extract_text() or ""
        norm_text = normalize_text(raw_text)

        # Content pages are pages 3 through 35 (pages 1, 2, 36 are cover, TOC, appendix)
        is_content = (3 <= i <= 35) and len(norm_text) > 0
        if not norm_text:
            empty_pages.append(i)

        if is_content:
            section = get_section_from_page(i)
            pages.append(
                DocumentPage(
                    document_id=document_id,
                    source=source,
                    page=i,
                    text=norm_text,
                    metadata={
                        "section": section,
                        "document_type": "handbook",
                        "year": 2025,
                        "audience": "undergraduate",
                        "language": "en"
                    }
                )
            )

    return pages
