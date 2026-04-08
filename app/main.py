from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline
from contextlib import asynccontextmanager

# Global variable to hold the model pipeline
ml_models = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model on startup
    print("Loading summarization model...")
    try:
        # Using a lightweight model (distilbart) for local testing.
        ml_models["summarizer"] = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
        print("Model loaded successfully!")
    except Exception as e:
        print(f"Failed to load model: {e}")
    yield
    # Clean up on shutdown
    ml_models.clear()

app = FastAPI(
    title="News Summarization API",
    description="MLOps Pipeline - Automatic News Article Summarization",
    version="1.0.0",
    lifespan=lifespan
)

class ArticleRequest(BaseModel):
    text: str
    max_length: int = 150
    min_length: int = 30

class SummaryResponse(BaseModel):
    summary: str

@app.get("/")
def read_root():
    return {"status": "ok", "message": "News Summarization API is running."}

@app.get("/health")
def health_check():
    model_status = "loaded" if "summarizer" in ml_models else "not loaded"
    return {"status": "healthy", "model_status": model_status}

@app.post("/summarize", response_model=SummaryResponse)
def summarize_article(request: ArticleRequest):
    summarizer = ml_models.get("summarizer")
    if not summarizer:
        raise HTTPException(status_code=500, detail="ML model is currently unavailable.")
    
    if len(request.text.strip()) < 50:
        raise HTTPException(status_code=400, detail="Article text is too short to summarize. Provide more context.")
        
    try:
        # Generate summary
        result = summarizer(
            request.text, 
            max_length=request.max_length, 
            min_length=request.min_length, 
            do_sample=False
        )
        return SummaryResponse(summary=result[0]['summary_text'])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference error: {str(e)}")
