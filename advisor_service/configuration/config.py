from dotenv import load_dotenv
import os
load_dotenv()

class Config:
    MYSQL_USER = os.getenv('MYSQL_USER')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
    MYSQL_HOST = os.getenv('MYSQL_HOST')
    MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))
    MYSQL_DATABASE_DW = os.getenv('MYSQL_DATABASE_DW')
    MYSQL_DATABASE_OLTP = os.getenv('MYSQL_DATABASE_OLTP')
    TRAINED_MODEL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../models'))
