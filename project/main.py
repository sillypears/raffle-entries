from venv import create
from flask import Blueprint, Flask, render_template, request, jsonify, redirect, url_for
from flask_api import status
from flask_login import login_required, current_user
import math
from pprint import pprint
from datetime import datetime
import os
from urllib.parse import urlparse
import json
from project import create_app
from . import db
from . import database
from .models import User, Entry, Maker

main = Blueprint('main', __name__)

conf = create_app().config['CONFIG']

@main.route("/", methods=["GET"])
@login_required
def index():
    cur = database.get_db(conf)
    e = database.get_entries(cur, current_user.id, conf)
    entries = e.fetchall()
    cur.close()
    # test = Entry.query.filter_by(user_id=current_user.id).all()
    return render_template("index.html", nav="index", percs=get_percs(), user=current_user, entries=entries, headers=e.description, total=len(entries))

@main.route("/entry/<id>", methods=["GET"])
@login_required
def get_entry_by_id(id):
    cur = database.get_db(conf)
    try:
        entry = database.get_entry(cur, id, current_user.id,conf).fetchall()[0]
    except Exception as e:
        entry = ["Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin",]
    cur.close()
    return render_template("entry.html", nav="entry", percs=get_percs(), user=current_user, entry=entry)

@main.route("/makers", methods=["GET"])
@login_required
def makers():
    makers = {}
    cur = database.get_db(conf)
    mss = Maker.query.filter_by(user_id=current_user.id).all()
    ms = database.get_makers_raffles(cur, current_user.id, conf).fetchall()
    for maker in ms:
        if maker[4] > 0:
            mpercs = database.get_percent_by_mid(cur, maker[0], current_user.id, conf).fetchall()
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
        else:
            makers[maker[1]] = {}
            makers[maker[1]]['win'] = 0
            makers[maker[1]]['lost'] = 0
            makers[maker[1]]['total'] = 0
            makers[maker[1]]['display'] = maker[2]
            makers[maker[1]]['mid'] = maker[0]
            
    cur.close()
    return render_template("makers.html", nav="makers", percs=get_percs(), user=current_user, makers=makers, total=len(makers))


@main.route("/maker/id/<id>", methods=["GET"])
@login_required
def get_maker_by_id(id):
    cur = database.get_db(conf)
    try:
        maker = database.get_maker_by_id(cur, id, current_user.id, conf).fetchall()[0]
        maker_entries = database.get_entries_by_maker(cur, id, current_user.id, conf).fetchall()
        maker_wins = [win[1] for win in maker_entries if win[1]]
    except Exception as e:
        maker = ["Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin"]
        maker_entries = [["Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin"],["Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin"],["Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin"],["Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin"],["Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin"],["Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin"],["Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin"],["Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin"],["Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin"],["Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin"],["Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin"],["Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin"],["Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin"],["Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin"],["Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin"]]
        maker_wins = 69
    cur.close()
    return render_template("maker.html", nav="maker-id", percs=get_percs(), user=current_user, maker=maker, maker_es=maker_entries, maker_wins=len(maker_wins))

@main.route("/maker/name/<name>", methods=["GET"])
@login_required
def get_maker_by_name(name):
    cur = database.get_db(conf)
    maker = database.get_maker_by_name(cur, name, current_user.id, conf).fetchall()[0]
    maker_entries = database.get_entries_by_maker(cur, maker[0], current_user.id, conf).fetchall()
    cur.close()
    return render_template("maker.html", nav="maker-name", percs=get_percs(), user=current_user, maker=maker, maker_es=maker_entries)


@main.route("/add/maker", methods=["GET", "POST"])
@login_required
def add_maker():
    if request.method == 'POST':
        f = request.form
        try:
            name = f['name']
            display = f['display']
            instagram = f['instagram']
        except:
            print('stop failing')
            return redirect("main.index")
        cur = database.get_db(conf)
        entry = database.add_maker(
            cur, {'name': name, 'display': display, 'instagram': instagram}, current_user.id, conf)
        cur.close()
        return redirect(url_for('main.index'))
    else:
        return render_template("add-maker.html", nav="maker-add", percs=get_percs(), user=current_user)


@main.route("/add/entry", methods=["GET", "POST"])
@login_required
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
        cur = database.get_db(conf)
        entry = database.add_entry(cur, {'maker_id': maker, 'link': link,
                                        'notes': notes, 'epoch': epoch, 'date': date,  'result': result}, current_user.id, conf)
        cur.close()
        return redirect(url_for('main.index'))
    else:
        cur = database.get_db(conf)
        makers = database.get_makers(cur, current_user.id, conf).fetchall()
        cur.close()
        return render_template("add-entry.html", nav="entry-add", percs=get_percs(), user=current_user, todayDate=datetime.now().strftime('%Y-%m-%d'), makers=makers)


@main.route("/edit/entry/<id>", methods=["GET", "POST"])
@login_required
def edit_entry(id):
    if request.method == "GET":
        cur = database.get_db(conf)
        entry = database.get_entry(cur, id, current_user.id, conf).fetchall()[0]
        makers = database.get_makers(cur, current_user.id, conf).fetchall()
        cur.close()
        return render_template("edit-entry.html", nav="entry-edit", percs=get_percs(), user=current_user, entry=entry, makers=makers)
    elif request.method == "POST":
        cur = database.get_db(conf)
        update = database.update_entry(cur, id, request.form, current_user.id, conf)
        cur.close()
        return redirect(url_for('main.index'))


@main.route("/edit/maker/<id>", methods=["GET", "POST"])
@login_required
def edit_maker(id):
    if request.method == "GET":
        db = database.get_db(conf)
        maker = database.get_maker_by_id(db, id, current_user.id, conf).fetchall()[0]
        db.close()
        return render_template("edit-maker.html", nav="maker-edit", percs=get_percs(), user=current_user, id=id, maker=maker)
    elif request.method == "POST":
        db = database.get_db(conf)
        update = database.update_maker_by_id(db, id, request.form, current_user.id, conf)
        db.close()
        return redirect(url_for('main.index'))

@main.route("/delete/entry/<id>", methods=["GET", "POST"])
@login_required
def del_entry(id):
    if request.method == "GET":
        return render_template("del-entry.html", nav="entry-del", percs=get_percs(), user=current_user, id=id )
    if request.method == "POST":
        db = database.get_db(conf) 
        del_id = database.del_entry(db, id, current_user.id, conf)
        db.close()
        return redirect(url_for('main.index'))

@main.route("/delete/maker/<id>", methods=["GET", "POST"])
@login_required
def delete_maker(id):
    if request.method == "GET":
        db = database.get_db(conf)
        makers = database.get_makers(db, current_user.id, conf).fetchall()
        db.close()
        return render_template('del-maker.html', nav="maker-del", percs=get_percs(), user=current_user, makers=makers)
    elif request.method == "POST":
        db = database.get_db(conf)
        for deletee in request.form.getlist('del-maker'):
            print(f"deleting {deletee}")
            deleted = database.del_maker(db, int(deletee), current_user.id, conf)
        db.close()
        return redirect(url_for('main.ndex'))

@main.route("/del-maker-secret-hidden-AJdneandDnsna", methods=["GET", "POST"])
@login_required
def del_makers():
    if request.method == "GET":
        db = database.get_db(conf)
        makers = database.get_makers(db, current_user.id, conf).fetchall()
        db.close()
        return render_template('del-maker.html', nav="secret", percs=get_percs(), user=current_user, makers=makers)
    elif request.method == "POST":
        db = database.get_db(conf)
        for deletee in request.form.getlist('del-maker'):
            print(f"deleting {deletee}")
            deleted = database.del_maker(db, int(deletee), current_user.id, conf)
        db.close()
        return redirect(url_for('main.ndex'))

@main.route("/toggle-result", methods=["PUT"])
@login_required
def toggle_result():
    toggle = None   
    try:
        id = request.form['id']
        result = int(request.form['result'])
    except:
        return "", status.HTTP_400_BAD_REQUEST
    db = database.get_db(conf)
    
    print(id, current_user.id, database.check_user_to_entry(db, id, current_user.id, conf))
    if database.check_user_to_entry(db, id, current_user.id, conf):
        toggle = database.toggle_entry(db, {'id': id, 'result': result}, current_user.id, conf)
    db.close()
    return "", status.HTTP_204_NO_CONTENT


@main.route("/api/getEntriesByMaker", methods=["GET"])
def get_entries_by_maker():
    db = database.get_db(conf)
    e = database.get_entries(db, current_user.id, conf)
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
        p = database.get_percents(db, current_user.id, conf)
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


def get_percs_by_maker_id(maker_id):
    try:
        db = database.get_db(conf)
        p = database.get_percents_by_mid(db, maker_id, current_user.id, conf)
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
        database = database.get_db(conf)
        database.close()
    except:
        print("databasease connection failed, setting up new DB")
        import database.build_db
        database.build_db.main(conf)
    app.run(threaded=True, debug=conf.DEBUG)
else:
    gunicorn_app = create_app()
