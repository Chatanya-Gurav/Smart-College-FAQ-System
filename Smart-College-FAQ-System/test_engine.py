from faq_engine import FAQEngine


# Create FAQ engine
engine = FAQEngine("data/faq_data.csv")


questions = [
    "How do I apply for hostel?",
    "Where can I see examination information?",
    "I want to register for placement",
    "How do I borrow a library book?",
    "What is the attendance requirement?",
    "How can I apply for scholarship?",
    "What is the weather today?"
]


print("======================================")
print("     SMART COLLEGE FAQ NLP TEST")
print("======================================")


for question in questions:

    result = engine.find_answer(question)

    print("\n--------------------------------------")

    print("Student Question:")
    print(question)

    print("\nBest Match:")
    print(result["question"])

    print("\nCategory:")
    print(result["category"])

    print("\nSimilarity Score:")
    print(f"{result['confidence'] * 100:.2f}%")

    print("\nAnswer:")
    print(result["answer"])

    print("\nTop 3 Matches:")

    for position, match in enumerate(
        result["top_matches"],
        start=1
    ):

        print(
            f"{position}. "
            f"{match['question']} "
            f"-> "
            f"{match['confidence'] * 100:.2f}%"
        )