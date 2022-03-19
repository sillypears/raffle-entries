from flask import Blueprint, Flask, render_template, request, jsonify, redirect, url_for, send_file, make_response
from flask_api import status
from flask_login import login_required, current_user
import math
from pprint import pprint
from datetime import datetime
import os
from urllib.parse import urlparse
import json
import csv
from project import create_app
from . import database

utils = Blueprint('utils', __name__)

conf = create_app().config['CONFIG']

@utils.route('/export', methods=["GET"])
@utils.route('/export/<filetype>', methods=["GET"])
@login_required
def export_raffles(filetype='csv'):
    print(filetype)
    if filetype == 'json':
        export_file = None
        export_data = {
            'makers': {},
            'entries': {}
        }
        db = database.get_db(conf)
        maker_data = database.get_makers_for_export(db, current_user.id, conf)
        colnames = [desc[0] for desc in maker_data.description]
        for data in maker_data:
            temp_data = {}
            for col in colnames:
                temp_data[col] = data[col]
            print(temp_data)
            export_data['makers'][data['name']] = temp_data
        db_data = database.get_entries_for_export(db, current_user.id, conf)
        colnames = [desc[0] for desc in db_data.description]
        for data in db_data:
            temp_data = {}
            for col in colnames:
                if col == 'date':
                    temp_data[col] = str(data[col])
                else:
                    temp_data[col] = data[col]
            export_data['entries'][str(data['id'])] = temp_data
        db.close()
        return make_response(export_data, 200)
    elif filetype == 'csv':
        db = database.get_db(conf)

        csv_raw = database.get_entries_for_export(db, current_user.id, conf)
        colnames = [desc[0] for desc in csv_raw.description]
        csv_raw = csv_raw.fetchall()
        csv_data = ""
        csv_data += ",".join(colnames)
        csv_data += "\n"
        print(csv_raw)
        for csv_line in csv_raw:
            print(csv_line)
            csv_data += ",".join(str(val) for val in csv_line)
            csv_data += "\n"
        db.close()
        return create_app().response_class(
            response=csv_data,
            status=200,
            mimetype='text/csv'
            # filename=f"{current_user.id}-{datetime.now().timestamp()}.{filetype}"
        )
    else:
        return redirect(url_for('main.index'))
    