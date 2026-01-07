DocSegment AI (Classification & Search)
**Focus:** Deep Learning (DistilBERT) and Semantic Discovery.

```markdown
# 📂 DocSegment AI: Intelligent Document Management

An enterprise-grade tool for automatic document classification and semantic discovery. This project uses a fine-tuned **DistilBERT** model to categorize files and a vector-search layer for finding documents based on meaning rather than keywords.

## The "Double-Brain" Architecture
1. **The Classifier (DistilBERT):** A deep learning model with 6 Transformer layers, fine-tuned on synthetic data to recognize 7 document categories (Reports, Emails, Invoices, etc.).
2. **The Search Engine (Nomic):** Uses **Mean Vector Embeddings** to create a "semantic fingerprint" for every file, enabling discovery through the search bar.

## Features
- **Batch Processing:** Upload multiple PDFs/TXTs simultaneously.
- **Real-time Confidence:** Visual "Glow Bars" show the model's certainty for each classification.
- **Semantic Search:** Find documents by searching for concepts (e.g., searching "money" finds "Invoices").
- **Synthetic Data Pipeline:** Includes a script to generate custom training data via Ollama.

## Tech Stack
- **Models:** DistilBERT (Hugging Face), Nomic-Embed-Text.
- **Database:** SQLite (Metadata), ChromaDB (Vector Store).
- **API:** FastAPI (Python).
- **UI:** React 18, Framer Motion (Animations).

## Quick Start
```bash
# Run the Backend
cd backend
python -m uvicorn app.main:app --reload --port 8001

# Run the Frontend
cd frontend
npm run dev
