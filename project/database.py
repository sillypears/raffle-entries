from flask import g
import psycopg2
from datetime import datetime
import re, json

from project import Config

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
    cur.execute(f"SELECT m.id, m.name, m.display, m.instagram, count(e.id) as total FROM makers m LEFT JOIN entries e ON e.maker_id = m.id WHERE m.user_id = {user_id} GROUP BY m.id ORDER BY m.name ASC")
    return cur

def get_maker_by_id(db, id, user_id, conf):
    cur = db.cursor()
    cur.execute(f"SELECT id, name, display, instagram FROM makers WHERE id = {id} AND user_id = {user_id} ")
    return cur

def get_maker_by_name(db, name, user_id, conf):
    cur = db.cursor()
    cur.execute(f"SELECT id, name, display, instagram FROM makers WHERE name = '{name}' AND user_id = {user_id} ")
    return cur

def get_entries(db, user_id, conf):
    cur = db.cursor()
    cur.execute(f"SELECT * FROM all_entries WHERE user_id = {user_id} ORDER BY date DESC, id DESC")
    return cur

def get_entries_by_maker(db, id, user_id, conf):
    cur = db.cursor()
    cur.execute(f"SELECT * FROM all_entries WHERE mid = {id} AND user_id = {user_id} ORDER BY epoch DESC, id DESC ")
    return cur

def get_top_three_makers(db, user_id, conf):
    cur = db.cursor()
    cur.execute(f"SELECT ae.maker,count(ae.mid) FROM all_entries ae WHERE ae.user_id = {user_id} GROUP BY ae.maker ORDER BY count(ae.mid) DESC LIMIT 3")
    return cur

def get_top_three_winning_makers(db, user_id, conf):
    cur = db.cursor()
    cur.execute(f"SELECT ae.maker,count(ae.mid) FROM all_entries ae WHERE ae.user_id = {user_id} AND ae.result = True GROUP BY ae.maker ORDER BY count(ae.mid) DESC LIMIT 3")
    return cur
    
def get_makers_for_export(db, user_id, conf):
    cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(f"SELECT * FROM makers WHERE user_id = {user_id} ORDER BY display ASC, id DESC")
    return cur

def get_entries_for_export(db, user_id, conf):
    cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(f"SELECT * FROM all_entries WHERE user_id = {user_id} ORDER BY epoch DESC, id DESC")
    return cur
    
def get_entry(db, id, user_id, conf):
    # check user_id matches entry
    cur = db.cursor()
    cur.execute(f"SELECT * FROM all_entries WHERE id = {id} AND user_id = {user_id}")
    return cur

def toggle_entry(db, data, user_id, conf):
    # check if user_id matches
    result = True if data['result'] == 0 else False
    cur = db.cursor()
    cur.execute(f"UPDATE entries SET result={result} WHERE id = {data['id']} RETURNING id")
    return cur

def get_percents(db, user_id, conf):
    cur = db.cursor()
    cur.execute(f"SELECT result, COUNT(result) FROM entries WHERE user_id = {user_id} GROUP BY result")
    return cur

def get_percent_by_mid(db, mid, user_id, conf):
    # check userid exists for entry
    cur = db.cursor()
    cur.execute(f"SELECT m.name, m.display, e.result, COUNT(e.result), m.id FROM entries e LEFT JOIN makers m ON m.id = e.maker_id WHERE e.maker_id = {mid} AND e.user_id = {user_id} GROUP BY m.name,e.result, m.display, m.id")
    return cur

def add_entry(db, data, user_id, conf):
    cur = db.cursor()
    cur.execute(f"""INSERT INTO entries (maker_id, epoch, date, raffle_link, notes, result, user_id) VALUES ({data['maker_id']}, {data['epoch']}, '{data['date']}', '{data['link'].replace("'","''")}', '{data['notes'].replace("'","''")}', {data['result']}, {user_id}) RETURNING id""")
    return cur

def update_entry(db, id, data, user_id, conf):
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

def update_maker_by_id(db, id, data, user_id, conf):
    cur = db.cursor()
    cur.execute(f"""UPDATE makers SET name='{data['name']}', display='{(data['display'])}', instagram='{data['instagram']}' WHERE id={id} AND user_id={user_id}""")
    return cur

def del_maker(db, id, user_id, conf):
    cur = db.cursor()
    cur.execute(f"DELETE FROM makers WHERE id = {id}")
    return cur

def del_entry(db, id, user_id, conf):
    cur = db.cursor()
    cur.execute(f"DELETE FROM entries WHERE id = {id}")
    return cur

def add_new_user(db, username, password, conf):
    cur = db.cursor()
    cur.execute(f"INSERT INFO users (name, password) VALUES ({username}, {password}) RETURNING id")
    return cur

def check_user_to_entry(db, id, user_id, conf):
    entry_id = -1
    cur = db.cursor()
    cur.execute(f"SELECT user_id FROM entries WHERE id = {id} AND user_id = {user_id} ")
    try:
        entry_id = int(cur.fetchall()[0][0])
    except:
        pass
    cur.close()
    return True if entry_id == user_id else False

def get_raffles_for_calendar_month(db: psycopg2.connection, date: datetime.date, user_id: int, conf: Config) -> psycopg2.cursor:
    """Get all of the entries for a calendar month

    Args:
        db (psycopg2.connection): db object
        date (datetime.date): date object with the month
        user_id (int): user id to look up entries for
        conf (Config): config object

    Returns:
        psycopg2.cursor: returns all the raffles for the month
    """

    cur = db.cursor()
    cur.execute(f"SELECT e.id, e.date, e.maker, e.mid FROM all_entries e WHERE e.user_id = {user_id} AND EXTRACT(MONTH from e.date) = {date.month} AND EXTRACT(YEAR from e.date) = {date.year} ORDER BY e.id DESC")
    cur.close()
    return cur
    
def get_raffles_for_date(db: psycopg2.connection, date: datetime.date, user_id: int, conf: Config) -> psycopg2.cursor:
    """Get raffles for a specific date

    Args:
        db (psycopg2.connection): The db to generate a cursor
        date (datetime.date): The date to search for
        user_id (int): User id
        conf (Config): Configurations

    Returns:
        psycopg2.cursor: All of the results for the date
    """
    cur = db.cursor()
    cur.execute(f"SELECT e.id, e.date, e.maker, e.mid, e.notes FROM all_entries e WHERE e.user_id = {user_id} AND e.date = {date}")
    cur.close()
    return cur

def get_raffles_for_date_expanded(db: psycopg2.connection, date: datetime.date, user_id: int, conf: Config) -> psycopg2.cursor:
    """Get raffles for a specific date

    Args:
        db (psycopg2.connection): The db to generate a cursor
        date (datetime.date): The date to search for
        user_id (int): User id
        conf (Config): Configurations

    Returns:
        psycopg2.cursor: All of the results for the date
    """
    cur = db.cursor()
    cur.execute(f"SELECT * FROM all_entries e WHERE e.user_id = {user_id} AND e.date = '{date}' ORDER BY e.id DESC")
    cur.close()
    return cur