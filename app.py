from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import json

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

with open('precip_json.json') as f:
    x = json.load(f)

with open('station_json.json') as f:
    y = json.load(f)

with open('temp_json.json') as f:
    z = json.load(f)
app= Flask(__name__)

@app.route("/")
def home():
    return (
        f"Welcome to the precipitation API</br>"
        f"Routes:</br>"
        f"/api/v1.0/precipitation</br>"
        f"/api/v1.0/stations</br>"
        f"/api/v1.0/tobs</br>"
        f"/api/v1.0/start_date </br>"
        f"/api/v1.0/start_date/end_date</br>"
        f"NB:Write Dates in YYYYMMDD Format</br>"
        f"NB:Both routes that take dates return in minimum tempurature, maximum tempurature, average tempurature format"
    )

@app.route("/api/v1.0/precipitation")
def precip():
    return jsonify(x)
    
@app.route("/api/v1.0/stations")
def station():
    return jsonify(y)

@app.route("/api/v1.0/tobs")
def tempurature():
    return jsonify(z)

@app.route("/api/v1.0/<start>")
def start(start):
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()
    return jsonify(results)
    
@app.route("/api/v1.0/<start>/<end>")
def startend(start, end):
    session = Session(engine)
    interval = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    return jsonify(interval)


if __name__ == "__main__":
    app.run(debug=True)