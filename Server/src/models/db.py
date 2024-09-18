import os

from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

from src.app import app
from config import SERVER_ABS_PATH

# Load environment variables from the .env file
if not load_dotenv(os.path.join(SERVER_ABS_PATH, "config", "credentials.env")):
    print("Failed to load .env file from ",SERVER_ABS_PATH)

# Get credentials for connection to database
user=os.getenv('CANVAS_USER')
password=os.getenv('CANVAS_USER_PASSWORD')
database=os.getenv('CANVAS_DATABASE_NAME')
port = os.getenv('CANVAS_DATABASE_PORT')
host = os.getenv('CANVAS_DATABASE_HOST')
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
