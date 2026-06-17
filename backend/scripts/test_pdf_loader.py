import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.ingestion import pdf_loader

loader = pdf_loader.PDFLoader()
file_path = "storage/uploads/NIPS-2017-attention-is-all-you-need-Paper_deeae239-18b3-432a-9bf1-1190ec8229e7.pdf"

# Print the cleanly formatted output
print(loader.get_formatted_string(file_path))