from flask import Flask, jsonify

import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def home():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end")

@app.route('/api/v1.0/<start>')
def get_t_start(start):
    session = Session(engine)
    
    result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    tobsall = []
    for min,avg,max in result:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Average"] = avg
        tobs_dict["Max"] = max
        tobsall.append(tobs_dict)
        
    session.close()
    return jsonify(tobsall)

@app.route('/api/v1.0/<start>/<stop>')
def get_t_start_stop(start,stop):
    session = Session(engine)
    
    result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= stop).all()

    tobsall = []
    for min,avg,max in result:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Average"] = avg
        tobs_dict["Max"] = max
        tobsall.append(tobs_dict)
        
    session.close()
    return jsonify(tobsall)

@app.route('/api/v1.0/tobs')
def tobs():
    session = Session(engine)
    
    last_str = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    last_date = dt.datetime.strptime(last_str, '%Y-%m-%d')
    query_date = dt.date(last_date.year -1, last_date.month, last_date.day)
    sel = [Measurement.date,Measurement.tobs]
    result = session.query(*sel).filter(Measurement.date >= query_date).all()

    tobsall = []
    for date, tobs in result:
        tobs_dict = {}
        tobs_dict["Date"] = date
        tobs_dict["Tobs"] = tobs
        tobsall.append(tobs_dict)
        
    session.close()
    return jsonify(tobsall)

@app.route('/api/v1.0/stations')
def stations():
    session = Session(engine)
    
    sel = [Station.station,Station.name,Station.latitude,Station.longitude,Station.elevation]
    result = session.query(*sel).all()

    stations = []
    for station,name,lat,lon,el in result:
        station_dict = {}
        station_dict["Station"] = station
        station_dict["Name"] = name
        station_dict["Lat"] = lat
        station_dict["Lon"] = lon
        station_dict["Elevation"] = el
        stations.append(station_dict)
        
    session.close()
    return jsonify(stations)

@app.route('/api/v1.0/precipitation')
def precipitation():
    session = Session(engine)
    
    sel = [Measurement.date,Measurement.prcp]
    result = session.query(*sel).all()

    precipitation = []
    for date, prcp in result:
        prcp_dict = {}
        prcp_dict["Date"] = date
        prcp_dict["Precipitation"] = prcp
        precipitation.append(prcp_dict)
        
    session.close()
    return jsonify(precipitation)

if __name__ == '__main__':
    app.run(debug=True)