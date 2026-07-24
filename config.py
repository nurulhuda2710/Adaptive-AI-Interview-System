from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Get API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")