import psycopg2
import datetime
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()


def trunc_tables():
    cur.execute('TRUNCATE TABLE public.course, public.news, public.term, public.user, public.term_body, public.study_request, public.course_request, public.course_students, public.course_lecturers RESTART IDENTITY CASCADE;')
    return


def trunc_table(table):
    cur.execute('TRUNCATE TABLE table RESTART IDENTITY CASCADE;')
    return


def hash_pas(pwd):
    hasish = bcrypt.generate_password_hash(str(pwd)).decode('utf-8')
    return hasish


def insert_course(abbr, descr, type, price, capacity, guarantor, auto_accept):
    cur.execute('INSERT INTO public.course (abbreviation, description, type, price, capacity, guarantor, auto_accept_students)'
                'VALUES (%s, %s, %s, %s, %s, %s, %s)',
                (abbr, descr, type, price, capacity, guarantor, auto_accept)
                )
    return


def insert_news(course, msg):
    cur.execute('INSERT INTO public.news (dourse, da_newz)'
                'VALUES (%s, %s)',
                (course, msg)
                )
    return


def insert_terms(course, name, t_type, descr, date, room, rath):
    cur.execute('INSERT INTO public.term (course, name, type, description, date, room, max_body)'
                'VALUES (%s, %s, %s, %s, %s, %s, %s)',
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


def insert_news(course, da_newz, created_ts):
    cur.execute('INSERT INTO news (course, da_newz, created_ts)'
                'VALUES (%s, %s, %s)',
                (course, da_newz, created_ts)
                )


conn = psycopg2.connect(
    host="localhost",
    database="iis",
    user='iis',
    password='chob0t3k')

cur = conn.cursor()

trunc_tables()

insert_user('xlogin00', hash_pas(123), datetime.datetime.utcnow(), True, True)
insert_user('xlogin01', hash_pas(123), datetime.datetime.utcnow(), True, False)
insert_user('xlogin02', hash_pas(123), datetime.datetime.utcnow(), True, False)
insert_user('xlogin03', hash_pas(123), datetime.datetime.utcnow(), True, False)
insert_user('xlogin04', hash_pas(123), datetime.datetime.utcnow(), True, False)
insert_user('xlogin05', hash_pas(123), datetime.datetime.utcnow(), True, False)
insert_user('xlogin06', hash_pas(123), datetime.datetime.utcnow(), True, False)
insert_user('xlogin07', hash_pas(123), datetime.datetime.utcnow(), True, False)
insert_user('xlogin08', hash_pas(123), datetime.datetime.utcnow(), True, False)
insert_user('xlogin09', hash_pas(123), datetime.datetime.utcnow(), True, False)
insert_user('xlogin10', hash_pas(123), datetime.datetime.utcnow(), True, False)
insert_user('xlogin11', hash_pas(123), datetime.datetime.utcnow(), False, False)

insert_course('iis', 'NEJLEPSI predmet na FITu', 'prezencni', 500, 15, 1, False)
insert_course('ims', 'druhy NEJLEPSI predmet na FITu', 'prezencni', 500, 15, 2, True)
insert_course('isa', 'ze vsech NEJLEPSI predmet na FITu', 'prezencni', 500, 15, 1, False)

course_lec(1, 1)
course_lec(2, 1)
course_lec(3, 1)

course_student(4, 1)
course_student(5, 1)
course_student(4, 2)
course_student(4, 3)

course_lec(2, 2)
course_lec(2, 3)

insert_news(1, 'Ok zacnete delat projekt', datetime.datetime.now() - datetime.timedelta(days=2))
insert_news(2, '========================', datetime.datetime.now() - datetime.timedelta(days=1))
insert_news(1, 'Pls mejte v tom projektu dokumentaci', datetime.datetime.now())

insert_terms('1', 'projekt', 'projekt','informacny system', datetime.datetime.now(), 'izba tvojej mamy', '69')

conn.commit()
cur.close()
conn.close()
