from dotenv import load_dotenv
import os
load_dotenv()

class Config:
    MYSQL_USER = os.getenv('MYSQL_USER')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
    MYSQL_HOST = os.getenv('MYSQL_HOST')
    MYSQL_PORT = os.getenv('MYSQL_PORT')
    MYSQL_DATABASE_DW = os.getenv('MYSQL_DATABASE_DW')
    MYSQL_DATABASE_OLTP = os.getenv('MYSQL_DATABASE_OLTP')

    MONGODB_USERNAME = os.getenv('MONGODB_USERNAME')
    MONGODB_PASSWORD = os.getenv('MONGODB_PASSWORD')
    MONGODB_HOST = os.getenv('MONGODB_HOST')
    MONGODB_CLUSTER_NAME = os.getenv('MONGODB_CLUSTER_NAME')
    MONGODB_DATABASE = os.getenv('MONGODB_DATABASE')