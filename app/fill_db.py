import psycopg2
import os

conn = psycopg2.connect(
        host="localhost",
        database="iis",
        user=os.environ['iis'],
        password=os.environ['chob0t3k'])

cur = conn.cursor()

cur.execute('TRUNCATE TABLE IF EXISTS course;')
cur.execute('TRUNCATE TABLE IF EXISTS user;')
cur.execute('TRUNCATE TABLE IF EXISTS news;')
cur.execute('TRUNCATE TABLE IF EXISTS term;')

cur.execute('INSERT INTO course')
