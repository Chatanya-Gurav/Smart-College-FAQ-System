import re
import nltk

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


# Download required NLTK resources
nltk.download("stopwords")
nltk.download("wordnet")
nltk.download("omw-1.4")


# Load English stopwords
stop_words = set(stopwords.words("english"))

# Create lemmatizer
lemmatizer = WordNetLemmatizer()


def preprocess_text(text):
    """
    Preprocess text for the FAQ NLP system.

    Steps:
    1. Convert text to lowercase
    2. Remove special characters and numbers
    3. Tokenize text
    4. Remove stopwords
    5. Lemmatize words
    6. Return cleaned text
    """

    # Convert to lowercase
    text = text.lower()

    # Remove special characters and numbers
    text = re.sub(r"[^a-zA-Z\s]", " ", text)

    # Tokenization
    words = text.split()

    # Remove stopwords and perform lemmatization
    processed_words = []

    for word in words:

        if word not in stop_words:

            lemma = lemmatizer.lemmatize(word)

            processed_words.append(lemma)

    # Convert list back into a sentence
    return " ".join(processed_words)