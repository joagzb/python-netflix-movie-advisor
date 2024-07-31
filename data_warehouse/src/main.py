import sys
import os

# Add the parent directory of 'src' to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from configuration.config import Config
from transform import merge_sources, preprocess_extracted_df, transform_excel_data, transform_mongo_data
from db_connection import connect_to_mysql
from extract import (
    extract_OLTP,
    extract_excel_movies_data,
    extract_excel_recommendations_data,
    extract_mongo_interactions,
    extract_mongo_movies,
)
from src.load import load_data, load_dim_tables, prepare_fact_watchs_excel, prepare_fact_watchs_mongo


def etl_excel():
	# connection to data warehouse
	dw_engine = connect_to_mysql(Config.MYSQL_DATABASE_DW)

	# extract stage
	df_movies_excel = extract_excel_movies_data()
	df_recommendations_excel = extract_excel_recommendations_data()

	# transform stage
	df_dim_movies, df_dim_user, df_dim_interactions, df_dim_score, df_dim_performers = transform_excel_data(df_movies_excel, df_recommendations_excel)

	# load stage
	with dw_engine.begin() as conn:
		try:
			load_dim_tables(dw_engine,df_dim_movies, df_dim_user, df_dim_interactions, df_dim_performers, df_dim_score)
			df_fact_watchs = prepare_fact_watchs_excel(dw_engine,df_recommendations_excel,df_movies_excel,df_dim_interactions)
			load_data(dw_engine, df_fact_watchs, 'factwatchs')
		except Exception as e:
			print(f"An error occurred: {e}")
			raise ValueError("An error occurred while processing transactions during LOAD STAGE.")


def etl_mongo_mysql():
	# connection to data warehouse
	dw_engine = connect_to_mysql(Config.MYSQL_DATABASE_DW)

	# extract stage
	df_movies_oltp = extract_OLTP()
	df_movies = extract_mongo_movies()
	df_interactions = extract_mongo_interactions()

	# transform stage
	preprocess_extracted_df(df_movies,df_interactions,df_movies_oltp)
	df_movies,df_movies_scores,df_movies_oltp = merge_sources(df_movies,df_interactions,df_movies_oltp)

	df_dim_movies, df_dim_users, df_dim_interactions, df_dim_performers, df_dim_score = transform_mongo_data(df_movies,df_movies_scores,df_movies_oltp)

	# load stage
	with dw_engine.begin() as conn:
		try:
			load_dim_tables(dw_engine,df_dim_movies, df_dim_users, df_dim_interactions, df_dim_performers, df_dim_score)
			df_fact_watchs = prepare_fact_watchs_mongo(dw_engine,df_dim_movies, df_dim_users, df_dim_interactions, df_dim_performers, df_dim_score)
			load_data(dw_engine, df_fact_watchs, 'factwatchs')
		except Exception as e:
			print(f"An error occurred: {e}")
			raise ValueError("An error occurred while processing transactions during LOAD STAGE.")


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python main.py <etl_type>")
        print("etl_type: 'excel' or 'mongo_mysql'")
        sys.exit(1)

    etl_type = sys.argv[1]

    if etl_type == 'excel':
        etl_excel()
    elif etl_type == 'mongo_mysql':
        etl_mongo_mysql()
    else:
        print("Invalid ETL type. Use 'excel' or 'mongo_mysql'.")
        sys.exit(1)