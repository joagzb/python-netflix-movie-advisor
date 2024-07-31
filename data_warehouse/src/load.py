import pandas as pd
from helpers import extract_performers

def load_data(dw_engine, dataframe, table_name):
    dataframe.to_sql(table_name, con=dw_engine, if_exists='append', index=False)


def load_dim_tables(dw_engine, df_dim_movies, df_dim_users, df_dim_interactions, df_dim_performers, df_dim_score):
  fix_dim_ids_to_avoid_loading_conflicts(dw_engine, df_dim_movies, df_dim_users, df_dim_interactions, df_dim_performers, df_dim_score)

  dim_columns=["movieID", "title","genre","releaseDate","award"]
  load_data(dw_engine, df_dim_movies[dim_columns], 'dimmovie')

  dim_columns = ["userID","username"]
  load_data(dw_engine, df_dim_users[dim_columns], 'dimuser')

  dim_columns = ['interactionID','finishCount', 'backClickCount', 'movieForwardCount','playCount', 'movieViewPercentage']
  load_data(dw_engine, df_dim_interactions[dim_columns], 'diminteraction')

  dim_columns=["performerID","name","role"]
  load_data(dw_engine, df_dim_performers[dim_columns], 'dimperformer')

  dim_columns=["scoreID","netflixScore","imdbScore","sensacineScore","rottentomatoesScore","peopleScore"]
  load_data(dw_engine, df_dim_score[dim_columns], 'dimscore')

def prepare_fact_watchs_excel(dw_engine,df_recommendations,df_movies,df_dim_interactions):
  df_fact_watchs =df_recommendations.copy()

  # Map users to their IDs
  df_dim_user = pd.read_sql('SELECT userID,username FROM dimuser', con=dw_engine)
  df_fact_watchs= df_fact_watchs.merge(df_dim_user, left_on='name', right_on='username', how='left').drop(columns=['name'])

  # Map movies to their IDs
  df_dim_movie= pd.read_sql('SELECT movieID,title FROM dimmovie', con=dw_engine)
  df_fact_watchs = df_fact_watchs.merge(df_dim_movie, left_on='movie', right_on='title',how='left').drop(columns=['title'])
  df_fact_watchs['movieID'] = df_fact_watchs['movieID'].astype(str)

  # Map performers to the movies they participate in
  df_dim_performers= pd.read_sql('SELECT performerID FROM dimperformer', con=dw_engine)
  df_performers = extract_performers(df_movies)
  df_dim_performers = df_dim_performers.merge(df_performers, left_on='performerID', right_on='id',how='left').drop(columns=['id'])
  df_fact_watchs = df_fact_watchs.merge(df_dim_performers, left_on='movie', right_on='movieTitle').drop(columns=['movieTitle','performerName','performerRole'])

  # Map scores to their movies
  df_dim_score = df_movies.copy()
  df_dim_score = df_dim_score.reset_index(names='scoreID')
  df_fact_watchs = df_fact_watchs.merge(df_dim_score, left_on='movie', right_on='name',how='left').drop(columns=['name','performers','mentions'])

  # Map interactions to their users
  df_fact_watchs = df_fact_watchs.merge(df_dim_interactions, left_on='userID', right_on="interactionID", how='left')

  df_fact_watchs.reset_index(names='id', inplace=True)
  df_fact_watchs = df_fact_watchs.drop_duplicates(subset=['userID', 'movieID','performerID','scoreID','interactionID'])

  return df_fact_watchs[['id','userID', 'movieID','performerID','scoreID','interactionID']]


def prepare_fact_watchs_mongo(dw_engine,df_dim_movies, df_dim_users, df_dim_interactions, df_dim_performers, df_dim_score):
  df_fact_watchs = df_dim_movies[['movieID','title_lowercase']].copy()
  df_fact_watchs = df_fact_watchs.merge(df_dim_performers[["performerID","title_lowercase"]], on="title_lowercase", how="left")
  df_fact_watchs = df_fact_watchs.merge(df_dim_interactions[['interactionID','title_lowercase']], on='title_lowercase', how='left')
  df_fact_watchs= df_fact_watchs.merge(df_dim_users[["userID","title_lowercase"]], on="title_lowercase",how='left')
  df_fact_watchs = df_fact_watchs.merge(df_dim_score[["scoreID","title_lowercase"]], on='title_lowercase',how='left')

  df_fact_watchs = df_fact_watchs[['userID', 'movieID','interactionID','performerID','scoreID']]
  df_fact_watchs.reset_index(names='id', inplace=True)
  query_last_fact_id = """
  SELECT MAX(id) FROM factwatchs;
  """
  last_fact_id_prefix = pd.read_sql(query_last_fact_id, con=dw_engine)
  if last_fact_id_prefix is not None and not last_fact_id_prefix.empty:
    last_fact_id_prefix = int(last_fact_id_prefix.iloc[0, 0])
    df_fact_watchs["id"] = last_fact_id_prefix + df_fact_watchs["id"] + 1

  return df_fact_watchs


def fix_dim_ids_to_avoid_loading_conflicts(dw_engine,df_dim_movies, df_dim_users, df_dim_interactions, df_dim_performers, df_dim_score):
  query_last_movie_id = """
    SELECT movieID
    FROM dimmovie
    ORDER BY movieID DESC
    LIMIT 1;
  """

  query_last_user_id = """
    SELECT MAX(userID) FROM dimuser;
  """

  query_last_interaction_id = """
    SELECT MAX(interactionID) FROM diminteraction;
  """

  query_last_score_id = """
    SELECT MAX(scoreID) FROM dimscore;
  """

  query_last_performer_id = """
    SELECT MAX(performerID) FROM dimperformer;
  """

  last_movie_id_prefix = pd.read_sql(query_last_movie_id, con=dw_engine)
  if last_movie_id_prefix is not None and not last_movie_id_prefix.empty:
    last_movie_id_prefix = last_movie_id_prefix.iloc[0, 0]
    df_dim_movies["movieID"] = last_movie_id_prefix + df_dim_movies["movieID"].astype(str)

  df_dim_users["userID"] = df_dim_users["userID"].astype(int)
  last_user_id = pd.read_sql(query_last_user_id, con=dw_engine).iloc[0, 0]
  if last_user_id is not None:
    last_user_id = int(last_user_id)
    df_dim_users["userID"] = df_dim_users["userID"] + last_user_id + 1

  df_dim_interactions["interactionID"] = df_dim_interactions["interactionID"].astype(int)
  last_interaction_id = pd.read_sql(query_last_interaction_id, con=dw_engine).iloc[0, 0]
  if last_interaction_id is not None:
    last_interaction_id = int(last_interaction_id)
    df_dim_interactions["interactionID"] = df_dim_interactions["interactionID"] + last_interaction_id + 1

  df_dim_score["scoreID"] = df_dim_score["scoreID"].astype(int)
  last_score_id = pd.read_sql(query_last_score_id, con=dw_engine).iloc[0, 0]
  if last_score_id is not None:
    last_score_id = int(last_score_id)
    df_dim_score["scoreID"] = df_dim_score["scoreID"] + last_score_id + 1

  df_dim_performers["performerID"] = df_dim_performers["performerID"].astype(int)
  last_performer_id = pd.read_sql(query_last_performer_id, con=dw_engine).iloc[0, 0]
  if last_performer_id is not None:
    last_performer_id = int(last_performer_id)
    df_dim_performers["performerID"] = df_dim_performers["performerID"] + last_performer_id + 1