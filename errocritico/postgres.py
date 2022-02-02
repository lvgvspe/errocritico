import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']

db = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = db.cursor()
with open('schema.sql') as f:
    cursor.execute(f.read())
db.commit()
