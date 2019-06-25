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
table4_config = jsonref.load(open('../config/modules/table4.json'))
logBase = config['logging']['logBase'] + '.modules.table4.table4'

@lD.log(logBase + '.logRegress')
def logRegress(logger, df):
    '''Performs logistic regression for any sud
    
    This function returns the logistic regression coefficients for a dataframe that is 
    passed in, and also returns the mental disorders that are dropped due to a small 
    sample. 

    Decorators:
        lD.log
    
    Arguments:
        logger {[type]} -- [description]
        df {dataframe} -- [description]
    '''

    try:

        print("Performing Logistic Regression...")

        # Drop columns who do not meet the minimum percentage of people diagnosed with the disorder
        row_count = df.shape[0]
        columns_to_drop = []
        copy_of_df = df.copy()

        for column, count in copy_of_df.apply(lambda column: (column == 1).sum()).iteritems():
            if count/row_count <= 0.005:
                columns_to_drop.append(column)
        print("These columns are dropped: " + str(columns_to_drop))
        df.drop(columns_to_drop, axis=1, inplace=True)
 
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

    return resultsDF, columns_to_drop
