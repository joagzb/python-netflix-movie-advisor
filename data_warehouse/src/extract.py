import pandas as pd
import os
from configuration.config import Config
from db_connection import connect_to_mongo, connect_to_mysql


def extract_OLTP():
  # connect to MySQL OLTP
  connection_OLTP = connect_to_mysql(Config.MYSQL_DATABASE_OLTP)

  # SQL query to retrieve movie details along with their genre and participants (actors, directors, etc.)
  query = """
  SELECT
      movie.movieID as movieID, movie.movieTitle as title, movie.releaseDate as releaseDate,
      genre.name as genre, person.name as participantName, performer.performerRole as performerRole
  FROM movie
  INNER JOIN performer ON movie.movieID=performer.movieID
  INNER JOIN person ON person.personID = performer.personID
  INNER JOIN movie_genre ON movie.movieID = movie_genre.movieID
  INNER JOIN genre ON movie_genre.genreID = genre.genreID
  """

  # Execute the SQL query and load the result into a DataFrame
  return pd.read_sql(query, con=connection_OLTP)


def extract_mongo_data(collection_name):
    client = connect_to_mongo()
    db = client['netflix_movies']
    collection = db[collection_name]
    documents = list(collection.find())
    return pd.DataFrame(documents)


def extract_mongo_movies():
  return extract_mongo_data('movies_df')

def extract_mongo_interactions():
    return extract_mongo_data('user_netflix_interactions')


def extract_excel_data(file_path,sheet_name):
  file_path = os.path.join(os.path.dirname(__file__), file_path)
  if not os.path.exists(file_path):
    raise FileNotFoundError(f"The file {file_path} does not exist.")

  return pd.read_excel(file_path,sheet_name)


def extract_excel_movies_data():
  file_path = '../data/facebook_groups.xlsx'
  return extract_excel_data(file_path, 'movies')

def extract_excel_recommendations_data():
  file_path = '../data/facebook_groups.xlsx'
  return extract_excel_data(file_path, 'recommendations')