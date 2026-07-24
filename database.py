import sqlite3

DATABASE_NAME = "interview.db"

def get_connection():
    """
    Create a connection to SQLite database.
    """
    conn = sqlite3.connect(DATABASE_NAME)
    return conn


def create_database():
    """
    Create all database tables if they do not exist.
    """

    conn = get_connection()
    cursor = conn.cursor()

    # -------------------------------------------------
    # Candidate Table
    # -------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS candidate (

            candidate_id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT,

            university TEXT,

            study_level TEXT,

            course TEXT,

            employment_status TEXT,

            target_position TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
    """)

    # -------------------------------------------------
    # Interview Table
    # -------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interview (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            candidate_id INTEGER,

            question_number INTEGER,

            question TEXT,

            answer TEXT,

            FOREIGN KEY(candidate_id)
            REFERENCES candidate(candidate_id)

        )
    """)

    # -------------------------------------------------
    # Evaluation Table
    # -------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS evaluation (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            candidate_id INTEGER,

            communication REAL,

            technical REAL,

            problem_solving REAL,

            confidence REAL,

            overall_score REAL,

            strengths TEXT,

            weaknesses TEXT,

             improvement_recommendations TEXT,
            
            summary TEXT,

            final_recommendation TEXT,

            FOREIGN KEY(candidate_id)
            REFERENCES candidate(candidate_id)

        )
    """)

    conn.commit()
    conn.close()


# -------------------------------------------------
# Save Candidate Information
# -------------------------------------------------

def save_candidate(
        name,
        university,
        study_level,
        course,
        employment_status,
        target_position
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
                   INSERT INTO candidate
                   (name,
                    university,
                    study_level,
                    course,
                    employment_status,
                    target_position)
                   VALUES (?, ?, ?, ?, ?, ?)
                   """, (
                       name,
                       university,
                       study_level,
                       course,
                       employment_status,
                       target_position
                   ))

    conn.commit()

    candidate_id = cursor.lastrowid

    conn.close()

    return candidate_id

# -------------------------------------------------
# Save Interview Question & Answer
# -------------------------------------------------

def save_interview(
    candidate_id,
    question_number,
    question,
    answer
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO interview
        (
            candidate_id,
            question_number,
            question,
            answer
        )
        VALUES (?, ?, ?, ?)
    """, (
        candidate_id,
        question_number,
        question,
        answer
    ))

    conn.commit()
    conn.close()

# -------------------------------------------------
# Save Evaluation
# -------------------------------------------------

def save_evaluation(
    candidate_id,
    communication,
    technical,
    problem_solving,
    confidence,
    overall_score,
    strengths,
    weaknesses,
    improvement_recommendations,
    summary,
    final_recommendation
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO evaluation
        (
            candidate_id,
            communication,
            technical,
            problem_solving,
            confidence,
            overall_score,
            strengths,
            weaknesses,
            improvement_recommendations,
            summary,
            final_recommendation
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        candidate_id,
        communication,
        technical,
        problem_solving,
        confidence,
        overall_score,
        strengths,
        weaknesses,
        improvement_recommendations,
        summary,
        final_recommendation
    ))

    conn.commit()
    conn.close()