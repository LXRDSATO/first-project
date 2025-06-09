import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

GOOGLE_PLACES_API_KEY = os.getenv('GOOGLE_PLACES_API_KEY')
UNSPLASH_ACCESS_KEY = os.getenv('UNSPLASH_ACCESS_KEY')
GOOGLE_TTS_API_KEY = os.getenv('GOOGLE_TTS_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
REDIS_URL = os.getenv('REDIS_URL')
DATABASE_URL = os.getenv('DATABASE_URL')
SECRET_KEY = os.getenv('SECRET_KEY')
VIDEO_OUTPUT_PATH = os.getenv('VIDEO_OUTPUT_PATH')
IMAGE_OUTPUT_PATH = os.getenv('IMAGE_OUTPUT_PATH')
REVIEW_FOLDER = os.getenv('REVIEW_FOLDER')
