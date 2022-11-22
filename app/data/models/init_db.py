import os
import psycopg2
import datetime
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()


def trunc_tables():
    cur.execute('TRUNCATE TABLE public.course, public.news, public.term, public.user RESTART IDENTITY CASCADE;')
    return


def trunc_table(table):
    cur.execute('TRUNCATE TABLE table RESTART IDENTITY CASCADE;')
    return


def hash_pas(pwd):
    hasish = bcrypt.generate_password_hash(str(pwd)).decode('utf-8')
    return hasish


def insert_course(abbr, descr, type, price, capacity, guarantor):
    cur.execute('INSERT INTO public.course (abbreviation, description, type, price, capacity, guarantor)'
                'VALUES (%s, %s, %s, %s, %s, %s)',
                (abbr, descr, type, price, capacity, guarantor)
                )
    return


def insert_news(course, msg):
    cur.execute('INSERT INTO public.news (dourse, da_newz)'
                'VALUES (%s, %s)',
                (course, msg)
                )
    return


def insert_terms(course, name, t_type, descr, date, room, rath):
    cur.execute('INSERT INTO public.term (course, name, type, description, date, room, rathing)'
                'VALUES (%s, %s, %s, %s, %s, %s)',
                (course, name, t_type, descr, date, room, rath)
                )
    return


def insert_user(username, pw_hash, created_ts, is_active, is_admin):
    cur.execute('INSERT INTO public.user (username, pw_hash, created_ts, is_active, is_admin)'
                'VALUES (%s, %s, %s, %s, %s)',
                (username, pw_hash, created_ts, is_active, is_admin)
                )
    return


conn = psycopg2.connect(
    host="localhost",
    database="iis",
    user='iis',
    password='chob0t3k')

cur = conn.cursor()

trunc_tables()
insert_user('xkokot00', hash_pas(123), datetime.datetime.utcnow(), True, True)
insert_user('xkokot01', hash_pas(234), datetime.datetime.utcnow(), True, False)
insert_user('xkokot02', hash_pas(345), datetime.datetime.utcnow(), True, False)
insert_user('xkokot03', hash_pas(456), datetime.datetime.utcnow(), False, False)

insert_course('iis', 'NEJLEPSI predmet na FITu', 'prezencni', 500, 15, 1)
insert_course('ims', 'druhy NEJLEPSI predmet na FITu', 'prezencni', 500, 15, 2)
insert_course('isa', 'ze vsech NEJLEPSI predmet na FITu', 'prezencni', 500, 15, 1)

conn.commit()
cur.close()
conn.close()
