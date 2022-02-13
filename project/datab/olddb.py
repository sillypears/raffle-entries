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

def get_makers(db, user_id, conf):
    cur = db.cursor()
    cur.execute(f"SELECT id, name, display, instagram FROM makers WHERE user_id = {user_id} ORDER BY name ASC")
    return cur

def get_makers_raffles(db, user_id, conf):
    cur = db.cursor()
    cur.execute(f"SELECT m.id, m.name, m.display, m.instagram, count(e.id) FROM makers m LEFT JOIN entries e ON e.maker_id = m.id WHERE e.user_id = {user_id} GROUP BY m.id HAVING COUNT(e.id) > 0 ORDER BY m.name ASC")
    return cur

def get_maker_by_id(db, id, user_id, conf):
    cur = db.cursor()
    cur.execute(f"SELECT id, name, display, instagram FROM makers WHERE id = {id} AND user_id = {user_id} ")
    return cur

def get_maker_by_name(db, name, user_id, conf):
    cur = db.cursor()
    cur.execute(f"SELECT id, name, display, instagram FROM makers WHERE name = {name} AND user_id = {user_id} ")
    return cur

def get_entries(db, user_id, conf):
    cur = db.cursor()
    cur.execute(f"SELECT * FROM all_entries WHERE user_id = {user_id} ORDER BY epoch DESC, id DESC")
    return cur

def get_entries_by_maker(db, id, user_id, conf):
    cur = db.cursor()
    cur.execute(f"SELECT * FROM all_entries WHERE mid = {id} AND user_id = {user_id} ORDER BY epoch, id ")
    return cur

def get_entry(db, id, user_id, conf):
    cur = db.cursor()
    cur.execute(f"SELECT * FROM all_entries WHERE id = {id} AND user_id = {user_id} ")
    return cur

def add_entry(db, data, user_id, conf):
    cur = db.cursor()
    cur.execute(f"""INSERT INTO entries (maker_id, user_id, epoch, date, raffle_link, notes, result) VALUES ({data['maker_id']}, {user_id}, {data['epoch']}, '{data['date']}', '{data['link'].replace("'","''")}', '{data['notes'].replace("'","''")}', {data['result']}) RETURNING id""")
    return cur

def update_entry(db, id, data, user_id, conf):
    # write something to verify user can update the entry
    try:
        result = True if data['result'] == 'on' else True
    except:
        result = False
    cur = db.cursor()
    cur.execute(f"""UPDATE entries SET maker_id={data['maker']}, epoch={int(datetime.fromisoformat(data['date']).timestamp())}, date='{data['date']}', raffle_link='{data['link'].replace("'","''")}', notes='{data['notes'].replace("'","''")}', result={result} WHERE id={id}""")
    return cur

def add_maker(db, data, user_id, conf):
    cur = db.cursor()
    cur.execute(f"INSERT INTO makers (name, display, instagram, user_id) VALUES ('{data['name']}', '{data['display']}', '{data['instagram']}', {user_id}) RETURNING id")
    return cur

def update_maker(db, id, data, user_id, conf):
    cur = db.cursor()
    cur.execute(f"""UPDATE makers SET name='{data['name']}', display='{(data['display'])}', instagram='{data['instagram']}' WHERE id={id} AND user_id = {user_id}""")
    return cur

def toggle_entry(db, data, user_id, conf):
    result = True if data['result'] == 0 else False
    
    cur = db.cursor()
    # write something to check user_id of entry before toggling or exit
    cur.execute(f"UPDATE entries SET result={result} WHERE id = {data['id']} RETURNING id")
    return cur

def get_percents(db, user_id, conf):
    cur = db.cursor()
    cur.execute(f"SELECT result, COUNT(result) FROM entries WHERE user_id = {user_id} GROUP BY result")
    return cur

def get_percent_by_id(db, id, user_id, conf):
    cur = db.cursor()
    cur.execute(f"SELECT m.name, m.display, e.result, COUNT(e.result), m.id FROM entries e LEFT JOIN makers m ON m.id = e.maker_id WHERE e.maker_id = {id} GROUP BY m.name,e.result, m.display, m.id")
    return cur

def del_maker(db, id, user_id, conf):
    cur = db.cursor()
    cur.execute(f"DELETE FROM makers WHERE id = {id}")
    return cur

def del_entry(db, id, user_id, conf):
    cur = db.cursor()
    # write something to verify user_id matches entry user_id
    cur.execute(f"DELETE FROM entries WHERE id = {id}")
    return cur