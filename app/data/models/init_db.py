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


def course_lec(l_id, c_id):
    cur.execute('INSERT INTO course_lecturers (user_id, course_id)'
                'VALUES (%s, %s)',
                (l_id, c_id)
                )
    return


def course_student(s_id, c_id):
    cur.execute('INSERT INTO course_students (user_id, course_id)'
                'VALUES (%s, %s)',
                (s_id, c_id)
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
insert_user('xkokot01', hash_pas(123), datetime.datetime.utcnow(), True, False)
insert_user('xkokot02', hash_pas(123), datetime.datetime.utcnow(), True, False)
insert_user('xkokot03', hash_pas(123), datetime.datetime.utcnow(), True, False)
insert_user('xkokot04', hash_pas(123), datetime.datetime.utcnow(), True, True)
insert_user('xkokot05', hash_pas(123), datetime.datetime.utcnow(), True, False)
insert_user('xkokot06', hash_pas(123), datetime.datetime.utcnow(), True, False)
insert_user('xkokot07', hash_pas(123), datetime.datetime.utcnow(), True, False)
insert_user('xkokot08', hash_pas(123), datetime.datetime.utcnow(), True, True)
insert_user('xkokot09', hash_pas(123), datetime.datetime.utcnow(), True, False)
insert_user('xkokot10', hash_pas(123), datetime.datetime.utcnow(), True, False)
insert_user('xkokot11', hash_pas(123), datetime.datetime.utcnow(), False, False)

insert_course('iis', 'NEJLEPSI predmet na FITu', 'prezencni', 500, 15, 1)
insert_course('ims', 'druhy NEJLEPSI predmet na FITu', 'prezencni', 500, 15, 2)
insert_course('isa', 'ze vsech NEJLEPSI predmet na FITu', 'prezencni', 500, 15, 1)

course_lec(1, 1)
course_lec(2, 1)
course_lec(3, 1)

course_student(4, 1)
course_student(5, 1)
course_student(4, 2)
course_student(4, 3)

course_lec(2, 2)
course_lec(2, 3)

conn.commit()
cur.close()
conn.close()
