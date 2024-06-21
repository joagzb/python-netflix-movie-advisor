/* Creating a new database dw_netflix for the data warehouse */
CREATE DATABASE IF NOT EXISTS dw_netflix;
USE dw_netflix;

/* Create the table dimMovie */
CREATE TABLE dimMovie (
    movieID VARCHAR(8) PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    releaseDate DATE,
    genre VARCHAR(100),
    award VARCHAR(20)
);

/* Create the table dimUser */
CREATE TABLE dimUser (
    userID INTEGER PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    country VARCHAR(50)
);

/* Create the table dimPerformer */
CREATE TABLE dimPerformer (
    performerID INTEGER PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    role VARCHAR(50),
    award VARCHAR(50)
);

/* Create the table dimInteraction */
CREATE TABLE dimInteraction (
    interactionID INTEGER PRIMARY KEY,
    finishCount INTEGER,
    backClickCount INTEGER,
    movieForwardCount INTEGER,
    playCount INTEGER,
    movieViewPercentage DECIMAL(4,2)
);

/* Create the table dimScore */
CREATE TABLE dimScore (
    scoreID INTEGER PRIMARY KEY,
    netflixScore DECIMAL(4,2),
    imdbScore DECIMAL(4,2),
    rottentomatoesScore DECIMAL(4,2),
    sensacineScore DECIMAL(4,2),
    peopleScore DECIMAL(4,2),
    peopleComment VARCHAR(255)
);

/* Create the table FactWatchs */
CREATE TABLE FactWatchs (
    id INTEGER PRIMARY KEY,
    userID INTEGER,
    movieID VARCHAR(8),
    performerID INTEGER,
    interactionID INTEGER,
    scoreID INTEGER,
    watchDate TIMESTAMP,

    /* Creating relationships */
    CONSTRAINT fk_factwatchs_movie FOREIGN KEY (movieID) REFERENCES dimMovie (movieID),
    CONSTRAINT fk_factwatchs_user FOREIGN KEY (userID) REFERENCES dimUser (userID),
    CONSTRAINT fk_factwatchs_performer FOREIGN KEY (performerID) REFERENCES dimPerformer (performerID),
    CONSTRAINT fk_factwatchs_interaction FOREIGN KEY (interactionID) REFERENCES dimInteraction (interactionID),
    CONSTRAINT fk_factwatchs_score FOREIGN KEY (scoreID) REFERENCES dimScore (scoreID)
);
