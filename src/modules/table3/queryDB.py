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
table3_config = jsonref.load(open('../config/modules/table3.json'))
logBase = config['logging']['logBase'] + '.modules.table3.table3'

@lD.log(logBase + '.addmorethan2sudcolumn')
def addmorethan2sudcolumn(logger):
    try:
        query = '''
        SELECT 
            t1.siteid,
            t1.backgroundid,
            t2.alc,
            t2.cannabis,
            t2.amphe,
            t2.halluc,
            t2.nicotin,
            t2.cocaine,
            t2.opioids,
            t2.sedate,
            t2.others,
            t2.polysub,
            t2.inhalant
        FROM
            sarah.newtable1data t1
        INNER JOIN 
            sarah.sudcats t2
        ON
            t1.siteid = t2.siteid 
        AND
            t1.backgroundid = t2.backgroundid
        '''

        data = pgIO.getAllData(query)

        csvfile = '../data/raw_data/morethan2suduser_keys.csv'

        with open(csvfile, 'w+') as output:
            csv_output = csv.writer(output)

            for tuple in data:
                if sum(list(tuple[2:13])) >=2:
                    csv_output.writerow(tuple[0:2])
        output.close()

        with open(csvfile) as f:
            readCSV = csv.reader(f, delimiter=",")

            for user in tqdm(readCSV):
                updateQuery = '''
                UPDATE 
                    sarah.sudcats
                SET 
                    morethan2sud = True
                WHERE
                   siteid = %s AND backgroundid = %s
                '''
                print(pgIO.commitData(updateQuery, user))

        #Run this query in Postgres to update column's null values to false
        # updateQuery = '''
        # UPDATE 
        #     sarah.sudcats
        # SET 
        #     morethan2sud = False
        # WHERE
        #    morethan2sud is null
        # '''

        
    except Exception as e:
        logger.error('adding morethan2sud column to the databse failed because of {}'.format(e))

    return 

@lD.log(logBase + '.getRaceSUDdata')
def getRaceSUDdata(logger):
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

        query = '''
        SELECT 
            t1.race,
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
        '''

        data = pgIO.getAllData(query)
        race_data = [d[0] for d in data]
        sud_data = [d[1] for d in data]

        d = {'sud': sud_data, 'race': race_data}
        df = pd.DataFrame(data=d)

        # Dummify the race column, change sud column to binary
        df.replace({False:0, True:1}, inplace=True)
        dummy_races = pd.get_dummies(df['race'])
        df = df[['sud']].join(dummy_races)
        df['intercept'] = 1.0

    except Exception as e:
        logger.error('getRaceSUDdata failed because of {}'.format(e))

    return df

@lD.log(logBase + '.getAgeSUDdata')
def getAgeSUDdata(logger):
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

        query = '''
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
        '''

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
        logger.error('getRaceAgedata failed because of {}'.format(e))

    return df

@lD.log(logBase + '.getSexSUDdata')
def getSexSUDdata(logger):
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

        query = '''
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
        '''

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
def getSettingSUDdata(logger):
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

        query = '''
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
        '''

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

@lD.log(logBase + '.getRace2SUDdata')
def getRace2SUDdata(logger):
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

        query = '''
        SELECT 
            t1.race,
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
        '''

        data = pgIO.getAllData(query)
        race_data = [d[0] for d in data]
        sud_data = [d[1] for d in data]

        d = {'sud': sud_data, 'race': race_data}
        df = pd.DataFrame(data=d)

        # Dummify the race column, change sud column to binary
        df.replace({False:0, True:1}, inplace=True)
        dummy_races = pd.get_dummies(df['race'])
        df = df[['sud']].join(dummy_races)
        df['intercept'] = 1.0

    except Exception as e:
        logger.error('getRace2SUDdata failed because of {}'.format(e))

    return df

@lD.log(logBase + '.getAge2SUDdata')
def getAge2SUDdata(logger):
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

        query = '''
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
        '''

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
def getSex2SUDdata(logger):
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

        query = '''
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
        '''

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
def getSetting2SUDdata(logger):
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

        query = '''
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
        '''

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
        logger.error('getSetting2SUDdata failed because of {}'.format(e))

    return df