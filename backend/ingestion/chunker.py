"""
Document Chunker - Split documents into smaller, embeddable chunks.

WHY DO WE CHUNK?
===============
Embedding models have input token limits (usually 512-2048 tokens).
Large documents often exceed this limit, so we split them into smaller pieces.

Example:
  • Document: 10,000 tokens (too large to embed as one)
  • Chunk size: 300 tokens
  • Result: ~33 chunks, each embeddable

Each chunk gets a unique ID and can be searched independently.
When a query matches a chunk, we retrieve the original document.

CHUNKING STRATEGIES:
===================
1. Fixed-size chunks: Split at token/character count (simple, predictable)
2. Sentence-based: Split on sentence boundaries (more semantic)
3. Paragraph-based: Split on paragraphs (respects document structure)

For this project, we use FIXED-SIZE with optional OVERLAP.

OVERLAP EXPLANATION:
===================
Without overlap: Chunks 1, 2, 3, ... may split important context.
With overlap: Chunk 1 (0-300), Chunk 2 (250-550), Chunk 3 (500-800)
             This keeps context from being split across boundaries.

Example:
  Text: "The cat sat on the mat. The dog barked loudly. The bird flew away."

  No overlap (chunk_size=20):
    Chunk 0: "The cat sat on the "
    Chunk 1: "mat. The dog barked "
    Chunk 2: "loudly. The bird fle"
    Problem: Sentence boundaries are split

  With overlap (chunk_size=20, overlap=10):
    Chunk 0: "The cat sat on the "
    Chunk 1: "on the mat. The dog "
    Chunk 2: "g barked loudly. The"
    Better: More context preserved at boundaries
"""

from dataclasses import dataclass
from typing import List, Dict
import uuid


@dataclass
class Chunk:
    """Represents a chunk of a document."""
    chunk_id: str
    document_id: str
    text: str
    start_position: int
    end_position: int
    chunk_index: int
    metadata: Dict = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class DocumentChunker:
    """Split documents into chunks."""

    def __init__(self, chunk_size: int = 300, overlap: int = 0):
        """
        Initialize the chunker.

        Args:
            chunk_size: Number of characters per chunk
            overlap: Number of overlapping characters between chunks
        """
        if chunk_size <= 0:
            raise ValueError("chunk_size must be > 0")
        if overlap < 0:
            raise ValueError("overlap must be >= 0")
        if overlap >= chunk_size:
            raise ValueError("overlap must be < chunk_size")

        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_document(self, document) -> List[Chunk]:
        """
        Split a document into chunks.

        Args:
            document: Document object from loader

        Returns:
            List of Chunk objects
        """
        text = document.text
        chunks = []

        # Calculate step size (how many chars to move forward for next chunk)
        step_size = self.chunk_size - self.overlap

        position = 0
        chunk_index = 0

        while position < len(text):
            # Get chunk text
            chunk_end = min(position + self.chunk_size, len(text))
            chunk_text = text[position:chunk_end]

            # Create chunk
            chunk = Chunk(
                chunk_id=f"{document.document_id}_chunk_{chunk_index:04d}",
                document_id=document.document_id,
                text=chunk_text,
                start_position=position,
                end_position=chunk_end,
                chunk_index=chunk_index,
                metadata={
                    "filename": document.metadata.get("filename", ""),
                    "chunk_size": len(chunk_text),
                    "char_range": f"{position}-{chunk_end}",
                }
            )

            chunks.append(chunk)

            # Move to next chunk position
            position += step_size
            chunk_index += 1

            # Stop if we've reached the end
            if chunk_end >= len(text):
                break

        return chunks

    def chunk_documents(self, documents: List) -> List[Chunk]:
        """
        Split multiple documents into chunks.

        Args:
            documents: List of Document objects

        Returns:
            Flat list of all Chunk objects
        """
        all_chunks = []

        for doc in documents:
            chunks = self.chunk_document(doc)
            all_chunks.extend(chunks)

        return all_chunks


def print_chunk_stats(chunks: List[Chunk]):
    """Print statistics about chunks."""
    if not chunks:
        print("No chunks to analyze")
        return

    total_chars = sum(len(c.text) for c in chunks)
    avg_size = total_chars / len(chunks) if chunks else 0

    print("\n" + "=" * 100)
    print("CHUNK STATISTICS")
    print("=" * 100)
    print(f"Total chunks: {len(chunks)}")
    print(f"Total characters: {total_chars:,}")
    print(f"Average chunk size: {avg_size:.1f} chars")
    print(f"Min chunk size: {min(len(c.text) for c in chunks)} chars")
    print(f"Max chunk size: {max(len(c.text) for c in chunks)} chars")

    # Group by document
    docs = {}
    for chunk in chunks:
        doc_id = chunk.document_id
        if doc_id not in docs:
            docs[doc_id] = 0
        docs[doc_id] += 1

    print(f"\nChunks per document:")
    for doc_id in sorted(docs.keys()):
        print(f"  {doc_id}: {docs[doc_id]} chunks")

    print("=" * 100 + "\n")
