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
    raw_dict = request.args.to_dict()
    
    #need to modify the payload to properly type the contents
    payload_dict = {}
    for key, value in raw_dict.items():
        if key == "PASSKEY":
            continue
        elif key == "dateutc":
            try:
                # Parse device-provided time (example: 2025-10-15 17:09:32)
                timestamp = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
                payload_dict[key] = timestamp.isoformat() + 'Z'
            except Exception as e:
                print(f"Could not parse dateutc: {e}")
            continue  # skip adding to fields
        try:
            if '.' in value:
                payload_dict[key] = float(value)
            else:
                payload_dict[key] = int(value)
        except ValueError:
            payload_dict[key] = value
        
            
    #make influxDB client
    influx_client = InfluxDBClient(os.getenv('INFLUX_SERVER'),
                                os.getenv('INFLUX_PORT'),
                                os.getenv('INFLUX_USER'),
                                os.getenv('INFLUX_PASSWORD'),
                                os.getenv('INFLUX_DATABASE'))

    payload = {}
    payload['fields'] = payload_dict
    payload['measurement'] = 'AMBWeather_' + str(payload['fields']['PASSKEY']) 
    commit = []
    commit.append(payload)
    influx_client.write_points(commit)
    pprint(commit)
    return "Hello, ambient"


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"