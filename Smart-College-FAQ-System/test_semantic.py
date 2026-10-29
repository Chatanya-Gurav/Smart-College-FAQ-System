import pandas as pd

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# ==========================================
# Load FAQ Dataset
# ==========================================

faq_data = pd.read_csv("data/faq_data.csv")


# ==========================================
# Load Sentence Transformer Model
# ==========================================

print("Loading semantic model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Model loaded successfully!")


# ==========================================
# Create FAQ Embeddings
# ==========================================

faq_embeddings = model.encode(
    faq_data["question"].tolist(),
    convert_to_numpy=True
)


# ==========================================
# Test Questions
# ==========================================

questions = [
    "Where can I see examination information?",
    "How do I borrow a library book?",
    "How do I get hostel accommodation?",
    "I want to register for placement",
    "What is the weather today?"
]


# ==========================================
# Semantic Search
# ==========================================

for question in questions:

    print("\n--------------------------------------")

    print("Student Question:")
    print(question)

    # Convert question into embedding
    question_embedding = model.encode(
        [question],
        convert_to_numpy=True
    )

    # Calculate similarity
    scores = cosine_similarity(
        question_embedding,
        faq_embeddings
    )[0]

    # Get top 3 matches
    top_indexes = scores.argsort()[::-1][:3]

    print("\nTop 3 Semantic Matches:")

    for position, index in enumerate(
        top_indexes,
        start=1
    ):

        print(
            f"{position}. "
            f"{faq_data.iloc[index]['question']} "
            f"-> "
            f"{scores[index] * 100:.2f}%"
        )