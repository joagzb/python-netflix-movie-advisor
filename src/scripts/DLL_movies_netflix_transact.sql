/* CREATE TABLE Movie */
CREATE TABLE Movie (
    movieID VARCHAR(8) PRIMARY KEY NOT NULL,
    movieTitle VARCHAR(100) NOT NULL,
    releaseDate DATE NOT NULL,
    originalLanguage VARCHAR(100) DEFAULT NULL,
    link VARCHAR(50) DEFAULT NULL
);

/* CREATE TABLE Genre */
CREATE TABLE Genre (
    genreID INTEGER PRIMARY KEY NOT NULL,
    name VARCHAR(100) NOT NULL
);

/* CREATE TABLE Person */
CREATE TABLE Person (
    personID VARCHAR(8) PRIMARY KEY NOT NULL,
    name VARCHAR(100) NOT NULL,
    birthday DATE NOT NULL
);

/* CREATE TABLE Performer */
CREATE TABLE Performer (
    performerID VARCHAR(8) PRIMARY KEY NOT NULL,
    movieID VARCHAR(8) NOT NULL,
    personID VARCHAR(8),
    performerRole VARCHAR(30),
    CONSTRAINT fk_movie_performer FOREIGN KEY (movieID) REFERENCES Movie (movieID),
    CONSTRAINT fk_person_performer FOREIGN KEY (personID) REFERENCES Person (personID)
);

/* CREATE TABLE Movie_Genre */
CREATE TABLE Movie_Genre (
    movieGenreID VARCHAR(8) PRIMARY KEY NOT NULL,
    movieID VARCHAR(8) NOT NULL,
    genreID INTEGER,
    CONSTRAINT fk_movie_genre_movie FOREIGN KEY (movieID) REFERENCES Movie (movieID),
    CONSTRAINT fk_movie_genre_genre FOREIGN KEY (genreID) REFERENCES Genre (genreID)
);
