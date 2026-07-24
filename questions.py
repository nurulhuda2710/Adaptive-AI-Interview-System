from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def generate_question(position, course):
    response = client.responses.create(
        model="gpt-5",
        input=f"""
    You are an experienced HR interviewer.

    The candidate is a fresh graduate.

    Course:
    {course}

    Target Position:
    {position}

    Generate ONE interview question from ONLY ONE of these categories:

    1. Self Introduction
    2. Internship or Final Year Project
    3. Communication Skills
    4. Teamwork
    5. Strengths
    6. Weaknesses
    7. Career Goals
    8. Basic Problem Solving
    
    Do NOT ask about:
    - Git
    - Docker
    - Kubernetes
    - CI/CD
    - System Design
    - Cloud Architecture
    - Advanced programming concepts
    - Anything requiring work experience
    
    The question must:
    - Be beginner-friendly
    - Suitable for fresh graduates
    - Maximum 30 words
    - Do not provide the answer
    """
)
    return response.output_text