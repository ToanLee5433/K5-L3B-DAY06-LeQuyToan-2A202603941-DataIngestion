"""Implement fixed-size and structure-aware chunking."""
from typing import Union
from .models import Chunk, DocumentPage


def fixed_size(page_or_pages: Union[DocumentPage, list[DocumentPage]], size: int = 500, overlap: int = 50) -> list[Chunk]:
    """Split text into overlapping character windows and retain full page metadata."""
    if isinstance(page_or_pages, list):
        all_chunks = []
        for p in page_or_pages:
            all_chunks.extend(fixed_size(p, size=size, overlap=overlap))
        return all_chunks

    page = page_or_pages
    text = page.text
    if not text:
        return []

    chunks = []
    step = max(size - overlap, 1)
    chunk_idx = 0

    for start in range(0, len(text), step):
        end = min(start + size, len(text))
        chunk_text = text[start:end].strip()
        if chunk_text:
            chunk_id = f"{page.document_id}_p{page.page}_fix_{chunk_idx:03d}"
            chunks.append(
                Chunk(
                    chunk_id=chunk_id,
                    document_id=page.document_id,
                    source=page.source,
                    page=page.page,
                    text=chunk_text,
                    metadata=dict(page.metadata, start_char=start, end_char=end, chunking="fixed_size")
                )
            )
            chunk_idx += 1
        if end >= len(text):
            break

    return chunks


def by_paragraph(page_or_pages: Union[DocumentPage, list[DocumentPage]], max_size: int = 1000) -> list[Chunk]:
    """Group coherent paragraphs together without exceeding max_size, keeping structure intact."""
    if isinstance(page_or_pages, list):
        all_chunks = []
        for p in page_or_pages:
            all_chunks.extend(by_paragraph(p, max_size=max_size))
        return all_chunks

    page = page_or_pages
    raw_paras = page.text.split("\n\n")
    paragraphs = [p.strip() for p in raw_paras if p.strip()]
    if not paragraphs:
        return []

    chunks = []
    chunk_idx = 0
    current_group = []
    current_len = 0

    for para in paragraphs:
        para_len = len(para)
        # If adding this paragraph exceeds max_size and we already have content
        if current_group and (current_len + para_len + 2 > max_size):
            chunk_text = "\n\n".join(current_group)
            chunk_id = f"{page.document_id}_p{page.page}_para_{chunk_idx:03d}"
            chunks.append(
                Chunk(
                    chunk_id=chunk_id,
                    document_id=page.document_id,
                    source=page.source,
                    page=page.page,
                    text=chunk_text,
                    metadata=dict(page.metadata, chunking="by_paragraph")
                )
            )
            chunk_idx += 1
            current_group = [para]
            current_len = para_len
        else:
            current_group.append(para)
            current_len += para_len + (2 if current_group else 0)

    # Flush remaining group
    if current_group:
        chunk_text = "\n\n".join(current_group)
        chunk_id = f"{page.document_id}_p{page.page}_para_{chunk_idx:03d}"
        chunks.append(
            Chunk(
                chunk_id=chunk_id,
                document_id=page.document_id,
                source=page.source,
                page=page.page,
                text=chunk_text,
                metadata=dict(page.metadata, chunking="by_paragraph")
            )
        )

    return chunks

