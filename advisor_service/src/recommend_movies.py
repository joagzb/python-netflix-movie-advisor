import sys
import os

# Add the parent directory of 'src' to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from configuration.config import Config
import pandas as pd
import argparse


def recommend_movies(movies_datacluster, user_id=None, genre=None):
    if user_id is not None:
        # Filter the user's watched movies and cluster movies
        user_filter = movies_datacluster["userID"] == user_id
        user_data = movies_datacluster[user_filter]

        if user_data.empty:
            return []

        cluster_id = user_data["Cluster"].iloc[0]
        cluster_filter = movies_datacluster["Cluster"] == cluster_id
        user_movies = user_data["title"].tolist()  # Convert to list for better performance with isin
        cluster_movies = movies_datacluster[cluster_filter]

        recommendations = cluster_movies[~cluster_movies["title"].isin(user_movies)]

    elif genre is not None:
        # Filter movies by genre
        genre_filter = movies_datacluster["genre"] == genre
        recommendations = movies_datacluster[genre_filter]

    else:
        raise ValueError("Either user_id or genre must be provided")

    return present_results(recommendations)

def present_results(recommendations):
    recommendations = recommendations[["title", "genre", "releaseDate", "score"]].drop_duplicates(subset="title")
    recommendations["releaseDate"] = recommendations["releaseDate"].dt.strftime("%Y-%m")
    recommendations.sort_values(["score","releaseDate"], ascending=[False,False], inplace=True)
    top_recommendations = recommendations.head(10)
    return top_recommendations[["title", "genre", "releaseDate"]].to_dict(orient='records')

def load_trained_model():
    # Load the precomputed movies_datacluster with cluster assignments
    return pd.read_pickle(Config.TRAINED_MODEL_PATH + '/movies_datacluster.pkl')

def main():
    parser = argparse.ArgumentParser(description='Recommend movies based on user_id or genre.')
    parser.add_argument('--user_id', type=int, help='User ID for recommendation')
    parser.add_argument('--genre', type=str, help='Genre for recommendation')

    args = parser.parse_args()

    # Load the precomputed cluster assignments
    movies_datacluster = load_trained_model()

    # Get recommendations based on provided arguments
    recommendations = recommend_movies(movies_datacluster, user_id=args.user_id, genre=args.genre)

    print("Recommended Movies:")
    for movie in recommendations:
        print(movie)


if __name__ == "__main__":
    main()