import requests


API_URL = "http://127.0.0.1:8000"


# ==========================================
# Test Questions
# ==========================================

test_cases = [

    # Admission
    ("What is the admission process?", "Admission"),

    # Examination
    ("Where can I find exam notices?", "Examination"),

    # Fees
    ("How can I pay my college fees?", "Fees"),

    # Library
    ("Where do I get books?", "Library"),

    # Hostel
    ("How can I get a hostel room?", "Hostel"),

    # Attendance
    ("How much attendance do I need?", "Attendance"),

    # Placement
    ("I want to register for campus placement", "Placement"),

    # Scholarship
    ("How can I get a scholarship?", "Scholarship"),

    # Academic
    ("How can I contact my department?", "Academic"),

    # Student Activities
    ("How can I join a college club?", "Student Activities"),

    # General
    ("What are the college working hours?", "General"),

    # Unknown questions
    ("What is the weather today?", "Unknown"),
    ("How do I cook rice?", "Unknown"),
    ("Tell me a joke.", "Unknown"),
]


# ==========================================
# Counters
# ==========================================

total_tests = len(test_cases)

passed_tests = 0

failed_tests = 0


print("\n==========================================")
print("      SMART COLLEGE FAQ API TEST")
print("==========================================\n")


# ==========================================
# Run Tests
# ==========================================

for number, (question, expected_category) in enumerate(
    test_cases,
    start=1
):

    try:

        response = requests.post(
            f"{API_URL}/ask",
            json={
                "question": question
            },
            timeout=60
        )

        result = response.json()

        actual_category = result.get(
            "category"
        )

        found = result.get(
            "found"
        )

        confidence = result.get(
            "confidence",
            0
        )

        # ----------------------------------
        # Check Result
        # ----------------------------------

        if actual_category == expected_category:

            status = "PASS"
            passed_tests += 1

        else:

            status = "FAIL"
            failed_tests += 1

        print("------------------------------------------")

        print(f"Test {number}")

        print(f"Question: {question}")

        print(
            f"Expected: {expected_category}"
        )

        print(
            f"Actual:   {actual_category}"
        )

        print(
            f"Confidence: {confidence * 100:.2f}%"
        )

        print(f"Status: {status}")


    except Exception as error:

        failed_tests += 1

        print("------------------------------------------")

        print(f"Test {number}")

        print(f"Question: {question}")

        print(f"Status: FAIL")

        print(f"Error: {error}")


# ==========================================
# Final Summary
# ==========================================

accuracy = (
    passed_tests / total_tests
) * 100


print("\n==========================================")
print("             TEST SUMMARY")
print("==========================================")

print(
    f"Total Tests : {total_tests}"
)

print(
    f"Passed      : {passed_tests}"
)

print(
    f"Failed      : {failed_tests}"
)

print(
    f"Accuracy    : {accuracy:.2f}%"
)

print("==========================================")