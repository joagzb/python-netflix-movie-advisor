import pandas as pd
import pickle
from configuration.config import Config


def load_fact_watchs(client):
    query = """
    SELECT factwatchs.userID,
        dimmovie.title, dimmovie.releaseDate, dimmovie.genre, dimmovie.award as movieAward,
        dimscore.netflixScore, dimscore.imdbScore, dimscore.rottentomatoesScore, dimscore.sensacineScore, dimscore.peopleScore,
        dimperformer.name as performerName, dimperformer.role performerRole, dimperformer.award as performerAward,
        diminteraction.finishCount, diminteraction.backClickCount, diminteraction.movieForwardCount, diminteraction.playCount, diminteraction.movieViewPercentage
    FROM factwatchs
    INNER JOIN dimmovie ON factwatchs.movieID = dimmovie.movieID
    INNER JOIN dimscore ON factwatchs.scoreID = dimscore.scoreID
    LEFT JOIN dimperformer ON factwatchs.performerID = dimperformer.performerID
    LEFT JOIN dimuser ON factwatchs.userID = dimuser.userID
    LEFT JOIN diminteraction ON factwatchs.interactionID = diminteraction.interactionID
    """

    return pd.read_sql(query, client)

def load_trained_model():
    with open(Config.TRAINED_MODEL_PATH, "rb") as f:
        kmeans = pickle.load(f)
    return kmeans