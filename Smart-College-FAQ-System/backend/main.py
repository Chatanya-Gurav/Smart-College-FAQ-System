from fastapi import FastAPI
from pydantic import BaseModel
from pathlib import Path

from hybrid_engine import HybridFAQEngine

from backend.database import (
    initialize_database,
    save_question,
    get_history
)


# ==========================================
# FastAPI Application
# ==========================================

app = FastAPI(
    title="Smart College FAQ API",
    description=(
        "Backend API for the Smart College FAQ System "
        "using hybrid NLP-based FAQ retrieval."
    ),
    version="1.0.0"
)


# ==========================================
# Load NLP Engine
# ==========================================

print("Initializing FAQ system...")

engine = HybridFAQEngine(
    "data/faq_data.csv"
)

initialize_database()

print("FAQ backend ready!")


# ==========================================
# Request Model
# ==========================================

class QuestionRequest(BaseModel):

    question: str


# ==========================================
# Health Check
# ==========================================

@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "service": "Smart College FAQ API"
    }


# ==========================================
# Ask FAQ
# ==========================================

@app.post("/ask")
def ask_question(
    request: QuestionRequest
):

    question = request.question.strip()

    if not question:

        return {
            "found": False,
            "answer": "Please enter a question.",
            "category": "Unknown",
            "confidence": 0.0
        }

    result = engine.find_answer(
        question,
        threshold=0.50
    )

    save_question(
        question=question,
        answer=result["answer"],
        category=result["category"],
        confidence=result["confidence"],
        found=result["found"]
    )

    return {
        "found": result["found"],
        "question": result["question"],
        "answer": result["answer"],
        "category": result["category"],
        "confidence": result["confidence"]
    }


# ==========================================
# Get FAQ Dataset
# ==========================================

@app.get("/faqs")
def get_faqs():

    faq_data = engine.faq_data

    faqs = []

    for _, row in faq_data.iterrows():

        faqs.append(
            {
                "id": int(row["id"]),
                "category": row["category"],
                "question": row["question"],
                "answer": row["answer"]
            }
        )

    return {
        "count": len(faqs),
        "faqs": faqs
    }


# ==========================================
# Get Categories
# ==========================================

@app.get("/categories")
def get_categories():

    categories = sorted(
        engine.faq_data["category"]
        .dropna()
        .unique()
        .tolist()
    )

    return {
        "count": len(categories),
        "categories": categories
    }


# ==========================================
# Get Question History
# ==========================================

@app.get("/history")
def history():

    records = get_history()

    return {
        "count": len(records),
        "history": records
    }