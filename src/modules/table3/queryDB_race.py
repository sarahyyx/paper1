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

@lD.log(logBase + '.getAgeSUDdata')
def getAgeSUDdata(logger, race):
    '''[summary]
    
    This function gets the odds (the exponential of the logistic regression coefficients) for a df that is passed in

    
    Decorators:
        lD.log
    
    Arguments:
        logger {[type]} -- [description]
        df {[type]} -- [description]
    '''



    try:

        query = SQL('''
        SELECT 
            t1.age,
            t2.sud
        FROM 
            sarah.newtable1data t1
        INNER JOIN 
            sarah.diagnoses t2
        ON 
            t1.siteid = t2.siteid 
        AND 
            t1.backgroundid = t2.backgroundid
        WHERE
            t1.age BETWEEN 12 AND 100
        AND
            t1.race = {}
        ''').format(
            Literal(race)
        )

        data = pgIO.getAllData(query)
        age_data = [d[0] for d in data]
        sud_data = [d[1] for d in data]

        d = {'sud': sud_data, 'age': age_data}
        df = pd.DataFrame(data=d)

        #Dummify the age column, change sud column to binary
        df.replace({False:0, True:1}, inplace=True)
        df.replace(to_replace=list(range(12, 18)), value="12-17", inplace=True)
        df.replace(to_replace=list(range(18, 35)), value="18-34", inplace=True)
        df.replace(to_replace=list(range(35, 50)), value="35-49", inplace=True)
        df.replace(to_replace=list(range(50, 100)), value="50+", inplace=True)

        dummy_ages = pd.get_dummies(df['age'])
        df = df[['sud']].join(dummy_ages)
        df['intercept'] = 1.0

    except Exception as e:
        logger.error('getAgeSUDdata failed because of {}'.format(e))

    return df

@lD.log(logBase + '.getSexSUDdata')
def getSexSUDdata(logger, race):
    '''[summary]
    
    [description]
    
    Decorators:
        lD.log
    
    Arguments:
        logger {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    '''

    try:

        
        query = SQL('''
        SELECT 
            t1.sex,
            t2.sud
        FROM 
            sarah.newtable1data t1
        INNER JOIN 
            sarah.diagnoses t2
        ON 
            t1.siteid = t2.siteid 
        AND 
            t1.backgroundid = t2.backgroundid
        WHERE
            t1.age BETWEEN 12 AND 100
        AND
            t1.race = {}
        ''').format(
            Literal(race)
        )

        data = pgIO.getAllData(query)
        sex_data = [d[0] for d in data]
        sud_data = [d[1] for d in data]

        d = {'sud': sud_data, 'sex': sex_data}
        df = pd.DataFrame(data=d)

        # Dummify the sex column, change sud column to binary
        df.replace({False:0, True:1}, inplace=True)
        dummy_sexes = pd.get_dummies(df['sex'])
        df = df[['sud']].join(dummy_sexes)
        df['intercept'] = 1.0

    except Exception as e:
        logger.error('getSexSUDdata failed because of {}'.format(e))

    return df

@lD.log(logBase + '.getSettingSUDdata')
def getSettingSUDdata(logger, race):
    '''[summary]
    
    [description]
    
    Decorators:
        lD.log
    
    Arguments:
        logger {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    '''

    try:

        query = SQL('''
        SELECT 
            t1.visit_type,
            t2.sud
        FROM 
            sarah.newtable1data t1
        INNER JOIN 
            sarah.diagnoses t2
        ON 
            t1.siteid = t2.siteid 
        AND 
            t1.backgroundid = t2.backgroundid
        WHERE
            t1.age BETWEEN 12 AND 100
        AND
            t1.race = {}
        ''').format(
            Literal(race)
        )
        
        data = pgIO.getAllData(query)
        setting_data = [d[0] for d in data]
        sud_data = [d[1] for d in data]

        d = {'sud': sud_data, 'setting': setting_data}
        df = pd.DataFrame(data=d)

        # Dummify the setting column, change sud column to binary
        df.replace({False:0, True:1}, inplace=True)
        dummy_setting = pd.get_dummies(df['setting'])
        df = df[['sud']].join(dummy_setting)
        df['intercept'] = 1.0

    except Exception as e:
        logger.error('getSettingSUDdata failed because of {}'.format(e))

    return df

@lD.log(logBase + '.getAge2SUDdata')
def getAge2SUDdata(logger, race):
    '''[summary]
    
    This function gets the odds (the exponential of the logistic regression coefficients) for a df that is passed in

    
    Decorators:
        lD.log
    
    Arguments:
        logger {[type]} -- [description]
        df {[type]} -- [description]
    '''

    try:

        query = SQL('''
        SELECT 
            t1.age,
            t2.morethan2sud
        FROM 
            sarah.newtable1data t1
        INNER JOIN 
            sarah.sudcats t2
        ON 
            t1.siteid = t2.siteid 
        AND 
            t1.backgroundid = t2.backgroundid
        WHERE
            t1.age BETWEEN 12 AND 100
        AND
            t1.race = {}
        ''').format(
            Literal(race)
        )

        data = pgIO.getAllData(query)
        age_data = [d[0] for d in data]
        sud_data = [d[1] for d in data]

        d = {'sud': sud_data, 'age': age_data}
        df = pd.DataFrame(data=d)

        #Dummify the age column, change sud column to binary
        df.replace({False:0, True:1}, inplace=True)
        df.replace(to_replace=list(range(12, 18)), value="12-17", inplace=True)
        df.replace(to_replace=list(range(18, 35)), value="18-34", inplace=True)
        df.replace(to_replace=list(range(35, 50)), value="35-49", inplace=True)
        df.replace(to_replace=list(range(50, 100)), value="50+", inplace=True)

        dummy_ages = pd.get_dummies(df['age'])
        df = df[['sud']].join(dummy_ages)
        df['intercept'] = 1.0

    except Exception as e:
        logger.error('getAge2SUDdata failed because of {}'.format(e))

    return df

@lD.log(logBase + '.getSex2SUDdata')
def getSex2SUDdata(logger, race):
    '''[summary]
    
    [description]
    
    Decorators:
        lD.log
    
    Arguments:
        logger {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    '''

    try:

        
        query = SQL('''
        SELECT 
            t1.sex,
            t2.morethan2sud
        FROM 
            sarah.newtable1data t1
        INNER JOIN 
            sarah.sudcats t2
        ON 
            t1.siteid = t2.siteid 
        AND 
            t1.backgroundid = t2.backgroundid
        WHERE
            t1.age BETWEEN 12 AND 100
        AND
            t1.race = {}
        ''').format(
            Literal(race)
        )

        data = pgIO.getAllData(query)
        sex_data = [d[0] for d in data]
        sud_data = [d[1] for d in data]

        d = {'sud': sud_data, 'sex': sex_data}
        df = pd.DataFrame(data=d)

        # Dummify the sex column, change sud column to binary
        df.replace({False:0, True:1}, inplace=True)
        dummy_sexes = pd.get_dummies(df['sex'])
        df = df[['sud']].join(dummy_sexes)
        df['intercept'] = 1.0

    except Exception as e:
        logger.error('getSex2SUDdata failed because of {}'.format(e))

    return df

@lD.log(logBase + '.getSetting2SUDdata')
def getSetting2SUDdata(logger, race):
    '''[summary]
    
    [description]
    
    Decorators:
        lD.log
    
    Arguments:
        logger {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    '''

    try:

        query = SQL('''
        SELECT 
            t1.visit_type,
            t2.morethan2sud
        FROM 
            sarah.newtable1data t1
        INNER JOIN 
            sarah.sudcats t2
        ON 
            t1.siteid = t2.siteid 
        AND 
            t1.backgroundid = t2.backgroundid
        WHERE
            t1.age BETWEEN 12 AND 100
        AND
            t1.race = {}
        ''').format(
            Literal(race)
        )
        
        data = pgIO.getAllData(query)
        setting_data = [d[0] for d in data]
        sud_data = [d[1] for d in data]

        d = {'sud': sud_data, 'setting': setting_data}
        df = pd.DataFrame(data=d)

        # Dummify the setting column, change sud column to binary
        df.replace({False:0, True:1}, inplace=True)
        dummy_setting = pd.get_dummies(df['setting'])
        df = df[['sud']].join(dummy_setting)
        df['intercept'] = 1.0

        print(df.head())

    except Exception as e:
        logger.error('getSetting2SUDdata failed because of {}'.format(e))

    return df