# Import the dependencies.
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    return (
        f"Thank you for accessing my climate check API!<br/>"
        f"The following API routes are available:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/end"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    #session link from Python to DB
    session = Session(engine)
    #queries
    year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= year).all()
    precip_yr = {date: prcp for date, prcp in precipitation}
    #close Session
    session.close()
    #convert to json
    return jsonify(precip_yr)
 

@app.route("/api/v1.0/stations")
def stations():
    # session link from Python to DB
    session = Session(engine)
    # queries
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    # close session
    session.close()
    # convert to json
    return jsonify(stations=stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # session link from Python to DB
    session = Session(engine)
    # Queries
    # Perform a query to retrieve the data and precipitation scores from most active station
    results = session.query(meas.date,meas.tobs).filter_by(station = "USC00519281").all()
    # create empty list
    active_tobs = []
    # for loop
    for date, tobs in results:
        # create dictionary
        tobs_d = {}
        # fill the dictionary
        tobs_dict[date] = tobs
        active_tobs.append(tobs_d)
    # convert to json
    return jsonify(active_tobs)

@app.route("/api/v1.0/start<start>")
def start(start):
    # session link from Python to DB
    session = Session(engine)
    # Queries
    # Perform a query to retrieve the data and precipitation scores
    results = session.query(func.min(meas.tobs), func.avg(meas.tobs), func.max(meas.tobs)).\filter(meas.date >= start).all()
    # close session
    session.close()
    # create dictionary
    temp_s = {}
    temp_s["Min Temp"] = results[0][0]
    temp_s["Average Temp"] = results[0][1]
    temp_s["Max Temp"] = results[0][2]
    # convert to json
    return jsonify(temp_s)

@app.route("/api/v1.0/start<start>/end<end>")
def end(start,end):
    # session link from Python to DB
    session = Session(engine)
    # Queries
    # Perform a query to retrieve the data and precipitation scores
    results=session.query(func.min(meas.tobs), func.avg(meas.tobs), func.max(meas.tobs)).\filter(meas.date >= start).filter(meas.date <= end).all()
    # close sesion
    session.close()
    # create dictionary
    temps = {}
    temps["Min Temp"] = results[0][0]
    temps["Average Temp"] = results[0][1]
    temps["Max Temp"] = results[0][2]
    #convert to json
    return jsonify(temps)

if __name__ == '__main__':
    app.run(debug=True)
    