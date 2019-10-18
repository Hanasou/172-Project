CREATE TABLE users(
    id INTEGER NOT NULL AUTO_INCREMENT,
    username VARCHAR(64) NOT NULL UNIQUE,
    password VARCHAR(128) NOT NULL,
    first_name VARCHAR(64) NOT NULL,
    last_name VARCHAR(64) NOT NULL,
    admin BOOLEAN,
    PRIMARY KEY (id)
);

CREATE TABLE files(
    id INTEGER NOT NULL AUTO_INCREMENT,
    item VARCHAR(64) NOT NULL,
    user_fn VARCHAR(64) NOT NULL,
    user_ln VARCHAR(64) NOT NULL,
    upload_date TIMESTAMP NOT NULL,
    update_date TIMESTAMP NOT NULL,
    description VARCHAR(100),
    user_id INTEGER NOT NULL, 
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES users (id)
);