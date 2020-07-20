
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={'check_same_thread': False})


Base = automap_base()

Base.prepare(engine, reflect=True)


Station=Base.classes.station
Measurement=Base.classes.measurement


session = Session(engine)

app = Flask(__name__)


last_twelve_months = '2016-08-23'

@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    maxDate = dt.date(2017, 8 ,23)
    year_ago = maxDate - dt.timedelta(days=365)

    past_temp = (session.query(Measurement.date, Measurement.prcp)
                .filter(Measurement.date <= maxDate)
                .filter(Measurement.date >= year_ago)
                .order_by(Measurement.date).all())
    
    precip = {date: prcp for date, prcp in past_temp}
    
    return jsonify(precip)




@app.route('/api/v1.0/stations')
def stations():

    stations_all = session.query(Station.station).all()

    return jsonify(stations_all)


@app.route('/api/v1.0/tobs') 
def tobs():  
    maxDate = dt.date(2017, 8 ,23)
    year_ago = maxDate - dt.timedelta(days=365)

    lastyear = (session.query(Measurement.tobs)
                .filter(Measurement.station == 'USC00519281')
                .filter(Measurement.date <= maxDate)
                .filter(Measurement.date >= year_ago)
                .order_by(Measurement.tobs).all())
    
    return jsonify(lastyear)

@app.route('/api/v1.0/<start>') 
def start(start=None):

    #start = Measurement.date <= '2010-01-01'
    #end = Measurement.date >= '2017-08-23'

    tobs = (session.query(Measurement.tobs).filter(Measurement.date.between(start, '2017-08-23')).all())
    
    tobs_df = pd.DataFrame(tobs)

    tavg = tobs_df["tobs"].mean()
    tmax = tobs_df["tobs"].max()
    tmin = tobs_df["tobs"].min()
    
    return jsonify(tavg, tmax, tmin)


@app.route('/api/v1.0/<start>/<end>') 
def startend(start=None, end=None):


    tobs = (session.query(Measurement.tobs).filter(Measurement.date.between(start, end)).all())
    
    tobs_df = pd.DataFrame(tobs)

    tavg = tobs_df["tobs"].mean()
    tmax = tobs_df["tobs"].max()
    tmin = tobs_df["tobs"].min()
    
    return jsonify(tavg, tmax, tmin)

if __name__ == "__main__":
    app.run(debug=True)
