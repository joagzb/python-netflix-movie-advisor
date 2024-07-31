import sqlalchemy as db
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from configuration.config import Config


def connect_to_mysql(database):
    username = Config.MYSQL_USER
    password = Config.MYSQL_PASSWORD
    host = Config.MYSQL_HOST
    port = Config.MYSQL_PORT
    uri = f"mysql://{username}:{password}@{host}/{database}"
    print(uri)
    return db.create_engine(uri)
