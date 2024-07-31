import pandas as pd
from sklearn.cluster import KMeans

def run_clustering(df, n_clusters):
    tabla_model = pd.pivot_table(df, values='score', index=['userID'], columns=['genre'], aggfunc="mean").reset_index()

    X1 = tabla_model.fillna(0).iloc[:, 1:].values
    predictions = train_model(X1,n_clusters)

    tabla_model['Cluster'] = predictions
    return tabla_model


def train_model(adj_matrix,n_clusters):
  kmeans = KMeans(n_clusters=n_clusters, random_state=0)
  kmeans.fit_predict(adj_matrix)
  return kmeans
