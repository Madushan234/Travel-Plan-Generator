import os
from dotenv import load_dotenv

load_dotenv()

def get_api_key():
    return os.getenv("GOOGLE_KEY")
    
def get_google_api_key():
    return os.getenv("GOOGLE_API_KEY")
