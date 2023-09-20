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


# This route displays the available API URLs on the landing page. 
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

# Created precipitation route that returns json with the date as the key and the value as the precipitation   
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

# Creates station route that returns jsonified data of all of the station names in the database
@app.route("/api/v1.0/stations")    
def stations():
    station_list = session.query(Station.station).all() 
    station_id = list(np.ravel(station_list))         
    return station_id
  

# creates  return jsonified data for the most active station
@app.route("/api/v1.0/tobs")
def tobs():
    last_result = session.query(Measurement).order_by(Measurement.date.desc()).first()
    last_date = datetime.strptime(last_result.date, "%Y-%m-%d")
    previous_date = last_date - dateutil.relativedelta.relativedelta(months=12)
    station_activity = session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
    most_active_id = station_activity[0][0]
    hist_data = session.query(Measurement.tobs).filter(Measurement.station==most_active_id, Measurement.date >= previous_date).all()
    tobs_list = list(np.ravel(hist_data))

    return tobs_list

@app.route("/api/v1.0/<start>")
def tobs_start(start):
    stats= [
    func.min(Measurement.tobs),   
    func.max(Measurement.tobs),
    func.avg(Measurement.tobs)
    ]
    tobs_stats = session.query(*stats).filter(Measurement.date >= start).all()
    tobs_stats_list = list(np.ravel(tobs_stats))
    return tobs_stats_list 

@app.route("/api/v1.0/<start>/<end>") 
def tobs_start_end(start, end):
    stats= [
    func.min(Measurement.tobs),   
    func.max(Measurement.tobs),
    func.avg(Measurement.tobs)
    ]
    tobs_stats = session.query(*stats).filter(Measurement.date >= start, Measurement.date <= end).all()
    tobs_stats_list = list(np.ravel(tobs_stats))
    return tobs_stats_list  
 


    
    


if __name__ == "__main__":
    app.run(debug=True)
