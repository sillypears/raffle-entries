from flask import g
import psycopg2
from datetime import datetime
import re, json

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
    cur.execute("SELECT id, name, display, instagram FROM makers ORDER BY name ASC")
    return cur

def get_maker(db, id, conf):
    cur = db.cursor()
    cur.execute(f"SELECT id, name, display, instagram FROM makers WHERE id = {id}")
    return cur

def get_entries(db, conf):
    cur = db.cursor()
    cur.execute("SELECT * FROM all_entries ORDER BY epoch DESC, id DESC")
    return cur

def get_entries_by_maker(db, id, conf):
    cur = db.cursor()
    cur.execute(f"SELECT * FROM all_entries WHERE mid = {id} ORDER BY epoch, id ")
    return cur

def get_entry(db, id, conf):
    cur = db.cursor()
    cur.execute(f"SELECT * FROM all_entries WHERE id = {id}")
    return cur

def add_entry(db, data, conf):
    cur = db.cursor()
    cur.execute(f"""INSERT INTO entries (maker_id, epoch, date, raffle_link, notes, result) VALUES ({data['maker_id']}, {data['epoch']}, '{data['date']}', '{data['link'].replace("'","''")}', '{data['notes'].replace("'","''")}', {data['result']}) RETURNING id""")
    return cur

def update_entry(db, id, data, conf):
    try:
        result = True if data['result'] == 'on' else True
    except:
        result = False
    cur = db.cursor()
    cur.execute(f"""UPDATE entries SET maker_id={data['maker']}, epoch={int(datetime.fromisoformat(data['date']).timestamp())}, date='{data['date']}', raffle_link='{data['link'].replace("'","''")}', notes='{data['notes'].replace("'","''")}', result={result} WHERE id={id}""")
    return cur

def add_maker(db, data, conf):
    cur = db.cursor()
    cur.execute(f"INSERT INTO makers (name, display, instagram) VALUES ('{data['name']}', '{data['display']}', '{data['instagram']}') RETURNING id")
    return cur

def update_maker(db, id, data, conf):
    cur = db.cursor()
    cur.execute(f"""UPDATE makers SET name='{data['name']}', display='{(data['display'])}', instagram='{data['instagram']}' WHERE id={id}""")
    return cur

def toggle_entry(db, data, conf):
    result = False if data['result'] else True
    cur = db.cursor()
    cur.execute(f"UPDATE entries SET result={result} WHERE id = {data['id']} RETURNING id")
    return cur

def get_percents(db, conf):
    cur = db.cursor()
    cur.execute(f"SELECT result, COUNT(result) FROM entries GROUP BY result")
    return cur

def get_percent_by_id(db, id, conf):
    cur = db.cursor()
    cur.execute(f"SELECT m.name, m.display, e.result, COUNT(e.result), m.id FROM entries e LEFT JOIN makers m ON m.id = e.maker_id WHERE e.maker_id = {id} GROUP BY m.name,e.result, m.display, m.id")
    return cur

def del_maker(db, id, conf):
    cur = db.cursor()
    cur.execute(f"DELETE FROM makers WHERE id = {id}")
    print(dir(cur))
    return cur