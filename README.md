# MLOps News Summarizer API

This is a local FastAPI-based API server that uses Hugging Face's `transformers` library to automate news article summarization.

## Setup and Run

1. Open your terminal and navigate to this folder.
2. Create a virtual environment:
   `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `.\venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
4. Install dependencies:
   `pip install -r requirements.txt`
5. Run the server:
   `uvicorn app.main:app --reload`
6. View the API documentation at: http://127.0.0.1:8000/docs
