import pandas as pd

def preprocess_data(dataframe):
    format_values(dataframe)
    fill_null_values(dataframe)
    filter_movies_by_mean_score(dataframe)
    return dataframe


def format_values(dataframe):
    dataframe["releaseDate"] = pd.to_datetime(dataframe["releaseDate"])


def fill_null_values(dataframe):
    score_columns = ["netflixScore", "imdbScore", "rottentomatoesScore", "sensacineScore"]
    people_score_mask_null = dataframe["peopleScore"].isnull()
    dataframe.loc[~people_score_mask_null, "peopleScore"] = (dataframe.loc[~people_score_mask_null, "peopleScore"] / 2) * 0.1
    dataframe.loc[people_score_mask_null, "peopleScore"] = dataframe.loc[people_score_mask_null, score_columns].mean(axis=1, skipna=True)

    dataframe["movieAward"] = dataframe["movieAward"].fillna("Sin Info")
    dataframe["performerName"] = dataframe["performerName"].fillna("No Info")

def filter_movies_by_mean_score(dataframe):
    calculate_movie_mean_score(dataframe)
    above_mean_condition = dataframe["score"] > dataframe["score"].mean()
    dataframe = dataframe[above_mean_condition]

def calculate_movie_mean_score(dataframe):
    score_columns = ["netflixScore", "imdbScore", "rottentomatoesScore", "sensacineScore","peopleScore"]
    dataframe["score"] = dataframe[score_columns].mean(axis=1,skipna=True)
    dataframe.drop(columns=score_columns,inplace=True)