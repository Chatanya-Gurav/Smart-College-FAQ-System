import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from preprocessing import preprocess_text


class FAQEngine:

    def __init__(self, dataset_path):

        # Load FAQ dataset
        self.faq_data = pd.read_csv(dataset_path)

        # Preprocess all FAQ questions
        self.faq_data["processed_question"] = (
            self.faq_data["question"]
            .apply(preprocess_text)
        )

        # Create TF-IDF vectorizer
        self.vectorizer = TfidfVectorizer()

        # Convert FAQ questions into TF-IDF vectors
        self.faq_vectors = self.vectorizer.fit_transform(
            self.faq_data["processed_question"]
        )

    def find_top_matches(self, user_question, top_k=3):

        # Preprocess user's question
        processed_question = preprocess_text(user_question)

        # Convert user's question into TF-IDF vector
        question_vector = self.vectorizer.transform(
            [processed_question]
        )

        # Calculate cosine similarity
        similarity_scores = cosine_similarity(
            question_vector,
            self.faq_vectors
        )[0]

        # Get indexes of highest scores
        top_indexes = similarity_scores.argsort()[::-1][:top_k]

        matches = []

        for index in top_indexes:

            faq = self.faq_data.iloc[index]

            matches.append({
                "question": faq["question"],
                "answer": faq["answer"],
                "category": faq["category"],
                "confidence": float(similarity_scores[index])
            })

        return matches

    def find_answer(self, user_question, threshold=0.20):

        # Get the best match
        matches = self.find_top_matches(
            user_question,
            top_k=3
        )

        best_match = matches[0]

        # Check similarity threshold
        if best_match["confidence"] < threshold:

            return {
                "found": False,
                "answer": (
                    "Sorry, I could not find a relevant answer. "
                    "Please contact the concerned college department."
                ),
                "category": "Unknown",
                "question": None,
                "confidence": best_match["confidence"],
                "top_matches": matches
            }

        return {
            "found": True,
            "answer": best_match["answer"],
            "category": best_match["category"],
            "question": best_match["question"],
            "confidence": best_match["confidence"],
            "top_matches": matches
        }