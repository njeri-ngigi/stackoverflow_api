'''app/__init__.py'''
import os
from dotenv import load_dotenv

APP_ROOT = os.path.join(os.path.dirname(__file__), '..')
# Create .env file path.
dotenv_path = os.path.join(APP_ROOT, '.env')
# Load file from the path.
load_dotenv(dotenv_path)
