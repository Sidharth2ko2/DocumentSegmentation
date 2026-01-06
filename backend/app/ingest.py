from PyPDF2 import PdfReader
import io
from app.db import cur, conn

async def read_file(file):
    # Read the raw binary content
    content = await file.read()
    
    if file.filename.lower().endswith('.pdf'):
        try:
            # Wrap binary content in a BytesIO stream for the PDF reader
            pdf_file = io.BytesIO(content)
            reader = PdfReader(pdf_file)
            text = ""
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted
            return text
        except Exception as e:
            print(f"PDF extraction error: {e}")
            return ""
    
    # If it's not a PDF, try to decode it as a normal text file
    try:
        return content.decode('utf-8')
    except UnicodeDecodeError:
        # Fallback for files with different encoding (like Windows-1252)
        return content.decode('latin-1')

def save_doc(name, text, label, confidence):
    cur.execute(
        "INSERT INTO documents (name, text, label, confidence) VALUES (?, ?, ?, ?)",
        (name, text, label, confidence)
    )
    conn.commit()