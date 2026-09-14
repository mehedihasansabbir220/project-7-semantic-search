"""
Document Loader - Load text files from a directory.

A "document" in this context is any text file we want to make searchable.
Documents are loaded as-is before chunking.
"""

import os
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class Document:
    """Represents a loaded document."""
    document_id: str
    filename: str
    text: str
    metadata: Dict = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class DocumentLoader:
    """Load text documents from a directory."""

    def __init__(self, directory: str):
        """
        Initialize the loader.

        Args:
            directory: Path to directory containing .txt files
        """
        self.directory = Path(directory)
        if not self.directory.exists():
            raise ValueError(f"Directory not found: {directory}")

    def load_documents(self) -> List[Document]:
        """
        Load all .txt files from the directory.

        Returns:
            List of Document objects
        """
        documents = []
        txt_files = sorted(self.directory.glob("*.txt"))

        if not txt_files:
            print(f"⚠️  No .txt files found in {self.directory}")
            return documents

        for i, file_path in enumerate(txt_files, 1):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    text = f.read()

                doc_id = f"doc_{i:03d}"
                doc = Document(
                    document_id=doc_id,
                    filename=file_path.name,
                    text=text,
                    metadata={
                        "file_path": str(file_path),
                        "file_size_bytes": file_path.stat().st_size,
                    }
                )
                documents.append(doc)
                print(f"✓ Loaded: {file_path.name} ({len(text)} chars)")

            except Exception as e:
                print(f"✗ Failed to load {file_path.name}: {e}")

        return documents

    def load_single_file(self, filename: str) -> Optional[Document]:
        """
        Load a single file by filename.

        Args:
            filename: Name of the file to load

        Returns:
            Document object or None if not found
        """
        file_path = self.directory / filename

        if not file_path.exists():
            return None

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()

            return Document(
                document_id=f"doc_{filename.replace('.txt', '')}",
                filename=filename,
                text=text,
                metadata={
                    "file_path": str(file_path),
                    "file_size_bytes": file_path.stat().st_size,
                }
            )
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            return None
