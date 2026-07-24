import json

from openai import OpenAI
from config import OPENAI_API_KEY

# -------------------------------------------------
# OpenAI Client
# -------------------------------------------------

client = OpenAI(api_key=OPENAI_API_KEY)

# -------------------------------------------------
# Evaluate Candidate Interview
# -------------------------------------------------

def evaluate_interview(candidate_info, interview_history):
    """
    Evaluate the candidate's interview performance
    based on the interview transcript.
    """

    history_text = ""

    for i, item in enumerate(interview_history, start=1):
        history_text += f"""
    Question {i}
    {item['question']}

    Candidate Answer
    {item['answer']}

    ----------------------------------------
    """

    response = client.responses.create(

        model="gpt-5",

        input=f"""
    You are an experienced HR interviewer responsible for evaluating job candidates objectively and fairly.

    ==========================
    Candidate Information
    ==========================

    Name: {candidate_info.get("name")}

    University: {candidate_info.get("university")}

    Study Level: {candidate_info.get("study_level")}

    Course: {candidate_info.get("course")}

    Employment Status: {candidate_info.get("employment_status")}

    Target Position: {candidate_info.get("target_position")}


    ==========================
    Interview Transcript
    ==========================
    
    {history_text}

    ==========================
    Evaluation Instructions
    ==========================

    Based ONLY on the interview transcript, evaluate the candidate using the following criteria.

    1. Communication Skills
    - Clarity of explanation
    - Fluency
    - Professional communication

    2. Technical Knowledge
    - Understanding of technical concepts
    - Accuracy
    - Relevant knowledge

    3. Problem Solving
    - Logical thinking
    - Analytical ability
    - Quality of solution

    4. Confidence
    - Confidence during responses
    - Professionalism
    - Ability to explain ideas

    Assign an integer score between 1 and 10 for each criterion.
    
    Use the following guideline:

        9-10 = Excellent
        
        7-8 = Good
        
        5-6 = Average
        
        3-4 = Weak
        
        1-2 = Poor
        
    Do not assign all scores as 10.

    Base every score only on the interview transcript and candidate responses.

    If the candidate provides insufficient evidence for a competency, assign a lower score accordingly.

    Calculate the Overall Score by averaging the four evaluation criteria and round the result to the nearest whole number.

    The Overall Score must be an integer between 1 and 10.

    Identify exactly THREE strengths based on the interview responses.

    Identify exactly THREE weaknesses based on the interview responses.

    Do not repeat the same point in strengths and weaknesses.

    Provide exactly THREE improvement recommendations.

    Write a concise HR summary (2-3 sentences).

    Determine the final hiring recommendation using ONLY one of the following values:
    - Suitable for Hiring
    - Needs Further Interview
    - Not Suitable

    Use the following guideline:
    - Overall Score 8–10 → Suitable for Hiring
    - Overall Score 6–7 → Needs Further Interview
    - Overall Score 1–5 → Not Suitable


    Return ONLY valid JSON.
    
    Important Rules:
    - Evaluate fairly and objectively.
    - Do not assume skills that are not demonstrated.
    - Do not invent information.
    - Base your evaluation only on the interview transcript.

    {{
        "communication": 0,
        "technical": 0,
        "problem_solving": 0,
        "confidence": 0,
        "overall_score": 0,

        "strengths": [
            "",
            "",
            ""
        ],

        "weaknesses": [
            "",
            "",
            ""
        ],

        "improvement_recommendations": [
            "",
            "",
            ""
        ],

        "summary": "",

        "final_recommendation": ""
    }}

    Do NOT return Markdown.

    Do NOT explain anything.

    Return JSON only.

    """
    )

    print(response.output_text)

    result = json.loads(response.output_text)

    return result