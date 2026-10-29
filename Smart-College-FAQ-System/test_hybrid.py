from hybrid_engine import HybridFAQEngine


# Create Hybrid FAQ Engine
engine = HybridFAQEngine(
    "data/faq_data.csv"
)


# Test questions
test_questions = [

    # Examination
    "Where can I get exam announcements?",
    "When will the exam schedule be available?",
    "Tell me about examination notices.",

    # Library
    "Where do I get books?",
    "Can I borrow books from the library?",
    "How can I issue a library book?",

    # Hostel
    "I need hostel accommodation.",
    "How can I get a room in the hostel?",
    "What is the hostel admission process?",

    # Placement
    "How do I enroll for placements?",
    "Where can I register for campus placement?",
    "Tell me about placement registration.",

    # Fees
    "How do I pay my college fees?",
    "Where can I find fee information?",

    # Scholarship
    "How can I get a scholarship?",
    "Tell me about scholarships for students.",

    # Attendance
    "What attendance percentage is required?",
    "How much attendance do I need?",

    # Unrelated questions
    "What is the weather today?",
    "Who is the Prime Minister of India?",
    "How do I cook rice?",
    "Tell me a joke."
]


print("\n======================================")
print("       HYBRID FAQ SYSTEM TEST")
print("======================================")


for question in test_questions:

    result = engine.find_answer(
        question,
        threshold=0.50
    )

    print("\n--------------------------------------")

    print("Student Question:")
    print(question)

    print("\nMatched FAQ:")
    print(result["question"])

    print("\nCategory:")
    print(result["category"])

    print("\nHybrid Score:")
    print(
        f"{result['confidence'] * 100:.2f}%"
    )

    print("\nStatus:")

    if result["found"]:
        print("ANSWER FOUND")
    else:
        print("NO RELEVANT ANSWER")

    print("\nAnswer:")
    print(result["answer"])