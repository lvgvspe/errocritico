DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;

CREATE TABLE user (
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

CREATE TABLE post (
  id INTEGER PRIMARY KEY SERIAL,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);