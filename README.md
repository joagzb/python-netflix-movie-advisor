# Overview
A data warehouse definition for recommending movies that can be found on Netflix. This data warehouse will enable data analysis and movies suggestions algorithms. We use various data sources, including MySQL, MongoDB, and Excel files, to build a robust OLAP system.

# Prerequisites
To run this project, you will need the following tools and libraries installed on your system:

- Python 3.x: Make sure you have Python 3.x installed. You can download it from Python's official website.

- MySQL: Install MySQL database server. You can download it from MySQL's official website.

- MongoDB: Install MongoDB database server. You can download it from MongoDB's official website.

- Python Libraries: Install the required Python libraries by running:

```python
pip install pymysql pymongo pandas
```

- .env File: Create a .env file in the root directory of the project to handle MongoDB and MySQL connections. Here is a template:

```
MYSQL_HOST=your_mysql_host
MYSQL_PORT=your_mysql_port
MYSQL_USER=your_mysql_user
MYSQL_PASSWORD=your_mysql_password
MYSQL_DB=your_mysql_db

MONGO_URI=your_mongo_uri
MONGO_DB=your_mongo_db
```

# Repository Structure
- docs: Create a directory for documentation, including tutorials, guides, and technical notes. This keeps documentation organized and easily accessible.
- src: Organize your source code in a directory named src. This includes scripts, configurations, and other files that make up the project.
- tests: Create a directory for test files and scripts to verify the functionality of the project.
- data: Store sample data or data used for testing and development in a directory named data.
- requirements.txt: Include a file listing the dependencies required to run the project.
- .gitignore: Specify which files and directories should be ignored by Git.
- .env: Use a file to store environment variables and configurations.