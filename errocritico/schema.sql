DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS posts;

CREATE TABLE users (
  id INTEGER PRIMARY KEY SERIAL,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  surname TEXT NULL,
  location TEXT NULL,
  country TEXT NULL,
  state TEXT NULL,
  zipcode TEXT NULL,
  aboutme TEXT NULL,
  birth TEXT NULL,
  gender TEXT NULL,
  private_profile TEXT NULL,
  private_email TEXT NULL,
  private_zipcode TEXT NULL,
  private_birth TEXT NULL,
  private_gender TEXT NULL
);

CREATE TABLE posts (
  id INTEGER PRIMARY KEY SERIAL,
  author_id INTEGER NOT NULL,
  created DATE NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES users (id)
);
