from preprocessing import preprocess_text


test_questions = [
    "How can I apply for the examinations?",
    "Where can I find the college library?",
    "What are the working hours of the college?",
    "How can students register for placements?"
]


print("===== NLP PREPROCESSING TEST =====")

for question in test_questions:

    processed = preprocess_text(question)

    print("\nOriginal:")
    print(question)

    print("Processed:")
    print(processed)