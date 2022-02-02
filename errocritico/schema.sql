DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS posts;

CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  surname TEXT,
  location TEXT,
  country TEXT,
  state TEXT,
  zipcode TEXT,
  aboutme TEXT,
  birth TEXT,
  gender TEXT,
  private_profile TEXT,
  private_email TEXT,
  private_zipcode TEXT,
  private_birth TEXT,
  private_gender TEXT
);

CREATE TABLE posts (
  id SERIAL PRIMARY KEY,
  author_id INTEGER NOT NULL,
  created DATE NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES users (id)
);
