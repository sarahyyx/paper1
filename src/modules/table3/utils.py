from logs import logDecorator as lD 
import jsonref, pprint
import numpy as np  
import pandas as pd
import matplotlib.pyplot as plt
import csv

from psycopg2.sql import SQL, Identifier, Literal
from lib.databaseIO import pgIO
from collections import Counter

import statsmodels.formula.api as sm

from tqdm import tqdm
from multiprocessing import Pool

config = jsonref.load(open('../config/config.json'))
table3_config = jsonref.load(open('../config/modules/table3.json'))
logBase = config['logging']['logBase'] + '.modules.table3.table3'

@lD.log(logBase + '.logRegress')
def logRegress(logger, df):
    '''Performs logistic regression
    
    This function gets the logistic regression coefficients for a dataframe that is passed in.
    
    Decorators:
        lD.log
    
    Arguments:
        logger {logging.Logger} -- logs error information
        df {dataframe} -- input dataframe where first column is 'sud'
    '''

    try:

        print("Performing Logistic Regression...")

        train_cols = df.columns[1:]
        logit = sm.Logit(df['sud'], df[train_cols])
        result = logit.fit()

        # Get odds, which are assessed by coeff[race/agebin/sex/setting]
        params = result.params
        conf = result.conf_int()
        conf['OR'] = params
        
        conf.columns = ['2.5%', '97.5%', 'OR']
        CI_OR_df = np.exp(conf)
        resultsDF = CI_OR_df[['OR']].join(CI_OR_df.ix[:,:'97.5%'])

    except Exception as e:
        logger.error('logRegress failed because of {}'.format(e))

    return resultsDF
