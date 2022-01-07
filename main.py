from flask import Flask, render_template, request, jsonify, redirect
import math
from pprint import pprint
from datetime import datetime
import os
import db.db as database
from urllib.parse import urlparse

url = urlparse(os.environ.get('DATABASE_URL'))
class Config(object):
    DEBUG = os.environ.get('FLASK_DEBUG')
    DATABASE_HOST = url.hostname
    DATABASE_PORT = url.port
    DATABASE_USER = url.username
    DATABASE_PASS = url.password
    DATABASE_SCHEMA = url.path[1:]

conf = Config

app = Flask(__name__, static_folder='static')

@app.route("/", methods=["GET"])
def index():
    db = database.get_db(conf)
    e = database.get_entries(db, conf)
    entries = e.fetchall()
    db.close()
    return render_template("index.html", percs=get_percs(), entries=entries, headers=e.description, total=len(entries))


@app.route("/add/maker", methods=["GET", "POST"])
def add_maker():
    if request.method == 'POST':
        f = request.form
        try:
            name = f['name']
            display = f['display']
        except:
            print('stop failing')
            return redirect("/")
        db = database.get_db(conf)
        entry = database.add_maker(
            db, {'name': name, 'display': display}, conf)
        db.close()
        return redirect("/")
    else:
        return render_template("add-maker.html", percs=get_percs())


@app.route("/add/entry", methods=["GET", "POST"])
def add_entry():
    if request.method == 'POST':
        f = request.form
        try:
            maker = f['maker']
            link = f['link']
            notes = f['notes']
            y, m, d = f['date'].split("-")
            date = datetime(int(y), int(m), int(d))
            epoch = int(date.timestamp())
        except:
            pass
        try:
            result = True if f['result'] == 'on' else False
        except:
            result = False
        db = database.get_db(conf)
        entry = database.add_entry(db, {'maker_id': maker, 'link': link,
                                        'notes': notes, 'epoch': epoch, 'date': date, 'result': result}, conf)
        db.close()
        return redirect("/")
    else:
        db = database.get_db(conf)
        makers = database.get_makers(db, conf).fetchall()
        db.close()
        return render_template("add-entry.html", percs=get_percs(), todayDate=datetime.now().strftime('%Y-%m-%d'), makers=makers)


@app.route("/edit/entry/<id>", methods=["GET", "POST"])
def edit_entry(id):
    if request.method == "GET":
        db = database.get_db(conf)
        entry = database.get_entry(db, id, conf).fetchall()[0]
        makers = database.get_makers(db, conf).fetchall()
        db.close()
        return render_template("edit-entry.html",  percs=get_percs(),  entry=entry, makers=makers)
    elif request.method == "POST":
        return index()


@app.route("/edit/maker", methods=["GET", "POST"])
def edit_maker():
    db = database.get_db(conf)
    maker = db.get_maker(request.form['id'])
    return render_template("edit-maker.html", percs=get_percs(), maker=maker)

@app.route("/toggle-result", methods=["POST"])
def toggle_result():
    try:
        id = request.form['id']
        result = int(request.form['result'])
    except:
        return {'success': 'FAIL', 'id': -1, 'result': False}
    db = database.get_db(conf)
    toggle = database.toggle_entry(db, {'id': id, 'result': result}, conf)
    toggle = toggle.fetchall()
    print(toggle)
    db.close()
    return {'success': 'OK', 'message': toggle, 'id': id, 'result': result}


def get_percs():
    try:
        db = database.get_db(conf)

        p = database.get_percents(db, conf)
        pes = p.fetchall()
        percs = {'win': 0, 'lose': 0, 'winp': 0, 'losep': 0, 'total': 0}
        for perc in pes:
            if perc[0]: 
                percs['win'] = int(perc[1])
            else:
                percs['lose'] = int(perc[1])

        percs['total'] = percs['win'] + percs['lose']
        percs['winp'] = int(round(percs['win'] / percs['total'] * 100, 0))
        percs['losep'] = int(round(percs['lose'] / percs['total'] * 100, 0))
        db.close()
        return percs
    except:
        return {'win': 0, 'lose': 0, 'winp': 0, 'losep': 0, 'total': 0}
if __name__ == "__main__":
    app.run(threaded=True, debug=conf.DEBUG)
