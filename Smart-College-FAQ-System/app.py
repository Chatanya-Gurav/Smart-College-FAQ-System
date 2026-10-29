import requests
import streamlit as st


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Smart College FAQ System",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# =========================================================
# BACKEND CONFIGURATION
# =========================================================

API_URL = "http://127.0.0.1:8000"


# =========================================================
# SESSION STATE
# =========================================================

if "question" not in st.session_state:
    st.session_state.question = ""


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
<style>
.block-container {
    max-width: 900px;
    padding-top: 2.5rem;
    padding-bottom: 3rem;
}

.hero {
    text-align: center;
    padding: 10px 0 25px 0;
}

.hero-icon {
    font-size: 52px;
    margin-bottom: 8px;
}

.main-title {
    font-size: 42px;
    font-weight: 750;
    color: #202124;
    margin-bottom: 5px;
}

.main-subtitle {
    font-size: 18px;
    color: #6b7280;
}

.section-title {
    font-size: 28px;
    font-weight: 700;
    color: #202124;
    margin-bottom: 6px;
}

.section-description {
    font-size: 16px;
    color: #6b7280;
    margin-bottom: 18px;
}

.popular-title {
    font-size: 22px;
    font-weight: 700;
    color: #202124;
    margin-top: 10px;
    margin-bottom: 15px;
}

.answer-box {
    padding: 22px;
    border-radius: 14px;
    background: #f5f9ff;
    border-left: 5px solid #4f8cff;
    font-size: 17px;
    line-height: 1.7;
    color: #202124;
}

.matched-box {
    padding: 16px 18px;
    border-radius: 10px;
    background: #f8fafc;
    border: 1px solid #e5e7eb;
    font-size: 15px;
    color: #4b5563;
}

.footer {
    text-align: center;
    color: #9ca3af;
    font-size: 13px;
    padding-top: 10px;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}
</style>
""",
    unsafe_allow_html=True
)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
<div class="hero">
<div class="hero-icon">🎓</div>
<div class="main-title">Smart College FAQ System</div>
<div class="main-subtitle">Your college questions, answered simply.</div>
</div>
""",
    unsafe_allow_html=True
)


st.divider()


# =========================================================
# QUESTION SECTION
# =========================================================

st.markdown(
    """
<div class="section-title">💬 What would you like to know?</div>
<div class="section-description">
Ask about admissions, examinations, fees, library,
hostel, placements, scholarships and more.
</div>
""",
    unsafe_allow_html=True
)


# =========================================================
# QUESTION INPUT
# =========================================================

user_question = st.text_input(
    "Enter your question",
    value=st.session_state.question,
    placeholder="Example: How can I apply for hostel?",
    key="question_input"
)


# =========================================================
# ASK BUTTON
# =========================================================

ask_clicked = st.button(
    "🔍  Ask Question",
    use_container_width=True
)


# =========================================================
# POPULAR QUESTIONS
# =========================================================

st.write("")

st.markdown(
    '<div class="popular-title">Popular Questions</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)


with col1:

    if st.button(
        "📚  Library\n\nBooks & timings",
        use_container_width=True
    ):
        st.session_state.question = "Where can I get books?"
        st.rerun()


with col2:

    if st.button(
        "🏠  Hostel\n\nAccommodation",
        use_container_width=True
    ):
        st.session_state.question = "How can I get a hostel room?"
        st.rerun()


with col3:

    if st.button(
        "💼  Placement\n\nCareer & registration",
        use_container_width=True
    ):
        st.session_state.question = (
            "How do I register for placements?"
        )
        st.rerun()


# =========================================================
# PROCESS QUESTION
# =========================================================

if ask_clicked:

    if not user_question.strip():

        st.warning(
            "Please enter a question before asking."
        )

    else:

        try:

            response = requests.post(
                f"{API_URL}/ask",
                json={
                    "question": user_question.strip()
                },
                timeout=60
            )

            response.raise_for_status()

            result = response.json()

        except requests.exceptions.ConnectionError:

            st.error(
                "The FAQ service is currently unavailable. "
                "Please make sure the FastAPI backend is running."
            )

            result = None

        except requests.exceptions.Timeout:

            st.error(
                "The request took too long. Please try again."
            )

            result = None

        except requests.RequestException:

            st.error(
                "Something went wrong while processing "
                "your question. Please try again."
            )

            result = None


        # =================================================
        # DISPLAY RESULT
        # =================================================

        if result:

            st.divider()


            # =================================================
            # ANSWER FOUND
            # =================================================

            if result.get("found", False):

                st.success("✓ Relevant answer found")


                # -------------------------------------------------
                # ANSWER
                # -------------------------------------------------

                st.subheader("🤖 Answer")

                st.markdown(
                    f"""
<div class="answer-box">
{result["answer"]}
</div>
""",
                    unsafe_allow_html=True
                )


                st.write("")


                # -------------------------------------------------
                # CATEGORY + CONFIDENCE
                # -------------------------------------------------

                col1, col2 = st.columns(2)


                with col1:

                    st.caption("CATEGORY")

                    st.info(
                        result["category"]
                    )


                with col2:

                    st.caption("MATCH CONFIDENCE")

                    confidence = (
                        result["confidence"] * 100
                    )

                    st.info(
                        f"{confidence:.2f}%"
                    )


                # -------------------------------------------------
                # MATCHED FAQ
                # -------------------------------------------------

                st.write("")

                st.caption("MATCHED FAQ")

                st.markdown(
                    f"""
<div class="matched-box">
{result["question"]}
</div>
""",
                    unsafe_allow_html=True
                )


            # =================================================
            # NO RELEVANT ANSWER
            # =================================================

            else:

                st.warning(
                    "⚠️ We couldn't find a relevant answer."
                )

                st.write(
                    "Please try asking your question in a "
                    "different way, or contact the concerned "
                    "college department for further assistance."
                )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.markdown(
    """
<div class="footer">
Smart College FAQ System •
Helping students find college information quickly
</div>
""",
    unsafe_allow_html=True
)