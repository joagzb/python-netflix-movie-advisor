import pandas as pd
from helpers import assign_score, extract_performers, generate_comment, generate_interaction_data, generate_uuid


def transform_excel_data(df_movies,df_recommendations):
  df_dim_movies = df_movies[['name', 'genre']].rename(columns={'name': 'title'})
  df_dim_movies["award"] = None
  df_dim_movies["releaseDate"] = None
  df_dim_movies = df_dim_movies.reset_index(names='movieID')
  df_dim_movies['movieID'] = df_dim_movies['movieID'].astype(str)


  # prepare dimPerformer DataFrame
  df_performers = extract_performers(df_movies)
  df_dim_performers = df_performers.copy()
  df_dim_performers.drop(columns=['id','movieTitle'],inplace=True)
  df_dim_performers.rename(columns={'performerName': 'name', 'performerRole': 'role'}, inplace=True)
  df_dim_performers.reset_index(names='performerID', inplace=True)

  # Calculate score for each movie
  total_recommendations_by_movie = df_recommendations['movie'].value_counts()

  # Create a score dataframe merging df_movies and df_recommendations
  df_movie_scores = pd.DataFrame(df_movies['name'].copy())
  df_movie_scores['recommendations'] = df_movie_scores['name'].map(df_recommendations['movie'].value_counts())
  df_movie_scores['score'] = df_movie_scores['recommendations'].apply(lambda x: assign_score(total_recommendations_by_movie.quantile(0.75), total_recommendations_by_movie.median(), x))

  df_movie_scores= df_movie_scores[['name', 'score']].rename(columns={
    'name': 'title',
    'calculated_score': 'peopleScore'
  })
  df_movie_scores['netflixScore'] = None
  df_movie_scores['imdbScore'] = None
  df_movie_scores['rottentomatoesScore'] = None
  df_movie_scores['sensacineScore'] = None
  df_movie_scores['peopleComment'] = df_movie_scores['score'].apply(lambda x: generate_comment(x))

  #prepare dimScore DataFrame
  df_dim_score = df_movie_scores.copy()
  df_dim_score.drop(columns=['title'], inplace=True)
  df_dim_score.rename(columns={'score': "peopleScore"}, inplace=True)
  df_dim_score = df_dim_score.reset_index(names='scoreID')

  # Apply the function to generate interaction data for each recommendation
  interactions_data = df_recommendations.apply(generate_interaction_data, axis=1)
  df_interactions = pd.DataFrame(list(interactions_data))
  df_interactions = df_interactions.reset_index(names='interactionID')

  # prepare dimInteraction DataFrame
  df_dim_interactions = df_interactions.copy()
  df_dim_interactions.drop(columns=['username'], inplace=True)

  # dim user
  df_dim_user = df_interactions[['username','interactionID']].copy()
  df_dim_user = df_dim_user.rename(columns={'interactionID':'userID'}).drop_duplicates(subset=['username'])

  return df_dim_movies, df_dim_user, df_dim_interactions, df_dim_score, df_dim_performers


def transform_mongo_data(df_movies,df_movies_scores,df_movies_oltp):
  # movies dimention
  df_dim_movies = df_movies[["title_lowercase","movieTitle", "genre","releaseDate","AwardMovie"]].copy()
  df_dim_movies["movieID"] = [generate_uuid() for _ in range(len(df_dim_movies))]
  df_dim_movies = df_dim_movies.rename(columns={"AwardMovie":"award","movieTitle":"title"})

  # users dimention
  df_dim_users = df_movies[["movieIndex","title_lowercase","user"]].copy()
  df_dim_users = df_dim_users.rename(columns={"user": "username","movieIndex":"userID"})

  # interactions dimention
  df_dim_interactions = df_movies[['movieIndex',"title_lowercase",'finishCount', 'backClickCount', 'movieForwardCount','playCount', 'movieViewPercentage']].copy()
  df_dim_interactions = df_dim_interactions.rename(columns={"movieIndex":"interactionID"})

  # performers dimention
  df_dim_performers = df_movies_oltp[["title_lowercase","participantName","performerRole"]].copy()
  df_dim_performers = df_dim_performers.reset_index(names="performerID")
  df_dim_performers.rename(columns={
    "participantName":"name",
    "performerRole":"role",
  }, inplace=True)

  # score dimention
  df_dim_score = df_movies_scores[["title_lowercase","movieTitle",'netflix_score','imdb_score', 'sensacine_score', 'rottentomatoes_score']].copy()

  # merge duplicated values keeping the maximum score if two movies have the same title and different scores
  df_dim_score = df_movies_scores.groupby('title_lowercase').agg({
      'netflix_score': 'max',
      'imdb_score': 'max',
      'sensacine_score': 'max',
      'rottentomatoes_score': 'max'
  }).reset_index()

  # rename columns
  df_dim_score.rename(columns={
      'netflix_score': 'netflixScore',
      'imdb_score': 'imdbScore',
      'sensacine_score': 'sensacineScore',
      'rottentomatoes_score': 'rottentomatoesScore'
  },inplace=True)

  df_dim_score["peopleScore"] = None
  df_dim_score = df_dim_score.reset_index(names="scoreID")

  return df_dim_movies, df_dim_users, df_dim_interactions, df_dim_performers, df_dim_score


def merge_sources(df_movies,df_interactions,df_movies_oltp):
  df_movies_scores = df_movies.copy()

  movies_columns = ['movieTitle', 'genre', 'releaseDate', 'AwardMovie','title_lowercase']
  df_movies = pd.concat([df_movies[movies_columns], df_movies_oltp[movies_columns]], ignore_index=True, axis=0)

  df_movies = df_movies.merge(df_interactions,on="title_lowercase",how="left")
  df_movies = df_movies.drop(columns="movieTitle_y").rename(columns={"movieTitle_x":"movieTitle"})
  df_movies.reset_index(names='movieIndex', inplace=True)

  return df_movies,df_movies_scores,df_movies_oltp


def preprocess_extracted_df(df_movies,df_interactions,df_movies_oltp):
  df_movies.rename(columns={"gender":"genre","title":"movieTitle"},inplace=True)
  df_movies.drop(columns=["_id"],inplace=True)
  df_movies['title_lowercase'] = df_movies['movieTitle'].str.lower()

  df_interactions.drop(columns=["_id"],inplace=True)
  df_interactions['title_lowercase'] = df_interactions['movieTitle'].str.lower()

  df_movies_oltp['title_lowercase'] = df_movies_oltp['title'].str.lower()
  df_movies_oltp['releaseDate'] = df_movies_oltp['releaseDate'].astype(str)
  df_movies_oltp['AwardMovie'] = "Sin Info"
  df_movies_oltp.rename(columns={"title":"movieTitle"},inplace=True)
  df_movies_oltp.drop(columns=["movieID"],inplace=True)
