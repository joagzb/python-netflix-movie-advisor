# 🎬 Movie Recommendation Data Warehouse
This project aims to define a data warehouse for recommending movies available on Netflix. This data warehouse will enable data analysis and movie suggestion algorithms. We use various data sources, including MySQL, MongoDB, and Excel files, to build a robust OLAP system.

The project includes two ETL (Extract, Transform, Load) processes:

- ETL for Loading Data Warehouse from Excel: This process extracts data from Excel files, transforms it, and loads it into the data warehouse.
- ETL for Loading Data Warehouse from OLTP MySQL Database and External MongoDB Source: This process extracts data from an OLTP MySQL database and an external MongoDB source, transforms it, and loads it into the data warehouse.

## Prerequisites
Before running this project, ensure you have the following tools and libraries installed on your system:

| Tool/Library      | Description | Link                                |
|-------------------|-------------|-------------------------------------|
| Python 3.x        | Programming language | [Python](https://www.python.org/downloads/)   |
| MySQL             | Database server      | [MySQL](https://dev.mysql.com/downloads/mysql/) |
| MongoDB           | NoSQL database server | [MongoDB](https://www.mongodb.com/try/download/community) |
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
   MYSQL_PORT=your_mysql_port
   MYSQL_DATABASE_DW=your_mysql_dw_database
   MYSQL_DATABASE_OLTP=your_mysql_oltp_database

   # MongoDB Configuration
   MONGODB_USERNAME=your_mongodb_username
   MONGODB_PASSWORD=your_mongodb_password
   MONGODB_HOST=your_mongodb_host
   MONGODB_CLUSTER_NAME=your_mongodb_cluster_name
   ```

## Repository Structure

```plaintext
data_warehouse/
├── configuration/
│   ├── __init__.py
│   ├── .env
│   └── config.py
├── data/
├── docs/
├── notebooks/
│   └── etl_notebook.ipynb
├── sql/
├── src/
│   ├── __init__.py
│   ├── extract.py
│   ├── transform.py
│   └── load.py
├── requirements.txt
└── README.md
```

- `configuration/`: Configuration files and environment variables.
- `data/`: raw or preprocessed data to use in the ETL process
- `docs/`: Contains docummentation about the project like how to use run it, api version, changing, etc.
- `notebooks/`: Contains Jupyter notebooks
- `sql/`: DDL and DML to load and seed data warehouse
- `src/`: Contains the source code for extracting, transforming, and loading data.
- `requirements.txt`: List of required Python libraries.
- `README.md`: Project documentation.

The `src` directory is a proper Python package (it includes an `__init__.py` file),
which allows modules inside it to be imported directly without using `src.`
prefixes. Ensure you execute commands from the `data_warehouse` directory so
these imports resolve correctly.

## Running the ETL Process

To run the ETL process, execute the following command:

```bash
python src/main.py excel
```
or
```bash
python src/main.py mongo_mysql
```

This command will:
1. **Extract** data from MySQL and MongoDB.
2. **Transform** the data according to defined business rules.
3. **Load** the data into the data warehouse.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
