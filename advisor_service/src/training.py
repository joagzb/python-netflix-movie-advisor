from sqlalchemy import create_engine
from .data_prosessing import preprocess_data
from .data_loading import load_fact_watchs
from .data_clustering import run_clustering
from configuration.config import Config

def main():
    # Database connection
    dw_engine = create_engine(Config.MYSQL_DATABASE_DW)

    # Load data
    fact_watchs_df = load_fact_watchs(dw_engine)

    # Preprocess data
    fact_watchs_df = preprocess_data(fact_watchs_df)

    # run kmeans clustering
    tabla_model = run_clustering(fact_watchs_df)

    # Merge cluster data
    movies_datacluster = fact_watchs_df.merge(tabla_model[['userID', 'Cluster']], on='userID', how='left')

    # Save tabla_model with cluster assignments
    movies_datacluster.to_pickle(Config.TRAINED_MODEL_PATH + '/movies_datacluster.pkl')

if __name__ == "__main__":
    main()