import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_NAME = os.environ.get('DATABASE_NAME', 'test')
GROQ_API_KEY = os.environ.get('GROQ_API_KEY', 'test')