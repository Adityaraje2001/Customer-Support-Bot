"""
Test script for the IngestionPipeline.

Usage:
    cd backend/
    python -m scripts.test_ingestion_pipeline

    Or directly:
    python backend/scripts/test_ingestion_pipeline.py

The script:
  1. Instantiates PDFLoader, TextSplitter, EmbeddingService, and ChromaStore.
  2. Creates an IngestionPipeline with those services.
  3. Runs ``ingest_pdf`` on a sample PDF.
  4. Prints the ingestion summary.
  5. Verifies that chunks were actually written to ChromaDB.
"""

from __future__ import annotations

import logging
import os
import sys

# ---------------------------------------------------------------------------
# Ensure the project root (backend/) is on sys.path so that imports work
# regardless of where the script is invoked from.
# ---------------------------------------------------------------------------
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_BACKEND_DIR = os.path.dirname(_SCRIPT_DIR)
_PROJECT_ROOT = os.path.dirname(_BACKEND_DIR)

for _path in (_PROJECT_ROOT, _BACKEND_DIR):
    if _path not in sys.path:
        sys.path.insert(0, _path)

# ---------------------------------------------------------------------------
# Application imports
# ---------------------------------------------------------------------------
from backend.app.ingestion.pdf_loader import PDFLoader          # noqa: E402
from backend.app.ingestion.text_splitter import TextSplitter      # noqa: E402
from backend.app.rag.embeddings import EmbeddingService            # noqa: E402
from backend.app.rag.vectorstores.chroma_store import ChromaStore  # noqa: E402
from backend.app.pipelines.ingestion_pipeline import IngestionPipeline  # noqa: E402

# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s — %(message)s",
)
logger = logging.getLogger(__name__)


def main() -> None:
    """Run the ingestion pipeline test."""

    # ---- Resolve a sample PDF path --------------------------------------
    # Look for a PDF in a few common locations relative to the project root.
    candidate_paths = [
        os.path.join(_PROJECT_ROOT, "data", "sample.pdf"),
        os.path.join(_PROJECT_ROOT, "tests", "fixtures", "sample.pdf"),
        os.path.join(_PROJECT_ROOT, "docs", "sample.pdf"),
        os.path.join(_BACKEND_DIR, "data", "sample.pdf"),
    ]

    pdf_path: str | None = None
    for path in candidate_paths:
        if os.path.isfile(path):
            pdf_path = path
            break

    if pdf_path is None:
        # Fall back to a user-supplied argument or a default placeholder
        if len(sys.argv) > 1:
            pdf_path = sys.argv[1]
        else:
            print(
                "\n⚠  No sample PDF found automatically.\n"
                "   Please supply the path as a CLI argument:\n\n"
                "   python backend/scripts/test_ingestion_pipeline.py "
                "<path_to_test_pdf.pdf>\n"
            )
            sys.exit(1)

    logger.info("Using PDF: %s", pdf_path)

    # ---- 1. Instantiate services ----------------------------------------
    pdf_loader = PDFLoader()
    text_splitter = TextSplitter()
    embedding_service = EmbeddingService()
    vectorstore = ChromaStore()

    # ---- 2. Instantiate the pipeline ------------------------------------
    pipeline = IngestionPipeline(
        pdf_loader=pdf_loader,
        text_splitter=text_splitter,
        embedding_service=embedding_service,
        vectorstore=vectorstore,
    )

    # ---- 3. Run ingestion -----------------------------------------------
    document_id = os.path.splitext(os.path.basename(pdf_path))[0]
    logger.info("Starting ingestion with document_id='%s' …", document_id)

    try:
        summary = pipeline.ingest_pdf(
            pdf_path=pdf_path,
            document_id=document_id,
        )
    except Exception as exc:
        logger.exception("Ingestion failed: %s", exc)
        sys.exit(1)

    # ---- 4. Print summary -----------------------------------------------
    print("\n" + "=" * 60)
    print("  INGESTION SUMMARY")
    print("=" * 60)
    for key, value in summary.items():
        print(f"  {key:>20s} : {value}")
    print("=" * 60 + "\n")

    # ---- 5. Verify chunks in ChromaDB -----------------------------------
    collection_count = vectorstore.collection.count()
    logger.info(
        "ChromaDB collection '%s' now contains %d document(s).",
        vectorstore.collection.name,
        collection_count,
    )

    if collection_count > 0 and summary["chunks_created"] > 0:
        print("✅  Verification PASSED — chunks successfully stored in ChromaDB.")
    elif summary["chunks_created"] == 0:
        print(
            "⚠  No chunks were created. The PDF might be empty or the text "
            "splitter produced no chunks."
        )
    else:
        print("❌  Verification FAILED — expected chunks in ChromaDB but found none.")
        sys.exit(1)

    # Quick peek: retrieve the first stored chunk for sanity check
    sample = vectorstore.collection.peek(limit=1)
    if sample and sample.get("documents"):
        print(f"\n📄  Sample stored chunk (first 200 chars):\n"
              f"    {sample['documents'][0][:200]}…\n")


if __name__ == "__main__":
    main()
