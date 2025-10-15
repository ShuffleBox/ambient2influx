import os

from datetime import datetime
import pytz
from influxdb import InfluxDBClient

from app import app
from flask import request

from pprint import pprint

@app.route('/ambient2influx/')
def ambient2influx():
    #convert args to python dictionary
    payload_dict = request.args.to_dict()
    
    #make influxDB client
    influx_client = InfluxDBClient(os.getenv('INFLUX_SERVER'),
                                os.getenv('INFLUX_PORT'),
                                os.getenv('INFLUX_USER'),
                                os.getenv('INFLUX_PASSWORD'),
                                os.getenv('INFLUX_DATABASE'))

    payload = {}
    payload['measurement'] = 'Ambient Weather Station Readings'
    payload['fields'] = payload_dict
    commit = []
    commit.append(payload)
    #influx_client.write_points(commit)
    pprint(commit)
    return "Hello, ambient"


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"