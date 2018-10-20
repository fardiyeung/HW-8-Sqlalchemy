import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
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
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
    )


@app.route("/api/v1.0/precipitation")
def date_prcp():
    result_f= session.query(Measurement.date, Measurement.tobs).all()

    date_tobs = []
    for res in result_f:
        date_tobs_dict = {}
        date_tobs_dict["date"] = res[0]
        date_tobs_dict["tobs"] = res[1]
        date_tobs.append(date_tobs_dict)

    return jsonify(date_tobs)



@app.route("/api/v1.0/stations")
def all_stations():
    result= session.query(Station.station).all()

    stations = list(np.ravel(result))
  
    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def all_tobs():
    result = session.query(Measurement.tobs)\
            .filter(Measurement.date >= '2016-08-23')\
            .group_by(Measurement.date)\
            .order_by(Measurement.date.desc()).all()
    tobs = list(np.ravel(result))
    return jsonify(tobs)



@app.route("/api/v1.0/<start>")
def start_date(start):

    start_date = start.replace(" ", "").lower()
    result = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs))\
    .filter(Measurement.date >= start_date)\
    .group_by(Measurement.date).order_by(Measurement.date.desc()).all()

    all_list = []
    all_list = [list(res) for res in result]
        
    
    return jsonify(all_list)

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    start_date = start.replace(" ", "").lower()
    end_date =end.replace(" ", "").lower()
    if start_date == '':
        return jsonify({"error": f"Please provide start date."}), 404

    result = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs))\
    .filter(Measurement.date >= start_date).filter(Measurement.date <= end_date)\
    .group_by(Measurement.date).order_by(Measurement.date.desc()).all()

    all_list = []
    all_list = [list(res) for res in result]
        
    
    return jsonify(all_list)

    





if __name__ == "__main__":
    app.run(debug=True)