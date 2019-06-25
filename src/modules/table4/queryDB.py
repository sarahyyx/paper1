from logs import logDecorator as lD 
import jsonref, pprint
import numpy as np  
import pandas as pd
import matplotlib.pyplot as plt
import csv

from psycopg2.sql import SQL, Identifier, Literal
from lib.databaseIO import pgIO
from collections import Counter
from textwrap import wrap

from tqdm import tqdm
from multiprocessing import Pool

config = jsonref.load(open('../config/config.json'))
table4_config = jsonref.load(open('../config/modules/table4.json'))
logBase = config['logging']['logBase'] + '.modules.table4.table4'

@lD.log(logBase + '.createDF_byRace_anySUD')
def createDF_byRace_anySUD(logger, race):
    '''Creates a dataframe with comorbid mental disorder diagnoses with SUD
    
    This function creates a dataframe of users from each race, with the first 
    column being having any sud, the dependent variable, and the rest of the 
    columns being the independent variables of the other mental disorder diagnoses. 
    
    Decorators:
        lD.log
    
    Arguments:
        logger {[type]} -- [description]
        race {str} -- [description]
    
    Returns:
        [type] -- [description]
    '''

    try:

        query = SQL('''
        SELECT 
            t2.sud,
            t2.mood,
            t2.anxiety,
            t2.adjustment,
            t2.adhd,
            t2.psyc,
            t2.pers,
            t2.childhood,
            t2.impulse,
            t2.cognitive,
            t2.eating,
            t2.smtf,
            t2.disso,
            t2.sleep,
            t2.fd
        FROM 
            sarah.test2 t1
        INNER JOIN 
            sarah.test3 t2
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
        sud_data = [d[0] for d in data]
        mood_data = [d[1] for d in data]
        anxiety_data = [d[2] for d in data]
        adjustment_data = [d[3] for d in data]
        adhd_data = [d[4] for d in data]
        psyc_data = [d[5] for d in data]
        pers_data = [d[6] for d in data]
        childhood_data = [d[7] for d in data]
        impulse_data = [d[8] for d in data]
        cognitive_data = [d[9] for d in data]
        eating_data = [d[10] for d in data]
        smtf_data = [d[11] for d in data]
        disso_data = [d[12] for d in data]
        sleep_data = [d[13] for d in data]
        fd_data = [d[14] for d in data]

        d = {'sud': sud_data, 'mood': mood_data, 'anxiety': anxiety_data, 'adjustment': adjustment_data, 'adhd': adhd_data, 'psyc': psyc_data, 'pers': pers_data, 'childhood': childhood_data, 'impulse': impulse_data, 'cognitive': cognitive_data, 'eating': eating_data, 'smtf': smtf_data, 'disso': disso_data, 'sleep': sleep_data, 'fd': fd_data}
        df = pd.DataFrame(data=d)

        # Change all columns to binary
        df.replace({False:0, True:1}, inplace=True)
        
        df['intercept'] = 1.0

    except Exception as e:
        logger.error('createDF_byRace_anySUD failed because of {}'.format(e))

    return df