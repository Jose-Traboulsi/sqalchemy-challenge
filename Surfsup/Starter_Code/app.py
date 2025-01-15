# Import the dependencies.
import warnings
warnings.filterwarnings('ignore')
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
station = Base.classes.station
measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(bind=engine)

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
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date (format: YYYY-MM-DD, e.g., /api/v1.0/2025-01-14)<br/>"
        f"/api/v1.0/start_date/end_date (format: YYYY-MM-DD, e.g., /api/v1.0/2025-01-14/2025-12-31)"
    )

@app.route("/api/v1.0/precipitation")

def prcp_func():
    end_date = dt.date(2017, 8, 23)
    start_date = dt.date(2016, 8, 23)

    results = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= start_date).\
        filter(measurement.date <= end_date).all()
    
    session.close()


    # Create a dictionary with date as the key and prcp as the value
    prcp_dict = {date: prcp for date, prcp in results}

    return jsonify(prcp_dict)


@app.route("/api/v1.0/stations")
def station_func():
    results2 = session.query(station.station).all()
    all_stations = list(np.ravel(results2))

    session.close()

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def active_station():
    start_date = dt.date(2016, 8, 18)
    tobs_data = session.query(measurement.date, measurement.tobs).\
        filter(measurement.station=='USC00519281').\
        filter(measurement.date >= start_date).all()

    session.close()

    active_station = list(np.ravel(tobs_data))
    return jsonify(active_station)


@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")

def date_func(start=None, end=None):
    select=[func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)]
    if not end:
        start = dt.datetime.strptime(start, "%Y-%m-%d")
        results = session.query(*select).\
            filter(measurement.date >= start).all()
            
        session.close()

        date_results=list(np.ravel(results))
        return jsonify(date_results)

    start = dt.datetime.strptime(start, "%Y-%m-%d")
    end = dt.datetime.strptime(end, "%Y-%m-%d")
    results = session.query(*select).\
         filter(measurement.date >= start).\
         filter(measurement.date <= end).all()

    session.close()    

    date_results2=list(np.ravel(results))
    return jsonify(date_results2)

if __name__ == "__main__":
    app.run(debug=True)