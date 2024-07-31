import pandas as pd

def preprocess_data(dataframe):
    format_values(dataframe)
    fill_null_values(dataframe)
    filter_by_mean_score(dataframe)
    return dataframe


def format_values(dataframe):
    dataframe["releaseDate"] = pd.to_datetime(dataframe["releaseDate"])


def fill_null_values(dataframe):
    score_columns = ["netflixScore", "imdbScore", "rottentomatoesScore", "sensacineScore"]
    dataframe[score_columns] = dataframe[score_columns].fillna(0)

    dataframe["movieAward"] = dataframe["movieAward"].fillna("Sin Info")
    dataframe["performerName"] = dataframe["performerName"].fillna("No Info")

def filter_by_mean_score(dataframe):
    score_columns = ["netflixScore", "imdbScore", "rottentomatoesScore", "sensacineScore"]
    dataframe["score"] = dataframe[score_columns].mean(axis=1)
    above_mean_condition = dataframe["score"] > dataframe["score"].mean()
    dataframe = dataframe[above_mean_condition]