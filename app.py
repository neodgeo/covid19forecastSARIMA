from flask import Flask, Blueprint
from flask_restplus import Api, Resource, fields
from random import randrange
from updateData import getData
from cleanData import cleanDataToDF
from forecasting import forecastOneToStep
import numpy as np
import pandas as pd
from pylab import *
from pandas import datetime
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error
from numpy.linalg import LinAlgError
from math import sqrt
import statsmodels
import sys
import pmdarima as pm
import itertools
import os
import datetime


app = Flask(__name__)
blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint, doc='/documentation') #,doc=False

app.register_blueprint(blueprint)

app.config['SWAGGER_UI_JSONEDITOR'] = True

a_doc = api.model('forecast',{})

global lastUpdateDate 
lastUpdateDate = ''

def updateDate(date):
    lastUpdateDate = date


@api.route('/forecast')
class Forecast(Resource):
    @api.expect(a_doc)
    def post(self):
        print('inside get', lastUpdateDate)
        dateNow = str(datetime.datetime.now().day) + '/' + str(datetime.datetime.now().month)
        if (lastUpdateDate != dateNow):
            updatedData = getData()
            if updatedData is True:
                updateDate(dateNow)
                # try:
                covid19_france_df = cleanDataToDF()
                cumulated, daily  = forecastOneToStep(covid19_france_df)
                cumulated = cumulated.to_dict(orient='record')
                daily = daily.to_dict(orient='record')
                return {'success' : 'test','data' : {'cumulated':cumulated, 'daily':  daily}}, 200
                # except:
                #     return {'error' : 'could not forecast'}, 401 
        else:
            try:
                covid19_france_df = cleanDataToDF()
                cumulated, daily  = forecastOneToStep(covid19_france_df)
                cumulated = cumulated.to_dict(orient='record')
                daily = daily.to_dict(orient='record')
                return {'success' : 'test','data' : {'cumulated':cumulated, 'daily':  daily}}, 200
            except:
                return {'error' : 'could not forecast'}, 401 



if __name__ == '__main__':
    app.run(debug=True)