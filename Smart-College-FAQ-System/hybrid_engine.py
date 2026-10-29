import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from sentence_transformers import SentenceTransformer

from preprocessing import preprocess_text


class HybridFAQEngine:

    def __init__(self, dataset_path):

        # Load FAQ dataset
        self.faq_data = pd.read_csv(dataset_path)

        # Preprocess FAQ questions
        self.faq_data["processed_question"] = (
            self.faq_data["question"]
            .apply(preprocess_text)
        )

        # --------------------------------
        # TF-IDF Model
        # --------------------------------
        self.tfidf_vectorizer = TfidfVectorizer()

        self.tfidf_vectors = (
            self.tfidf_vectorizer.fit_transform(
                self.faq_data["processed_question"]
            )
        )

        # --------------------------------
        # Semantic Model
        # --------------------------------
        print("Loading semantic model...")

        self.semantic_model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        print("Semantic model loaded!")

        # Create semantic embeddings
        self.semantic_embeddings = (
            self.semantic_model.encode(
                self.faq_data["question"].tolist(),
                convert_to_numpy=True
            )
        )

    def calculate_intent_boost(
        self,
        user_question,
        faq_question
    ):
        """
        Give a small score boost when important
        intent words appear in both questions.
        """

        user_words = set(
            preprocess_text(user_question).split()
        )

        faq_words = set(
            preprocess_text(faq_question).split()
        )

        # Important intent words
        intent_words = {
            "apply",
            "application",
            "admission",
            "register",
            "registration",
            "issue",
            "borrow",
            "payment",
            "pay",
            "schedule",
            "requirement",
            "information",
            "notice",
            "accommodation",
            "hostel",
            "scholarship",
            "placement",
            "attendance"
        }

        common_intent_words = (
            user_words
            & faq_words
            & intent_words
        )

        # Small boost
        if common_intent_words:
            return 0.05

        return 0.0

    def find_answer(
        self,
        user_question,
        threshold=0.50
    ):

        # --------------------------------
        # Preprocess user question
        # --------------------------------
        processed_question = preprocess_text(
            user_question
        )

        # --------------------------------
        # TF-IDF Similarity
        # --------------------------------
        question_tfidf = (
            self.tfidf_vectorizer.transform(
                [processed_question]
            )
        )

        tfidf_scores = cosine_similarity(
            question_tfidf,
            self.tfidf_vectors
        )[0]

        # --------------------------------
        # Semantic Similarity
        # --------------------------------
        question_embedding = (
            self.semantic_model.encode(
                [user_question],
                convert_to_numpy=True
            )
        )

        semantic_scores = cosine_similarity(
            question_embedding,
            self.semantic_embeddings
        )[0]

        # --------------------------------
        # Hybrid Score
        # --------------------------------
        hybrid_scores = (
            0.30 * tfidf_scores
            +
            0.70 * semantic_scores
        )

        # --------------------------------
        # Intent Boost
        # --------------------------------
        final_scores = []

        for index in range(
            len(self.faq_data)
        ):

            boost = self.calculate_intent_boost(
                user_question,
                self.faq_data.iloc[index]["question"]
            )

            final_score = (
                hybrid_scores[index]
                + boost
            )

            final_scores.append(
                final_score
            )

        final_scores = pd.Series(
            final_scores
        ).to_numpy()

        # --------------------------------
        # Keep confidence between 0 and 1
        # --------------------------------
        final_scores = final_scores.clip(
            0,
            1
        )

        # --------------------------------
        # Find best FAQ
        # --------------------------------
        best_index = final_scores.argmax()

        best_score = final_scores[
            best_index
        ]

        # --------------------------------
        # Threshold Check
        # --------------------------------
        if best_score < threshold:

            return {
                "found": False,
                "question": None,
                "answer": (
                    "Sorry, I could not find a "
                    "relevant answer. Please contact "
                    "the concerned college department."
                ),
                "category": "Unknown",
                "confidence": float(best_score)
            }

        # --------------------------------
        # Return Best FAQ
        # --------------------------------
        best_faq = self.faq_data.iloc[
            best_index
        ]

        return {
            "found": True,
            "question": best_faq["question"],
            "answer": best_faq["answer"],
            "category": best_faq["category"],
            "confidence": float(best_score)
        }