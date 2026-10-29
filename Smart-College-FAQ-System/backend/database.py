import sqlite3
from pathlib import Path


# ==========================================
# Database Configuration
# ==========================================

DATABASE_PATH = Path("backend/faq_history.db")


# ==========================================
# Initialize Database
# ==========================================

def initialize_database():

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS question_history (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            question TEXT NOT NULL,

            answer TEXT NOT NULL,

            category TEXT NOT NULL,

            confidence REAL NOT NULL,

            found BOOLEAN NOT NULL,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    connection.commit()
    connection.close()


# ==========================================
# Save Question
# ==========================================

def save_question(
    question,
    answer,
    category,
    confidence,
    found
):

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO question_history
        (
            question,
            answer,
            category,
            confidence,
            found
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            question,
            answer,
            category,
            confidence,
            found
        )
    )

    connection.commit()
    connection.close()


# ==========================================
# Get Question History
# ==========================================

def get_history():

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            question,
            answer,
            category,
            confidence,
            found,
            created_at
        FROM question_history
        ORDER BY id DESC
        """
    )

    rows = cursor.fetchall()

    connection.close()

    return [
        dict(row)
        for row in rows
    ]