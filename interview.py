from openai import OpenAI
from config import OPENAI_API_KEY

# -------------------------------------------------
# OpenAI Client
# -------------------------------------------------

client = OpenAI(api_key=OPENAI_API_KEY)


# -------------------------------------------------
# Generate First Interview Question
# -------------------------------------------------

def generate_first_question(candidate_info):
    """
    Generate the opening interview question based on
    the candidate's background.
    """

    response = client.responses.create(

        model="gpt-5",

        input=f"""
You are an experienced HR interviewer conducting a professional job interview.

Candidate Information:
- Name: {candidate_info.get('name', '')}
- University: {candidate_info.get('university', '')}
- Study Level: {candidate_info.get('study_level', '')}
- Course: {candidate_info.get('course', '')}
- Employment Status: {candidate_info.get('status', '')}
- Target Position: {candidate_info.get('position', '')}

This is Question 1 of 5.

Generate ONE professional opening interview question.

Requirements:
- Ask the candidate to introduce themselves.
- Relate the question to the target position whenever appropriate.
- Keep the question professional and conversational.
- Ask ONLY one question.
- Do NOT evaluate the candidate.
- Return ONLY the interview question.
"""
    )

    return response.output_text.strip()


# -------------------------------------------------
# Generate Follow-up Question
# -------------------------------------------------

def generate_followup_question(candidate_info, interview_history, question_number):
    """
    Generate an adaptive follow-up interview question
    based on the candidate's previous responses.
    """

    history_text = "\n\n".join(
        [
            f"Question: {item['question']}\nAnswer: {item['answer']}"
            for item in interview_history
        ]
    )

    response = client.responses.create(

        model="gpt-5",

        input=f"""
You are an experienced HR interviewer conducting a professional job interview.

Candidate Information:
- Name: {candidate_info.get('name', '')}
- University: {candidate_info.get('university', '')}
- Study Level: {candidate_info.get('study_level', '')}
- Course: {candidate_info.get('course', '')}
- Employment Status: {candidate_info.get('status', '')}
- Target Position: {candidate_info.get('position', '')}

Interview History:

{history_text}

Current Question Number: {question_number} of 5

Interview Flow:

Question 2:
- Academic background
- Previous work experience
- Internship
- Projects related to the target position

Question 3:
- Technical knowledge
- Problem-solving ability
- Relevant tools, methods, or technologies

Question 4:
- Behavioural or situational interview
- Teamwork
- Leadership
- Communication
- Conflict resolution

Question 5:
- Career goals
- Motivation
- Strengths
- Closing interview question

Requirements:
- Generate ONLY ONE interview question.
- Build naturally from the candidate's previous answer.
- Do NOT repeat previous questions.
- Be relevant to the target position.
- Keep the interview conversational and professional.
- Ask ONLY one question.
- Do NOT evaluate the candidate.
- Return ONLY the interview question.
"""
    )

    return response.output_text.strip()