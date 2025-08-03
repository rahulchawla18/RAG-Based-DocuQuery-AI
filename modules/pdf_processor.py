import PyPDF2
import uuid

class SimplePDFProcessor:
    def __init__(self, chunk_size=1000, chunk_overlap=200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def read_pdf(self, pdf_file):
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text

    def create_chunks(self, text, file):
        chunks = []
        start = 0

        while start < len(text):
            end = start + self.chunk_size
            if start > 0:
                start -= self.chunk_overlap
            chunk = text[start:end]

            if end < len(text):
                last_period = chunk.rfind(".")
                if last_period != -1:
                    chunk = chunk[:last_period + 1]
                    end = start + last_period + 1

            chunks.append({
                "id": str(uuid.uuid4()),
                "text": chunk,
                "metadata": {"source": file.name},
            })

            start = end

        return chunks