"""
Ingestion Pipeline for the Customer Support RAG Agent.

Orchestrates the end-to-end document ingestion flow:
  PDF → Page Extraction → Text Chunking → Embedding → Vector Store

This module follows dependency-injection principles — every external service
is received through the constructor, making the pipeline easy to test and
swap implementations.
"""

from __future__ import annotations

import logging
import os
from typing import Any

from app.ingestion.pdf_loader import PDFLoader
from app.ingestion.text_splitter import TextSplitter
from app.rag.embeddings import EmbeddingService
from app.rag.vectorstores.chroma_store import ChromaStore

logger = logging.getLogger(__name__)


class IngestionPipeline:
    """Pipeline that ingests a PDF document into the ChromaDB vector store.

    The pipeline performs the following steps for each PDF:
      1. Extract raw text from every page.
      2. Split each page's text into semantically meaningful chunks.
      3. Generate dense vector embeddings for every chunk.
      4. Persist each chunk — along with its embedding and metadata — in ChromaDB.

    Attributes:
        pdf_loader:        Service responsible for PDF text extraction.
        text_splitter:     Service responsible for chunking text.
        embedding_service: Service responsible for generating embeddings.
        vectorstore:       ChromaDB-backed store for persisting chunks.
    """

    def __init__(
        self,
        pdf_loader: PDFLoader,
        text_splitter: TextSplitter,
        embedding_service: EmbeddingService,
        vectorstore: ChromaStore,
    ) -> None:
        """Initialise the pipeline with all required services.

        Args:
            pdf_loader:        Instance of :class:`PDFLoader`.
            text_splitter:     Instance of :class:`TextSplitter`.
            embedding_service: Instance of :class:`EmbeddingService`.
            vectorstore:       Instance of :class:`ChromaStore`.
        """
        self.pdf_loader = pdf_loader
        self.text_splitter = text_splitter
        self.embedding_service = embedding_service
        self.vectorstore = vectorstore

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def ingest_pdf(
        self,
        pdf_path: str,
        document_id: str | None = None,
        user_id: int | None = None,
    ) -> dict[str, Any]:
        """Ingest a single PDF document into the vector store.

        Args:
            pdf_path:    Absolute or relative filesystem path to the PDF file.
            document_id: Optional human-readable identifier for the document.
                         When *None*, the PDF filename (without extension) is
                         used automatically — e.g. ``"employee_handbook.pdf"``
                         becomes ``"employee_handbook"``.

        Returns:
            A summary dictionary with the following keys:

            - ``document_id``      – identifier used for every chunk.
            - ``source_file``      – original PDF filename.
            - ``pages_processed``  – number of pages extracted.
            - ``chunks_created``   – total number of chunks stored.
            - ``status``           – ``"success"`` when the pipeline completes.

        Raises:
            FileNotFoundError: If *pdf_path* does not point to an existing file.
            RuntimeError:      If PDF extraction, text splitting, embedding
                               generation, or vector-store insertion fails.
        """

        # --- Pre-flight checks -------------------------------------------
        if not os.path.isfile(pdf_path):
            logger.error("PDF file not found: %s", pdf_path)
            raise FileNotFoundError(
                f"The specified PDF file does not exist: {pdf_path}"
            )

        if document_id is None:
            document_id = os.path.splitext(
                os.path.basename(pdf_path)
            )[0]
            logger.info(
                "No document_id supplied — derived from filename: %s",
                document_id,
            )

        source_file: str = os.path.basename(pdf_path)

        logger.info(
            "Starting ingestion for document '%s' from '%s'",
            document_id,
            pdf_path,
        )

        # --- Step 1: Extract pages ----------------------------------------
        try:
            pages: list[str] = self.pdf_loader.extract_text_from_pdf(pdf_path)
        except Exception as exc:
            logger.error("PDF extraction failed for '%s': %s", pdf_path, exc)
            raise RuntimeError(
                f"PDF extraction failed for '{pdf_path}': {exc}"
            ) from exc

        total_pages: int = len(pages)
        total_chunks: int = 0

        logger.info("Extracted %d page(s) from '%s'", total_pages, pdf_path)

        # --- Step 2–4: Process each page ----------------------------------
        for page_number, page_text in enumerate(pages, start=1):
            if not page_text.strip():
                logger.debug(
                    "Skipping empty page %d of document '%s'",
                    page_number,
                    document_id,
                )
                continue

            # Step 2: Chunk the page text
            try:
                chunks: list[str] = self.text_splitter.split_text(page_text)
            except Exception as exc:
                logger.warning(
                    "Text splitting failed on page %d of document '%s': %s",
                    page_number,
                    document_id,
                    exc,
                )
                continue

            for chunk_number, chunk in enumerate(chunks, start=1):
                # Step 3: Generate embedding
                try:
                    embedding = self.embedding_service.embed_text(chunk)
                except Exception as exc:
                    logger.error(
                        "Embedding generation failed for "
                        "document '%s', page %d, chunk %d: %s",
                        document_id,
                        page_number,
                        chunk_number,
                        exc,
                    )
                    raise RuntimeError(
                        f"Embedding generation failed on page {page_number}, "
                        f"chunk {chunk_number}: {exc}"
                    ) from exc

                # EmbeddingService may return an empty list on failure
                if isinstance(embedding, (list,)) and len(embedding) == 0:
                    logger.error(
                        "Received empty embedding for document '%s', "
                        "page %d, chunk %d — skipping chunk.",
                        document_id,
                        page_number,
                        chunk_number,
                    )
                    raise RuntimeError(
                        f"Empty embedding returned for page {page_number}, "
                        f"chunk {chunk_number}. The embedding model may have "
                        f"failed silently."
                    )

                # Convert array-like embeddings → plain Python list for ChromaDB
                if hasattr(embedding, "tolist"):
                    embedding = embedding.tolist()

                # Step 4a: Build unique chunk ID
                chunk_id: str = (
                    f"{document_id}_page_{page_number}_chunk_{chunk_number}"
                )

                # Step 4b: Persist to vector store
                metadata: dict[str, Any] = {
                    "source": source_file,
                    "document_id": document_id,
                    "page": page_number,
                    "chunk": chunk_number,
                }

                if user_id is not None:
                    metadata["user_id"] = user_id

                try:
                    self.vectorstore.add(
                        id=chunk_id,
                        text=chunk,
                        embedding=embedding,
                        metadata=metadata,
                    )
                except Exception as exc:
                    logger.error(
                        "ChromaDB insertion failed for chunk '%s': %s",
                        chunk_id,
                        exc,
                    )
                    raise RuntimeError(
                        f"Vector store insertion failed for chunk "
                        f"'{chunk_id}': {exc}"
                    ) from exc

                total_chunks += 1
                logger.debug("Stored chunk '%s'", chunk_id)

        # --- Build summary ------------------------------------------------
        summary: dict[str, Any] = {
            "document_id": document_id,
            "source_file": source_file,
            "pages_processed": total_pages,
            "chunks_created": total_chunks,
            "status": "success",
        }

        logger.info(
            "Ingestion complete for '%s' — %d page(s), %d chunk(s)",
            document_id,
            total_pages,
            total_chunks,
        )

        return summary
