import sqlalchemy as db
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from configuration.config import Config


def connect_to_mysql(database):
    username = Config.MYSQL_USER
    password = Config.MYSQL_PASSWORD
    host = Config.MYSQL_HOST
    port = Config.MYSQL_PORT
    uri = f"mysql://{username}:{password}@{host}:{port}/{database}"
    print(uri)
    return db.create_engine(uri)

def connect_to_mongo():
    username = Config.MONGODB_USERNAME
    password = Config.MONGODB_PASSWORD
    host = Config.MONGODB_HOST
    database = Config.MONGODB_CLUSTER_NAME
    uri = f"mongodb+srv://{username}:{password}@{host}?appName={database}"
    print(uri)
    return MongoClient(uri, server_api=ServerApi('1'))
