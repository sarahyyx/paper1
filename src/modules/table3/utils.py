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
    '''[summary]
    
    This function gets the odds (the exponential of the logistic regression coefficients) for a df that is passed in

    
    Decorators:
        lD.log
    
    Arguments:
        logger {[type]} -- [description]
        df {[type]} -- [description]
    '''

    try:

        print("Performing Logistic Regression...")

        # include condition to check if logRegress can be performed? e.g. sample size too small etc.
        train_cols = df.columns[1:]
        logit = sm.Logit(df['sud'], df[train_cols])
        result = logit.fit()

        # Get odds, which are assessed by coeff[race/agebin/sex/setting]
        coeff = result.params
        odds = round(np.exp(coeff), 3)

    except Exception as e:
        logger.error('logRegress failed because of {}'.format(e))

    return odds
