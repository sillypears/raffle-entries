from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_api import status
import math
from pprint import pprint
from datetime import datetime
import os
import db.db as database
from urllib.parse import urlparse
import json

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


@app.route("/entry/<id>", methods=["GET"])
def get_entry_by_id(id):
    db = database.get_db(conf)
    entry = database.get_entry(db, id, conf).fetchall()[0]
    db.close()
    return render_template("entry.html", percs=get_percs(), entry=entry)


@app.route("/makers", methods=["GET"])
def makers():
    makers = {}
    db = database.get_db(conf)
    ms = database.get_makers_raffles(db, conf).fetchall()
    for maker in ms:
        mpercs = database.get_percent_by_id(db, maker[0], conf).fetchall()
        for perc in mpercs:
            if perc[0] in makers.keys() and len(perc) > 0:
                if perc[2]:
                    makers[perc[0]]['win'] += perc[3]
                    makers[perc[0]]['total'] += perc[3]

                else:
                    makers[perc[0]]['lose'] += perc[3]
                    makers[perc[0]]['total'] += perc[3]

            elif len(perc) > 0:
                if perc[2]:
                    makers[perc[0]] = {}
                    makers[perc[0]]['win'] = perc[3]
                    makers[perc[0]]['lose'] = 0
                    makers[perc[0]]['total'] = perc[3]
                    makers[perc[0]]['display'] = perc[1]
                    makers[perc[0]]['mid'] = perc[4]

                else:
                    makers[perc[0]] = {}
                    makers[perc[0]]['lose'] = perc[3]
                    makers[perc[0]]['win'] = 0
                    makers[perc[0]]['display'] = perc[1]
                    makers[perc[0]]['total'] = perc[3]
                    makers[perc[0]]['mid'] = perc[4]
    db.close()
    return render_template("makers.html", percs=get_percs(), makers=makers, total=len(makers))


@app.route("/maker/<id>", methods=["GET"])
def get_maker_by_id(id):
    db = database.get_db(conf)
    maker = database.get_entries_by_maker(db, id, conf).fetchall()
    db.close()
    return render_template("maker.html", percs=get_percs(), maker=maker)


@app.route("/add/maker", methods=["GET", "POST"])
def add_maker():
    if request.method == 'POST':
        f = request.form
        try:
            name = f['name']
            display = f['display']
            instagram = f['instagram']
        except:
            print('stop failing')
            return redirect("/")
        db = database.get_db(conf)
        entry = database.add_maker(
            db, {'name': name, 'display': display, 'instagram': instagram}, conf)
        db.close()
        return redirect(url_for('index'))
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
        return redirect(url_for('index'))
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
        db = database.get_db(conf)
        update = database.update_entry(db, id, request.form, conf)
        db.close()
        return redirect(url_for('index'))


@app.route("/edit/maker/<id>", methods=["GET", "POST"])
def edit_maker(id):
    if request.method == "GET":
        db = database.get_db(conf)
        maker = database.get_maker(db, id, conf).fetchall()[0]
        db.close()
        return render_template("edit-maker.html", percs=get_percs(), e_id=id, maker=maker)
    elif request.method == "POST":
        db = database.get_db(conf)
        update = database.update_maker(db, id, request.form, conf)
        db.close()
        return redirect(url_for('index'))

@app.route("/delete/entry/<id>", methods=["GET", "POST"])
def del_entry(id):
    if request.method == "GET":
        return render_template("del-entry.html", percs=get_percs(), id=id )
    if request.method == "POST":
        db = database.get_db(conf) 
        del_id = database.del_entry(db, id, conf)
        db.close()
        return redirect(url_for('index'))

@app.route("/del-maker", methods=["GET", "POST"])
def del_makers():
    if request.method == "GET":
        db = database.get_db(conf)
        makers = database.get_makers(db, conf).fetchall()
        db.close()
        return render_template('del-maker.html', percs=get_percs(), makers=makers)
    elif request.method == "POST":
        db = database.get_db(conf)
        for deletee in request.form.getlist('del-maker'):
            print(f"deleting {deletee}")
            deleted = database.del_maker(db, int(deletee), conf)
        db.close()
        return redirect(url_for('index'))

@app.route("/toggle-result", methods=["PUT"])
def toggle_result():
    try:
        id = request.form['id']
        result = int(request.form['result'])
    except:
        return "", status.HTTP_400_BAD_REQUEST
    print(id, result)
    db = database.get_db(conf)
    toggle = database.toggle_entry(db, {'id': id, 'result': result}, conf)
    tggle = toggle.fetchall()[0]
    print(tggle)
    db.close()
    return "", status.HTTP_204_NO_CONTENT


@app.route("/api/getEntriesByMaker", methods=["GET"])
def get_entries_by_maker():
    db = database.get_db(conf)
    e = database.get_entries(db, conf)
    es = e.fetchall()
    entries = {}
    print(e.description)
    for entry in es:
        if entry[-1] in entries.keys():
            entries[entry[-1]].append(entry)
        else:
            entries[entry[-1]] = [entry]
    db.close() 
    return {'status': 'OK', 'data': entries}


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


def get_percs_by_id(id):
    try:
        db = database.get_db(conf)
        p = database.get_percents(db, id, conf)
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
    try:
        db = database.get_db(conf)
        db.close()
    except:
        print("Database connection failed, setting up new DB")
        import db.build_db
        db.build_db.main(conf)
    app.run(threaded=True, debug=conf.DEBUG)
