import pandas as pd
import pickle
from configuration.config import Config


def load_fact_watchs(client):
    query = """
    SELECT factwatchs.userID,
           dimmovie.title, dimmovie.releaseDate, dimmovie.genre, dimmovie.award as movieAward,
           dimscore.netflixScore, dimscore.imdbScore, dimscore.rottentomatoesScore, dimscore.sensacineScore,
           dimperformer.name as performerName
    FROM factwatchs
    INNER JOIN dimmovie ON factwatchs.movieID = dimmovie.movieID
    INNER JOIN dimuser ON factwatchs.userID = dimuser.userID
    INNER JOIN dimscore ON factwatchs.scoreID = dimscore.scoreID
    LEFT JOIN dimperformer ON factwatchs.performerID = dimperformer.performerID
    """

    return pd.read_sql(query, client)

def load_trained_model():
    with open(Config.TRAINED_MODEL_PATH, "rb") as f:
        kmeans = pickle.load(f)
    return kmeans