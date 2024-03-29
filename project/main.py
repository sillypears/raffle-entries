from venv import create
from flask import Blueprint, Flask, render_template, request, jsonify, redirect, url_for
from flask_api import status
from flask_login import login_required, current_user
import math
from pprint import pprint
from datetime import datetime, timedelta
from dateutil import relativedelta
import os
from urllib.parse import urlparse
import json
import calendar
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
    return render_template("index.html", nav="index", percs=get_percs(current_user.id), user=current_user, entries=entries, headers=e.description, total=len(entries))

@main.route("/user", methods=["GET"])
@login_required
def user_data():
    cur = database.get_db(conf)
    e = database.get_entries(cur, current_user.id, conf)
    entries = e.fetchall()
    m = database.get_makers(cur, current_user.id, conf)
    makers = m.fetchall()
    m3 = database.get_top_three_makers(cur, current_user.id, conf)
    top_makers = m3.fetchall()
    e3 = database.get_top_three_winning_makers(cur, current_user.id, conf)
    top_winners = e3.fetchall()
    m1 = database.get_raffle_count_by_month(cur, current_user.id, conf)
    month_raffles = m1.fetchall()
    m2 = database.get_raffle_win_count_by_month(cur, current_user.id, conf)
    month_wins = m2.fetchall()
    month_raf = {}
    for m in month_raffles:
        month_raf[m[0]] = m[1]
    month_perc = {}
    for win in month_wins:
        wins = int(win[1])
        win = win[0]
        if win in month_raf.keys():
            month_perc[win] = {'wins': wins, 'perc': round(wins/int(month_raf[win])* 100)}
    cur.close()
    return render_template("user.html", nav="user", percs=get_percs(current_user.id), user=current_user, entries=entries, makers=makers, top_makers=top_makers, top_winners=top_winners, totals={"entries": len(entries), "makers": len(makers)}, month_raffles=month_raffles, month_wins=month_wins, month_perc=month_perc)


@main.route("/entry/<id>", methods=["GET"])
@login_required
def get_entry_by_id(id):
    cur = database.get_db(conf)
    try:
        entry = database.get_entry(cur, id, current_user.id,conf).fetchall()[0]
    except Exception as e:
        entry = ["Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin",]
    cur.close()
    return render_template("entry.html", nav="entry", percs=get_percs(current_user.id), user=current_user, entry=entry)

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
    return render_template("makers.html", nav="makers", percs=get_percs(current_user.id), user=current_user, makers=makers, total=len(makers))


@main.route("/maker/id/<id>", methods=["GET"])
@login_required
def get_maker_by_id(id):
    cur = database.get_db(conf)
    try:
        maker = database.get_maker_by_id(cur, id, current_user.id, conf).fetchall()[0]
        maker_entries = database.get_entries_by_maker(cur, id, current_user.id, conf).fetchall()
        maker_wins = [win[1] for win in maker_entries if win[1]]
        win_perc = 0 if len(maker_entries) < 1 else len(maker_wins)/len(maker_entries)
    except Exception as e:
        maker = ["Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin"]
        maker_entries = [["Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin"],["Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin"],["Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin"],["Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin"],["Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin"],["Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin"],["Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin"],["Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin"],["Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin"],["Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin"],["Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin"],["Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin"],["Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin"],["Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin"],["Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin","Naughty Gremlin"]]
        maker_wins = 69
        win_perc = 420
    cur.close()
    return render_template("maker.html", nav="maker-id", percs=get_percs(current_user.id), user=current_user, maker=maker, maker_es=maker_entries, maker_wins=len(maker_wins), win_perc=win_perc)

@main.route("/maker/name/<name>", methods=["GET"])
@login_required
def get_maker_by_name(name):
    cur = database.get_db(conf)
    maker = database.get_maker_by_name(cur, name, current_user.id, conf).fetchall()[0]
    maker_entries = database.get_entries_by_maker(cur, maker[0], current_user.id, conf).fetchall()
    cur.close()
    return render_template("maker.html", nav="maker-name", percs=get_percs(current_user.id), user=current_user, maker=maker, maker_es=maker_entries)


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
        return render_template("add-maker.html", nav="maker-add", percs=get_percs(current_user.id), user=current_user)


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
        return render_template("add-entry.html", nav="entry-add", percs=get_percs(current_user.id), user=current_user, todayDate=datetime.now().strftime('%Y-%m-%d'), makers=makers)


@main.route("/edit/entry/<id>", methods=["GET", "POST"])
@login_required
def edit_entry(id):
    if request.method == "GET":
        cur = database.get_db(conf)
        entry = database.get_entry(cur, id, current_user.id, conf).fetchall()[0]
        makers = database.get_makers(cur, current_user.id, conf).fetchall()
        cur.close()
        return render_template("edit-entry.html", nav="entry-edit", percs=get_percs(current_user.id), user=current_user, entry=entry, makers=makers)
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
        return render_template("edit-maker.html", nav="maker-edit", percs=get_percs(current_user.id), user=current_user, id=id, maker=maker)
    elif request.method == "POST":
        db = database.get_db(conf)
        update = database.update_maker_by_id(db, id, request.form, current_user.id, conf)
        db.close()
        return redirect(url_for('main.index'))

@main.route("/delete/entry/<id>", methods=["GET", "POST"])
@login_required
def del_entry(id):
    if request.method == "GET":
        return render_template("del-entry.html", nav="entry-del", percs=get_percs(current_user.id), user=current_user, id=id )
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
        return render_template('del-maker.html', nav="maker-del", percs=get_percs(current_user.id), user=current_user, makers=makers)
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
        return render_template('del-maker.html', nav="secret", percs=get_percs(current_user.id), user=current_user, makers=makers)
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

@main.route('/calendar', methods=["GET"])
def get_calendar():
    try:
        t_delta = timedelta(minutes=int(request.cookies['tz_info'])*-1)
        dutc_now = datetime.utcnow()
        if request.args:
            find_date = datetime(int(request.args['year']), int(request.args['month']), int((dutc_now + t_delta).day))
        else:
            find_date = datetime.utcnow() + timedelta(minutes=int(request.cookies['tz_info'])*-1)
    except:
        find_date = dutc_now + timedelta(minutes=int(request.cookies['tz_info'])*-1)
    db = database.get_db(conf)
    e = database.get_raffles_for_calendar_month(db, find_date, current_user.id, conf).fetchall()
    db.close()
    cal = build_calendar(month=find_date.month, year=find_date.year)
    entries = {}
    for entry in e:
        if entries.get(entry[1].day):
            entries[entry[1].day].append(entry)
        else:
            entries[entry[1].day] = []
            entries[entry[1].day].append(entry)
    return render_template(
        "calendar.html", 
        nav="calendar", 
        percs=get_percs(current_user.id), 
        user=current_user, entries=entries, 
        calendar=cal, 
        header={'year': find_date.year, 'month': find_date.strftime('%B')}, 
        days=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        links={'next': {'year': (find_date + relativedelta.relativedelta(months=1)).year, 'month': (find_date + relativedelta.relativedelta(months=1)).month}, 'prev': {'year': (find_date - relativedelta.relativedelta(months=1)).year, 'month': (find_date - relativedelta.relativedelta(months=1)).month} }
    )

def get_percs(user_id):
    try:
        db = database.get_db(conf)
        p = database.get_percents(db, user_id, conf)
        pes = p.fetchall()
        percs = {'win': 0, 'lose': 0, 'winp': 0, 'losep': 0, 'total': 0}
        for perc in pes:
            if perc[0]:
                percs['win'] = int(perc[1])
            else:
                percs['lose'] = int(perc[1])

        percs['total'] = percs['win'] + percs['lose']
        percs['winp'] = float(round(percs['win'] / percs['total'] * 100, 2))
        percs['losep'] = float(round(percs['lose'] / percs['total'] * 100, 2))
        db.close()
        return percs
    except:
        return {'win': 0, 'lose': 0, 'winp': 0, 'losep': 0, 'total': 0}


def get_percs_by_maker_id(maker_id, user_id):
    try:
        db = database.get_db(conf)
        p = database.get_percents_by_mid(db, maker_id, user_id, conf)
        pes = p.fetchall()
        percs = {'win': 0, 'lose': 0, 'winp': 0, 'losep': 0, 'total': 0}
        for perc in pes:
            if perc[0]:
                percs['win'] = int(perc[1])
            else:
                percs['lose'] = int(perc[1])

        percs['total'] = percs['win'] + percs['lose']
        percs['winp'] = float(round(percs['win'] / percs['total'] * 100, 2))
        percs['losep'] = float(round(percs['lose'] / percs['total'] * 100, 2))
        db.close()
        return percs
    except:
        return {'win': 0, 'lose': 0, 'winp': 0, 'losep': 0, 'total': 0}

def build_calendar(month: int, year: int) -> dict:
    return calendar.Calendar().itermonthdays2(year=year, month=month)


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
