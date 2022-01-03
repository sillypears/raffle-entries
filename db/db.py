from flask import g
import psycopg2

def get_db(conf):
    db = psycopg2.connect(
        user = conf.DATABASE_USER,
        password = conf.DATABASE_PASS,
        database = conf.DATABASE_SCHEMA,
        port = conf.DATABASE_PORT,
        host= conf.DATABASE_HOST,
        
        )
    db.autocommit = True
    return db

def close_db(db, conf):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def get_makers(db, conf):
    cur = db.cursor()
    cur.execute("SELECT id, name, display FROM makers")
    return cur

def get_maker(db, id, conf):
    cur = db.cursor()
    cur.execute(f"SELECT id, name, display FROM makers WHERE id = {id}")
    return cur

def get_entries(db, conf):
    cur = db.cursor()
    cur.execute("SELECT * FROM all_entries ORDER BY epoch, id ASC")
    return cur

def get_entry(db, id, conf):
    cur = db.cursor()
    cur.execute(f"SELECT * FROM all_entries WHERE id = {id}")
    return cur

def add_entry(db, data, conf):
    cur = db.cursor()
    cur.execute(f"INSERT INTO entries (maker_id, epoch, date, raffle_link, notes, result) VALUES ({data['maker_id']}, {data['epoch']}, '{data['date']}', '{data['link']}', '{data['notes']}', {data['result']}) RETURNING id")
    return cur

def add_maker(db, data, conf):
    cur = db.cursor()
    cur.execute(f"INSERT INTO makers (name, display) VALUES ('{data['name']}', '{data['display']}') RETURNING id")
    return cur

def toggle_entry(db, data, conf):
    result = False if data['result'] else True
    print(type(data['result']), data['result'], result)
    cur = db.cursor()
    cur.execute(f"UPDATE entries SET result={result} WHERE id = {data['id']} RETURNING id")
    return cur

def get_percents(db, conf):
    cur = db.cursor()
    cur.execute(f"SELECT result, COUNT(result) FROM entries GROUP BY result")
    return cur