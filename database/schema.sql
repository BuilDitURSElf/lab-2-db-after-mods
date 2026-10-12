-- Lab 2: database for the Login & To-Do application.
-- Re-runnable: it drops and recreates everything. Contains no data.

DROP DATABASE IF EXISTS registration;
CREATE DATABASE registration;
USE registration;

-- Table 1: users (must be created first, todos points at it)
CREATE TABLE users (
    user_id           INT          NOT NULL AUTO_INCREMENT,
    email             VARCHAR(255) NOT NULL,
    name              VARCHAR(100) NOT NULL,
    password_hash     VARCHAR(255) NOT NULL,
    registration_date TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id),
    UNIQUE (email)
);

-- Table 2: todos (one user has many to-dos, each to-do has exactly one user)
CREATE TABLE todos (
    todo_id    INT          NOT NULL AUTO_INCREMENT,
    user_id    INT          NOT NULL,
    title      VARCHAR(200) NOT NULL,
    is_done    TINYINT(1)   NOT NULL DEFAULT 0,
    due_date   DATE         NULL,          -- [Bonus: due dates] optional
    created_at TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (todo_id),
    FOREIGN KEY (user_id) REFERENCES users (user_id)
);
