# PDF Document loader for RAG
from pypdf import PdfReader

class PDFLoader:
    def __init__(self):
        pass
    
    def extract_text_from_pdf(self, file_path: str) -> list[str]:
        """Extract text from each page of a PDF file.

        Args:
            file_path: Path to the PDF file.

        Returns:
            A list of strings, one per page.

        Raises:
            RuntimeError: If the PDF cannot be read or parsed.
        """
        try:
            reader = PdfReader(file_path)
            text = []

            # Iterate through each page and extract text
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text.append(page_text)
                else:
                    text.append("")  # Append empty string if page has no text

            return text

        except Exception as e:
            raise RuntimeError(f"Failed to extract text from PDF: {e}") from e

    def get_formatted_string(self, file_path: str) -> str:
        """Extract text and format it with page count and separators.

        Args:
            file_path: Path to the PDF file.

        Returns:
            A formatted string with page separators, or an error message
            if extraction fails.
        """
        try:
            pages = self.extract_text_from_pdf(file_path)
        except RuntimeError as exc:
            return f"Failed to load PDF: {exc}"

        # Build the formatted string
        formatted_output = f"Total Pages: {len(pages)}\n\n"
        for i, page_text in enumerate(pages):
            formatted_output += f"--- Page {i + 1} ---\n"
            formatted_output += f"{page_text.strip()}\n\n"
            
        return formatted_output.strip()