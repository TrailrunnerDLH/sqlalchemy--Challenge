# Import the dependencies.
from flask import Flask, jsonify

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

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
        "/api/v1.0/precipitation/<br/>"
        "/api/v1.0/stations<br/>"
        "/api/v1.0/tobs<br/>"
        "/api/v1.0/&lt;start&gt;<br/>"
        "/api/v1.0/&lt;start&gt;/&lt;end&gt;<br/>"
    )
            

@app.route("/api/v1.0/precipitation/")
def precipitation():
    return "Hello World"

@app.route("/api/v1.0/stations")    
def stations():
    return ""

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
