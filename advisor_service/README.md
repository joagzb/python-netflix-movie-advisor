# 🎬 Movie Recommendation System

This project aims to provide a movie recommendation system using clustering techniques. It involves extracting data from an SQL database, preprocessing the data, training a KMeans model, and providing recommendations based on user IDs or genres.

## Project Structure

```plaintext
advisor_service/
├── docs/
├── notebooks/
├── models/
├── src/
│   ├── __init__.py
│   ├── data_clustering.py
│   ├── data_loading.py
│   ├── data_processing.py
│   ├── db_connection.py
│   ├── training.py
│   ├── recommend_movies.py
│   └── main.py
├── configuration/
│   |── .env
│   └── config.py
├── requirements.txt
└── README.md
```

- `docs/`: Contains docummentation about the project like how to use run it, api version, changing, etc.
- `notebooks/`: Contains Jupyter notebooks
- `models/`: Contains trained models
- `src/`: Contains the source code for data preprocessing, model training, and movie recommendation.
- `configuration/`: Configuration files and environment variables.
- `requirements.txt`: List of required Python libraries.
- `README.md`: Project documentation.

## Prerequisites

Before running the project, ensure you have the following tools and libraries installed:

| Tool/Library      | Description | Link                                |
|-------------------|-------------|-------------------------------------|
| Python 3.x        | Programming language | [Python](https://www.python.org/downloads/)   |
| MySQL             | Database server      | [MySQL](https://dev.mysql.com/downloads/mysql/) |
| Python Libraries  | Required packages    | `pip install -r requirements.txt` |

## Installation Steps

1. **Clone the repository**:

2. **Install Python libraries**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Create a `.env` file** in the configuration directory with the following content:
   ```env
   # MySQL Configuration
   MYSQL_USER=your_mysql_user
   MYSQL_PASSWORD=your_mysql_password
   MYSQL_HOST=your_mysql_host
   MYSQL_PORT=3306  # Default MySQL port
   MYSQL_DATABASE_DW=your_mysql_dw_database
   ```

## Running the Project

### Training the Model

To train the KMeans model and save the results, execute the following command:

```bash
python src/training.py
```

This command will:
1. **Extract** data from the SQL database.
2. **Preprocess** and **transform** the data.
3. **Train** the KMeans model.
4. **Save** the `movies_datacluster` DataFrame with cluster assignments.

### Getting Recommendations

To get movie recommendations based on user ID [0..200] or movie genre [Action, Comedy, ...], use the following command:

```bash
python src/recommend_movies.py --user_id <user_id>
```

or

```bash
python src/recommend_movies.py --genre <genre>
```

This command will:
1. **Load** the precomputed `movies_datacluster` DataFrame.
2. **Recommend** movies based on the specified `user_id` or `genre`.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
