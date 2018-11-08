
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, text
import datetime as dt
from flask import Flask, jsonify


#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///./hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB



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
        f"/api/v1.0/startdate<br/>"
        f"/api/v1.0/startdate/enddate"

    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Query for the dates and temperature observations from the last year.
    Convert the query results to a Dictionary using date as the key and tobs as the value.
    Return the JSON representation of your dictionary.   """
    # Query
    session = Session(engine)

    results = session.query(Measurement.prcp, Measurement.date).\
          filter(Measurement.date >='2016-08-23').all()
    all_data = []
    for data in results:
        prcp_dict = {}
        prcp_dict["prcp"] = data.prcp
        prcp_dict["date"] =  data.date
        all_data.append(prcp_dict)



    # Convert list of tuples into normal list
    #all_results = list(np.ravel(results))

    return jsonify(all_data)

@app.route("/api/v1.0/stations")
def stations():
    """/api/v1.0/stations Return a JSON list of stations from the dataset.  """
    session = Session(engine)

    # Query
    results = session.query(Measurement.station).group_by(Measurement.station).all()


    # Convert list of tuples into normal list
    stations = list(np.ravel(results))

    return jsonify(stations)
@app.route("/api/v1.0/tobs")
def tobs():
    """/api/v1.0/stations Return a JSON list of stations from the dataset.  """
    session = Session(engine)

    # Query
    results_temp = session.query(Measurement.tobs).\
                filter(Measurement.date >='2016-08-23').\
              group_by(Measurement.tobs).all()

    # Convert list of tuples into normal list
    tobs = list(np.ravel(results_temp))

    return jsonify(tobs)

@app.route("/api/v1.0/<start>")
def startdate(start):
    query_stdate=dt.datetime.strptime(start,'%Y-%m-%d')
    session = Session(engine)
    results_temp_st=session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
                filter(Measurement.date>=query_stdate).all()



    return jsonify(results_temp_st)


@app.route("/api/v1.0/<start1>/<end1>")
def startenddate(start1,end1):
    query_stdate1=dt.datetime.strptime(start1,'%Y-%m-%d')
    query_enddate=dt.datetime.strptime(end1,'%Y-%m-%d')
    session = Session(engine)
    results_temp_st_end=session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
                filter(Measurement.date>=query_stdate1).\
                filter(Measurement.date<=query_enddate).all()



    return jsonify(results_temp_st_end)


#"""
if __name__ == '__main__':
    app.run(debug=True)
