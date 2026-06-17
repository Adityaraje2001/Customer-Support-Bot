# Document chunking for RAG ingestion
# TODO: Implement RecursiveCharacterTextSplitter with optimized chunk size and overlap.
class TextSplitter:
    def __init__(self):
        self.chunk_size = 4
        self.overlap = 1 
    def split_text(self, text: str) -> list[str]:
        """Split *text* into overlapping chunks of sentences.

        Args:
            text: The raw text to split.

        Returns:
            A list of chunk strings.

        Raises:
            RuntimeError: If splitting fails for any reason.
        """
        try:
            sentences = [
                s.strip()
                for s in text.split(".")
                if s.strip()
            ]

            chunks = []
            for i in range(
                0,
                len(sentences),
                self.chunk_size - self.overlap
            ):
                chunk = sentences[i:i+self.chunk_size]

                if len(chunk) < 2:
                    continue

                chunks.append(". ".join(chunk))
            return chunks
        except Exception as e:
            raise RuntimeError(f"Text splitting failed: {e}") from e


text_splitter = TextSplitter()
print(text_splitter.split_text("Refunds are allowed within 30 days. The request must include proof of purchase. Business customers are exempt. Support can be contacted by email."))