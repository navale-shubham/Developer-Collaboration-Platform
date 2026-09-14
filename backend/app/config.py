from dotenv import load_dotenv
import os


dotenv_path = '.env' if os.getenv('PRODUCTION') else '.env.dev'
load_dotenv(dotenv_path=dotenv_path)

DATABASE_URL = os.getenv('DATABASE_URL')
SECRET_KEY = os.getenv('SECRET_KEY')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM')
