# Import the dependencies.
from flask import Flask, jsonify
import datetime as dt
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

# Save references to each table
measurement_table = Base.classes.measurement
station_table = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

#Setting up the Flask App as var name
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

# Set most recent data point in the database. 
last_date = dt.datetime(2017, 8, 23)
# Calculate the date one year from the last date in data set.
start_date = last_date - dt.timedelta(days=366)

#Homepage Set up with available routes
@app.route("/")
def homepage():
    return (
        f"Welcome to the Climate API!<br/>"
        f"Available Routes:<br/>"
        f"12 months of data of precipitation observed: /api/v1.0/precipitation<br/>"
        f"List of Stations observed: /api/v1.0/stations<br/>"
        f"12 months of data of temperature observed: /api/v1.0/tobs<br/>"
        f"Minimum, MAximum and average temperatures observed within a date range (being start and end the range of dates of your search): /api/v1.0/<start> and /api/v1.0/<start>/<end>"
    )

#Setting up page 12 months of data of precipitation observed:  
@app.route("/api/v1.0/precipitation")
def precipitation():

    # Perform a query to retrieve the data and precipitation scores
    scores = session.query(measurement_table.date, measurement_table.prcp).filter(measurement_table.date >= start_date).filter(measurement_table.date <= last_date).order_by(measurement_table.date).all()

    # Save the query results as a dictionary.
    scores_dict = {}
    for date, prcp in scores:
        scores_dict[date] = prcp

    # convert Dcitionary into a JSON file
    json_scores = jsonify(scores_dict)

    return (json_scores)

#Setting up page List of Stations observed:  
@app.route("/api/v1.0/stations")
def stations():
    #query stations
    stations = session.query(station_table.station).all()

    #Add the query results to a list
    station_list = [stat[0] for stat in stations]
    
    #Json from list of stations
    station_json = jsonify(station_list)

    return (station_json)

#Setting up page 12 months of data of temperature observed on the most frequent station:  
@app.route("/api/v1.0/tobs")
def temperature():
    #Identifying the most frequent station:
    station_feq = session.query(measurement_table.station, func.count(measurement_table.station)).group_by(measurement_table.station).order_by(func.count(measurement_table.station).desc()).all()
    act_station = station_feq[0][0]

    # Perform a query to retrieve the data and precipitation scores
    tobs_query = session.query(measurement_table.date, measurement_table.tobs).filter(measurement_table.date >= start_date).filter(measurement_table.date <= last_date).filter(measurement_table.station == act_station).order_by(measurement_table.date).all()

    #Add the query results to a list
    tobs_list = [f"{date} - {tobs}" for date, tobs in tobs_query]

    # convert list into a JSON file
    json_scores = jsonify(tobs_list)

    return (json_scores)

#Setting up page Minimum, MAximum and average temperatures observed within a date range - Start only:  
@app.route("/api/v1.0/<start>")
def tempdatastart(start):

    # Perform a query to retrieve the data and precipitation scores
    min_tobs = session.query(func.min(measurement_table.tobs)).filter(measurement_table.date >= start).first()
    max_tobs = session.query(func.max(measurement_table.tobs)).filter(measurement_table.date >= start).first()
    avg_tobs = session.query(func.avg(measurement_table.tobs)).filter(measurement_table.date >= start).first()

    #Add the query results to a list
    tobs_list = [min_tobs[0], max_tobs[0], avg_tobs[0]]

    # convert list into a JSON file
    json_tobs = jsonify(tobs_list)

    return (json_tobs)

#Setting up page Minimum, MAximum and average temperatures observed within a date range - Start + End dates provided:  
@app.route("/api/v1.0/<start>/<end>")
def tempdatarange(start, end):

    # Perform a query to retrieve the data and precipitation scores
    min_tobs = session.query(func.min(measurement_table.tobs)).filter(measurement_table.date >= start).filter(measurement_table.date <= end).first()
    max_tobs = session.query(func.max(measurement_table.tobs)).filter(measurement_table.date >= start).filter(measurement_table.date <= end).first()
    avg_tobs = session.query(func.avg(measurement_table.tobs)).filter(measurement_table.date >= start).filter(measurement_table.date <= end).first()

    #Add the query results to a list
    tobs_list = [min_tobs[0], max_tobs[0], avg_tobs[0]]

    # convert list into a JSON file
    json_tobs = jsonify(tobs_list)
    
    return (json_tobs)

#Assign var name to main for running at startup of main module
if __name__ == "__main__":
    app.run(debug=True)
