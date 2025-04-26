import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration class"""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
    PDFLAYER_API_KEY = os.environ.get('PDFLAYER_API_KEY')
    PDFLAYER_API_ENDPOINT = 'https://api.pdflayer.com/api/convert'
    PDF_STORAGE_PATH = os.path.join(os.getcwd(), 'app', 'static', 'pdfs')
    
    # Create PDF storage directory if it doesn't exist
    os.makedirs(PDF_STORAGE_PATH, exist_ok=True)