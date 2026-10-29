# Smart College FAQ System

An NLP-based FAQ retrieval application that helps students find answers
to common college-related questions by asking them in natural language.

## Overview

The system compares a student's question with a predefined FAQ dataset
and returns the most relevant stored answer. Supported topics include
admissions, examinations, fees, library, hostel, attendance, placements,
scholarships, academics, student activities, and general college
information.

It combines lexical similarity (TF-IDF) and semantic similarity
(Sentence Transformers), with hybrid scoring and an intent-based
adjustment. It is a **retrieval-based system**: it retrieves answers
from the FAQ dataset instead of generating new answers with a large
language model.

## Features

-   Streamlit question-answering interface.
-   FAQ retrieval using TF-IDF and cosine similarity.
-   Semantic matching with `all-MiniLM-L6-v2`.
-   Hybrid lexical and semantic scoring.
-   Displays answer, category, matched FAQ, and match-confidence score.
-   Unknown-question handling.
-   FastAPI backend with Swagger documentation.
-   SQLite question-history storage.
-   Test scripts for preprocessing, TF-IDF, semantic, hybrid, and API
    behaviour.

## Technology Stack

  Component             Technology
  --------------------- --------------------------------------------
  Language              Python
  Frontend              Streamlit
  Backend API           FastAPI
  API server            Uvicorn
  Text preprocessing    NLTK
  Dataset handling      Pandas
  Lexical similarity    Scikit-learn: TF-IDF and cosine similarity
  Semantic embeddings   Sentence Transformers: `all-MiniLM-L6-v2`
  History storage       SQLite
  Dataset               CSV

## Project Structure

``` text
Smart-College-FAQ/
├── app.py
├── faq_engine.py
├── hybrid_engine.py
├── preprocessing.py
├── requirements.txt
├── data/
│   └── faq_data.csv
├── backend/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   └── faq_history.db
├── models/
├── screenshots/
├── test_preprocessing.py
├── test_engine.py
├── test_semantic.py
├── test_hybrid.py
└── test_api.py
```

The exact files can vary by local setup. Keep the dataset at
`data/faq_data.csv` unless you update the path in the code.

## How It Works

1.  The student enters a question in the Streamlit interface.
2.  The frontend sends the question to the FastAPI backend.
3.  Text preprocessing lowercases the text, removes unwanted characters
    and stopwords, and applies lemmatization.
4.  TF-IDF compares lexical similarity between the question and stored
    FAQ questions.
5.  Sentence Transformer embeddings are used to compare semantic
    similarity.
6.  The hybrid engine combines the scores and applies the intent-based
    adjustment implemented in the code.
7.  The best-scoring FAQ is returned if it passes the configured
    threshold. Otherwise, the system returns an
    unknown/no-relevant-answer response.
8.  The frontend displays the result. SQLite is used for
    question-history storage.

The current hybrid scoring uses a 30% TF-IDF component and a 70%
semantic-similarity component, with an additional intent-based boost
where applicable. The confidence score is a retrieval score, not a
calibrated probability.

## Requirements

-   Python and `pip`
-   Dependencies listed in `requirements.txt`
-   Internet access on the first run may be required to download the
    Sentence Transformer model and NLTK resources

## Setup (Windows PowerShell)

Run these commands from the project root.

### 1. Create and activate a virtual environment

``` powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

``` powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Check that the dependencies in `requirements.txt` match the packages
imported by the source code.

### 3. Check the dataset

Ensure this file exists:

``` text
data/faq_data.csv
```

The CSV should include the question, answer, and category columns
expected by the code. Answers containing commas must be correctly
quoted.

## Run the Application

Open two terminals in VS Code. Activate the virtual environment in both.

### Terminal 1 --- FastAPI backend

``` powershell
uvicorn backend.main:app --reload
```

Local URLs:

-   API: `http://127.0.0.1:8000`
-   Swagger docs: `http://127.0.0.1:8000/docs`

Keep the backend running while using the frontend or running API tests.

### Terminal 2 --- Streamlit frontend

``` powershell
streamlit run app.py
```

Open the local URL printed by Streamlit. Start the backend first if the
frontend sends requests to the FastAPI service.

## API Endpoints

  Method   Endpoint        Purpose
  -------- --------------- ------------------------------------------
  `GET`    `/health`       Check backend health
  `POST`   `/ask`          Submit a question and retrieve an answer
  `GET`    `/faqs`         Retrieve FAQ data
  `GET`    `/categories`   Retrieve available categories
  `GET`    `/history`      Retrieve question history

### Example request

Send a `POST` request to `http://127.0.0.1:8000/ask` with this JSON
body:

``` json
{
  "question": "How can I get a hostel room?"
}
```

The response schema includes fields such as `found`, `question`,
`answer`, `category`, and `confidence`, according to the backend
implementation.

## Testing

Run the component tests from the project root:

``` powershell
python test_preprocessing.py
python test_engine.py
python test_semantic.py
python test_hybrid.py
```

For API tests, keep the FastAPI backend running in another terminal:

``` powershell
python test_api.py
```

If the API tests show `Connection refused` or `WinError 10061`, start
the backend first and rerun the tests. That error means the test client
could not connect to the server at the configured address.

## Example Queries

-   `How can I get a hostel room?`
-   `Where do I get books?`
-   `I want to register for campus placement`
-   `Where can I find examination notices?`
-   `What is the weather today?` --- an unrelated query for
    demonstrating unknown-question handling.

Exact answers and scores depend on the dataset and scoring
configuration.

## Limitations and Notes

-   Answers come from the configured FAQ dataset. Verify them against
    official college sources before treating them as authoritative
    policy.
-   The system can only answer questions covered by its FAQ data.
-   The score represents similarity, not a guaranteed probability of
    correctness.
-   First-time model/resource downloads may need internet access.
-   The project retrieves predefined answers; it does not use a
    generative LLM to compose answers.
-   Do not report tests as passing unless they have been run
    successfully with the API and dependencies configured correctly.

## Future Improvements

-   Expand and verify the dataset using official college information.
-   Evaluate with a larger set of paraphrased and unrelated questions.
-   Tune hybrid weights, intent adjustment, and the unknown-query
    threshold using measured results.
-   Improve API error handling and test setup.
-   Consider an admin workflow or deployment after local behaviour is
    validated.

## Academic Details

Update before publishing or submitting:

-   **Project:** Smart College FAQ System
-   **Student name:** \[Your Name\]
-   **Department:** Information Technology
-   **College:** \[Your College Name\]
-   **Academic year:** \[Academic Year\]
-   **Project guide:** \[Guide Name\]

## License

Add a license file if you intend to distribute this project publicly. No
specific open-source license is implied unless one is added.
