# Import the dependencies.
from flask import Flask, jsonify

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from datetime import datetime
import dateutil.relativedelta

import numpy as np


#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

print(Base.classes.keys())
# Save references to each table

Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB

session = Session(engine)
#################################################
# Flask Setup
#################################################

app = Flask (__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def index():
    return (
        "Available Routes<br/>"
        "/api/v1.0/precipitation<br/>"
        "/api/v1.0/stations<br/>"
        "/api/v1.0/tobs<br/>"
        "/api/v1.0/&lt;start&gt;<br/>"
        "/api/v1.0/&lt;start&gt;/&lt;end&gt;<br/>"
    )
            
@app.route("/api/v1.0/precipitation")
def precipitation():
    last_result = session.query(Measurement).order_by(Measurement.date.desc()).first()
    last_date = datetime.strptime(last_result.date, "%Y-%m-%d")
    previous_date = last_date - dateutil.relativedelta.relativedelta(months=12)
    measurements = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= previous_date).all()
    
    measure_dict = {}

    for date, prcp in measurements:
        if type (prcp) == float:
            measure_dict[date]= prcp
    return measure_dict

@app.route("/api/v1.0/stations")    
def stations():
    station_count = session.query(Station.station).all()
    station_list = list(np.ravel(station_count))
    return station_list

@app.route("/api/v1.0/tobs")
def tobs():
    return ""

@app.route("/api/v1.0/<start>")
def start():
    return ""

@app.route("/api/v1.0/<start>/<end>")
def Start_end():
    return ""


    
    


if __name__ == "__main__":
    app.run(debug=True)
