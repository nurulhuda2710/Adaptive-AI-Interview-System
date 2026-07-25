import psycopg

from config import (
    PGHOST,
    PGPORT,
    PGDATABASE,
    PGUSER,
    PGPASSWORD
)

def get_connection():

    conn = psycopg.connect(
        host=PGHOST,
        port=PGPORT,
        dbname=PGDATABASE,
        user=PGUSER,
        password=PGPASSWORD,
        sslmode="require"
    )

    return conn


def create_database():

    conn = get_connection()
    cursor = conn.cursor()

    # -------------------------------------------------
    # Candidate Table
    # -------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS candidate (

            candidate_id SERIAL PRIMARY KEY,

            name VARCHAR(255),

            university VARCHAR(255),

            study_level VARCHAR(100),

            course VARCHAR(255),

            employment_status VARCHAR(100),

            target_position VARCHAR(255),

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
    """)

    # -------------------------------------------------
    # Interview Table
    # -------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interview (

            id SERIAL PRIMARY KEY,

            candidate_id INT,

            question_number INT,

            question TEXT,

            answer TEXT,

            FOREIGN KEY (candidate_id)
            REFERENCES candidate(candidate_id)
            ON DELETE CASCADE

        )
    """)

    # -------------------------------------------------
    # Evaluation Table
    # -------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS evaluation (

            id SERIAL PRIMARY KEY,

            candidate_id INT,

            communication FLOAT,

            technical FLOAT,

            problem_solving FLOAT,

            confidence FLOAT,

            overall_score FLOAT,

            strengths TEXT,

            weaknesses TEXT,

            improvement_recommendations TEXT,

            summary TEXT,

            final_recommendation VARCHAR(100),

            FOREIGN KEY (candidate_id)
            REFERENCES candidate(candidate_id)
            ON DELETE CASCADE

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
        (
            name,
            university,
            study_level,
            course,
            employment_status,
            target_position
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING candidate_id
    """, (
        name,
        university,
        study_level,
        course,
        employment_status,
        target_position
    ))

    candidate_id = cursor.fetchone()[0]

    conn.commit()
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
        VALUES (%s, %s, %s, %s)
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
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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

# -------------------------------------------------
# Test Connection
# -------------------------------------------------

if __name__ == "__main__":

    print("1. Start")

    create_database()

    print("2. Database created")

    print("✅ PostgreSQL connection successful.")