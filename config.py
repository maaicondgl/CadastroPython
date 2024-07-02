from dotenv import load_dotenv
import os

load_dotenv()

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

print(f"Conectando ao banco de dados {DB_NAME} em {DB_HOST}:{DB_PORT} como {DB_USER}...")
