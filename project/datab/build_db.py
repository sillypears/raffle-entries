import psycopg2
from psycopg2 import sql
from urllib.parse import urlparse
from os import environ as env
import sys
from time import sleep
from datetime import datetime

def main(conf):
    sqlDropDatabase = f"""DROP DATABASE IF EXISTS {conf.DATABASE_SCHEMA};"""
    sqlCreateDatabase = f"""CREATE DATABASE {conf.DATABASE_SCHEMA};"""
    sqlGrantDatabase = f"""GRANT ALL ON DATABASE {conf.DATABASE_SCHEMA} TO pg_database_owner;"""
    sqlCreateUsers = f"""CREATE TABLE public.users
    (
        id serial NOT NULL,
        name character varying(100) NOT NULL,
        password character varying(500) NOT NULL
    );"""
    sqlCreateMakers = f"""CREATE TABLE IF NOT EXISTS makers
    (
        id serial NOT NULL,
        name character varying(50) COLLATE pg_catalog."default" NOT NULL,
        display character varying(200) COLLATE pg_catalog."default" NOT NULL,
        instagram character varying(200) COLLATE pg_catalog."default",
        CONSTRAINT makers_pkey PRIMARY KEY (id)
    )"""

    sqlCreateEntries = f"""CREATE TABLE IF NOT EXISTS entries
    (
        id serial NOT NULL,
        user_id integer NOT NULL, 
        maker_id integer NOT NULL,
        epoch integer NOT NULL,
        raffle_link character varying(500) COLLATE pg_catalog."default" NOT NULL,
        notes text COLLATE pg_catalog."default",
        result boolean NOT NULL DEFAULT false,
        date date NOT NULL,
        CONSTRAINT entries_pkey PRIMARY KEY (id),
        CONSTRAINT user_id_fkey FOREIGN KEY (user_id)
            REFERENCES public.users (id) MATCH SIMPLE
            ON UPDATE NO ACTION
            ON DELETE NO ACTION
        CONSTRAINT maker_id_fkey FOREIGN KEY (maker_id)
            REFERENCES public.makers (id) MATCH SIMPLE
            ON UPDATE NO ACTION
            ON DELETE NO ACTION
    )"""

    sqlCreateView = f"""CREATE OR REPLACE VIEW all_entries
    AS
    SELECT m.display AS maker,
        e.result,
        e.epoch,
        e.date,
        e.notes,
        e.raffle_link AS info,
        e.id,
        m.id AS "maker id",
        m.instagram
    FROM entries e
        LEFT JOIN makers m ON e.maker_id = m.id;"""

    sqlAddUsers = f"""
        INSERT INTO users (name, password) VALUES ('user1', 'sha256$RBFTAYLKjqbXxlXt$40088c30c40ec938c5427b2bca21ea304a06209518dc30795ec8231fdbdfb644');
        INSERT INTO users (name, password) VALUES ('user1', 'sha256$RBFTAYLKjqbXxlXt$40088c30c40ec938c5427b2bca21ea304a06209518dc30795ec8231fdbdfb644');

    """
    sqlAddMakers = f"""
        INSERT INTO makers (name, display, instagram) VALUES ('test1', 'Test 1', 'test.1');
        INSERT INTO makers (name, display, instagram) VALUES ('test2', 'Test 2', 'test.2');
        INSERT INTO makers (name, display, instagram) VALUES ('test3', 'Test 3', 'test.3');
        INSERT INTO makers (name, display, instagram) VALUES ('test4', 'Test 4', 'test.4');
        INSERT INTO makers (name, display, instagram) VALUES ('test5', 'Test 5', 'test.5');
    """

    sqlAddEntries = f"""
        INSERT INTO entries (user_id, maker_id, epoch, raffle_link, notes, result, date, user_id) VALUES (1, 1, {int(datetime.now().timestamp())}, 'https://frms.gle/test1', 'raffle for test1', false, '{datetime.now().strftime('%Y-%m-%d')}', 1);
        INSERT INTO entries (user_id, maker_id, epoch, raffle_link, notes, result, date, user_id) VALUES (1, 2, {int(datetime.now().timestamp())}, 'https://frms.gle/test2', 'raffle for test2', false, '{datetime.now().strftime('%Y-%m-%d')}', 1);
        INSERT INTO entries (user_id, maker_id, epoch, raffle_link, notes, result, date, user_id) VALUES (2, 3, {int(datetime.now().timestamp())}, 'https://frms.gle/test3', 'raffle for test3', true, '{datetime.now().strftime('%Y-%m-%d')}', 1);
        INSERT INTO entries (user_id, maker_id, epoch, raffle_link, notes, result, date, user_id) VALUES (1, 2, {int(datetime.now().timestamp())}, 'https://frms.gle/test4', 'raffle for test4', false, '{datetime.now().strftime('%Y-%m-%d')}', 1);
        INSERT INTO entries (user_id, maker_id, epoch, raffle_link, notes, result, date, user_id) VALUES (2, 4, {int(datetime.now().timestamp())}, 'https://frms.gle/test5', 'raffle for test5', true, '{datetime.now().strftime('%Y-%m-%d')}', 1);
        INSERT INTO entries (user_id, maker_id, epoch, raffle_link, notes, result, date, user_id) VALUES (2, 4, {int(datetime.now().timestamp())}, 'https://frms.gle/test6', 'raffle for test6', false, '{datetime.now().strftime('%Y-%m-%d')}', 1);
        INSERT INTO entries (user_id, maker_id, epoch, raffle_link, notes, result, date, user_id) VALUES (1, 2, {int(datetime.now().timestamp())}, 'https://frms.gle/test7', 'raffle for test7', false, '{datetime.now().strftime('%Y-%m-%d')}', 1);
        INSERT INTO entries (user_id, maker_id, epoch, raffle_link, notes, result, date, user_id) VALUES (1, 5, {int(datetime.now().timestamp())}, 'https://frms.gle/test8', 'raffle for test8', true, '{datetime.now().strftime('%Y-%m-%d')}', 1);
        INSERT INTO entries (user_id, maker_id, epoch, raffle_link, notes, result, date, user_id) VALUES (2, 1, {int(datetime.now().timestamp())}, 'https://frms.gle/test9', 'raffle for test9', true, '{datetime.now().strftime('%Y-%m-%d')}', 2);
        INSERT INTO entries (user_id, maker_id, epoch, raffle_link, notes, result, date, user_id) VALUES (2, 2, {int(datetime.now().timestamp())}, 'https://frms.gle/test10', 'raffle for test10', false, '{datetime.now().strftime('%Y-%m-%d')}', 2);
        INSERT INTO entries (user_id, maker_id, epoch, raffle_link, notes, result, date, user_id) VALUES (1, 3, {int(datetime.now().timestamp())}, 'https://frms.gle/test11', 'raffle for test11', false, '{datetime.now().strftime('%Y-%m-%d')}', 1);
        INSERT INTO entries (user_id, maker_id, epoch, raffle_link, notes, result, date, user_id) VALUES (1, 2, {int(datetime.now().timestamp())}, 'https://frms.gle/test11', 'raffle for test12', false, '{datetime.now().strftime('%Y-%m-%d')}', 1);
        INSERT INTO entries (user_id, maker_id, epoch, raffle_link, notes, result, date, user_id) VALUES (1, 4, {int(datetime.now().timestamp())}, 'https://frms.gle/test11', 'raffle for test13', false, '{datetime.now().strftime('%Y-%m-%d')}', 2);
        INSERT INTO entries (user_id, maker_id, epoch, raffle_link, notes, result, date, user_id) VALUES (1, 3, {int(datetime.now().timestamp())}, 'https://frms.gle/test11', 'raffle for test14', false, '{datetime.now().strftime('%Y-%m-%d')}', 1);
        INSERT INTO entries (user_id, maker_id, epoch, raffle_link, notes, result, date, user_id) VALUES (1, 2, {int(datetime.now().timestamp())}, 'https://frms.gle/test11', 'raffle for test15', false, '{datetime.now().strftime('%Y-%m-%d')}', 1);
        INSERT INTO entries (user_id, maker_id, epoch, raffle_link, notes, result, date, user_id) VALUES (1, 3, {int(datetime.now().timestamp())}, 'https://frms.gle/test11', 'raffle for test16', false, '{datetime.now().strftime('%Y-%m-%d')}', 1);
        INSERT INTO entries (user_id, maker_id, epoch, raffle_link, notes, result, date, user_id) VALUES (1, 2, {int(datetime.now().timestamp())}, 'https://frms.gle/test11', 'raffle for test17', false, '{datetime.now().strftime('%Y-%m-%d')}', 1);
        INSERT INTO entries (user_id, maker_id, epoch, raffle_link, notes, result, date, user_id) VALUES (1, 2, {int(datetime.now().timestamp())}, 'https://frms.gle/test11', 'raffle for test18', false, '{datetime.now().strftime('%Y-%m-%d')}', 1);
        INSERT INTO entries (user_id, maker_id, epoch, raffle_link, notes, result, date, user_id) VALUES (1, 5, {int(datetime.now().timestamp())}, 'https://frms.gle/test11', 'raffle for test19', false, '{datetime.now().strftime('%Y-%m-%d')}', 1);
        INSERT INTO entries (user_id, maker_id, epoch, raffle_link, notes, result, date, user_id) VALUES (1, 3, {int(datetime.now().timestamp())}, 'https://frms.gle/test11', 'raffle for test20', false, '{datetime.now().strftime('%Y-%m-%d')}', 1);
        INSERT INTO entries (user_id, maker_id, epoch, raffle_link, notes, result, date, user_id) VALUES (1, 2, {int(datetime.now().timestamp())}, 'https://frms.gle/test11', 'raffle for test21', false, '{datetime.now().strftime('%Y-%m-%d')}', 1);
        INSERT INTO entries (user_id, maker_id, epoch, raffle_link, notes, result, date, user_id) VALUES (1, 3, {int(datetime.now().timestamp())}, 'https://frms.gle/test11', 'raffle for test22', false, '{datetime.now().strftime('%Y-%m-%d')}', 1);
        INSERT INTO entries (user_id, maker_id, epoch, raffle_link, notes, result, date, user_id) VALUES (1, 2, {int(datetime.now().timestamp())}, 'https://frms.gle/test11', 'raffle for test23', false, '{datetime.now().strftime('%Y-%m-%d')}', 1);
        INSERT INTO entries (user_id, maker_id, epoch, raffle_link, notes, result, date, user_id) VALUES (1, 5, {int(datetime.now().timestamp())}, 'https://frms.gle/test11', 'raffle for test24', false, '{datetime.now().strftime('%Y-%m-%d')}', 1);
        INSERT INTO entries (user_id, maker_id, epoch, raffle_link, notes, result, date, user_id) VALUES (1, 3, {int(datetime.now().timestamp())}, 'https://frms.gle/test11', 'raffle for test25', false, '{datetime.now().strftime('%Y-%m-%d')}', 1);
        INSERT INTO entries (user_id, maker_id, epoch, raffle_link, notes, result, date, user_id) VALUES (1, 4, {int(datetime.now().timestamp())}, 'https://frms.gle/test11', 'raffle for test26', false, '{datetime.now().strftime('%Y-%m-%d')}', 1);
        INSERT INTO entries (user_id, maker_id, epoch, raffle_link, notes, result, date, user_id) VALUES (1, 4, {int(datetime.now().timestamp())}, 'https://frms.gle/test11', 'raffle for test27', false, '{datetime.now().strftime('%Y-%m-%d')}', 1);
        INSERT INTO entries (user_id, maker_id, epoch, raffle_link, notes, result, date, user_id) VALUES (1, 3, {int(datetime.now().timestamp())}, 'https://frms.gle/test11', 'raffle for test28', false, '{datetime.now().strftime('%Y-%m-%d')}', 1);
        INSERT INTO entries (user_id, maker_id, epoch, raffle_link, notes, result, date, user_id) VALUES (1, 5, {int(datetime.now().timestamp())}, 'https://frms.gle/test11', 'raffle for test29', false, '{datetime.now().strftime('%Y-%m-%d')}', 1);
        INSERT INTO entries (user_id, maker_id, epoch, raffle_link, notes, result, date, user_id) VALUES (1, 3, {int(datetime.now().timestamp())}, 'https://frms.gle/test11', 'raffle for test30', false, '{datetime.now().strftime('%Y-%m-%d')}', 1);
        INSERT INTO entries (user_id, maker_id, epoch, raffle_link, notes, result, date, user_id) VALUES (1, 2, {int(datetime.now().timestamp())}, 'https://frms.gle/test11', 'raffle for test31', false, '{datetime.now().strftime('%Y-%m-%d')}', 1);
        INSERT INTO entries (user_id, maker_id, epoch, raffle_link, notes, result, date, user_id) VALUES (1, 2, {int(datetime.now().timestamp())}, 'https://frms.gle/test11', 'raffle for test32', false, '{datetime.now().strftime('%Y-%m-%d')}', 1);
        INSERT INTO entries (user_id, maker_id, epoch, raffle_link, notes, result, date, user_id) VALUES (1, 3, {int(datetime.now().timestamp())}, 'https://frms.gle/test11', 'raffle for test33', false, '{datetime.now().strftime('%Y-%m-%d')}', 1);
        INSERT INTO entries (user_id, maker_id, epoch, raffle_link, notes, result, date, user_id) VALUES (1, 3, {int(datetime.now().timestamp())}, 'https://frms.gle/test11', 'raffle for test34', false, '{datetime.now().strftime('%Y-%m-%d')}', 1);
        INSERT INTO entries (user_id, maker_id, epoch, raffle_link, notes, result, date, user_id) VALUES (1, 2, {int(datetime.now().timestamp())}, 'https://frms.gle/test11', 'raffle for test35', false, '{datetime.now().strftime('%Y-%m-%d')}', 1);
        INSERT INTO entries (user_id, maker_id, epoch, raffle_link, notes, result, date, user_id) VALUES (1, 2, {int(datetime.now().timestamp())}, 'https://frms.gle/test11', 'raffle for test36', false, '{datetime.now().strftime('%Y-%m-%d')}', 1);
        INSERT INTO entries (user_id, maker_id, epoch, raffle_link, notes, result, date, user_id) VALUES (1, 3, {int(datetime.now().timestamp())}, 'https://frms.gle/test11', 'raffle for test37', false, '{datetime.now().strftime('%Y-%m-%d')}', 1);
    """

    con = psycopg2.connect(
        user=conf.DATABASE_USER,
        password=conf.DATABASE_PASS,
        port=conf.DATABASE_PORT,
        host=conf.DATABASE_HOST,
    )
    try:
        con.autocommit = True
        cur = con.cursor()
        cur.execute(sql.SQL(sqlDropDatabase))
        cur.execute(sql.SQL(sqlCreateDatabase))
        cur.execute(sql.SQL(sqlGrantDatabase))
        cur.close()
        con = psycopg2.connect(
            user=conf.DATABASE_USER,
            password=conf.DATABASE_PASS,
            port=conf.DATABASE_PORT,
            host=conf.DATABASE_HOST,
            database=conf.DATABASE_SCHEMA
        )
        con.autocommit = True
        cur = con.cursor()
        cur.execute(sql.SQL(sqlCreateUsers))
        cur.execute(sql.SQL(sqlCreateMakers))
        cur.execute(sql.SQL(sqlCreateEntries))
        cur.execute(sql.SQL(sqlCreateView))
        if (conf.DEBUG):
            cur.execute(sql.SQL(sqlAddUsers))
            cur.execute(sql.SQL(sqlAddMakers))
            cur.execute(sql.SQL(sqlAddEntries))
        con.close()
    except:
        con.close()
        con = psycopg2.connect(
            user=conf.DATABASE_USER,
            password=conf.DATABASE_PASS,
            port=conf.DATABASE_PORT,
            host=conf.DATABASE_HOST,
        )
        con.cursor().execute(sql.SQL(f"DROP DATABASE IF EXISTS {conf.DATABASE_SCHEMA}"))
        sys.exit(1)
    print("Database created")


if __name__ == "__main__":
    url = urlparse(env.get('DATABASE_URL'))

    class Config(object):
        def __init__(self):
            self.DEBUG = env.get('FLASK_DEBUG')
            self.DATABASE_HOST = url.hostname
            self.DATABASE_PORT = url.port
            self.DATABASE_USER = url.username
            self.DATABASE_PASS = url.password
            self.DATABASE_SCHEMA = url.path[1:]

        def __str__(self):
            return f"{self.DATABASE_HOST}, {self.DATABASE_PORT}, {self.DATABASE_SCHEMA}, {self.DATABASE_USER}"
    conf = Config()
    print(conf)
    sys.exit(main(conf))
