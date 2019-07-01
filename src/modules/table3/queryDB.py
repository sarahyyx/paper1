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
    '''Populates the 'morethan2sud' column in sarah.test4
    
    This function counts the number of 'True' for each mental disorder 
    for each user in sarah.test4. If they have more than 1 'True' value,
    their 'morethan2sud' column will be set to 'True'.
    
    Decorators:
        lD.log
    
    Arguments:
        logger {[type]} -- [description]
    '''
    try:
        query = '''
        SELECT 
            t1.patientid,
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
            sarah.test2 t1
        INNER JOIN 
            sarah.test4 t2
        ON
            t1.patientid = t2.patientid
        '''

        data = pgIO.getAllData(query)

        csvfile = '../data/raw_data/morethan2suduser_keys.csv'

        with open(csvfile, 'w+') as output:
            csv_output = csv.writer(output)

            for row in data:
                if sum(list(row[1:12])) >=2:
                    csv_output.writerow(row)
        output.close()

        with open(csvfile) as f:
            readCSV = csv.reader(f, delimiter=",")

            for user in tqdm(readCSV):
                updateQuery = '''
                UPDATE 
                    sarah.test4
                SET 
                    morethan2sud = True
                WHERE
                   patientid = {}
                '''.format(user[0])
                print(pgIO.commitData(updateQuery))

                # print(type(user[0]))

        #Update column's null values to false
        updateQuery2 = '''
        UPDATE 
            sarah.test4
        SET 
            morethan2sud = False
        WHERE
           morethan2sud is null
        '''
        print(pgIO.commitData(updateQuery2))

        
    except Exception as e:
        logger.error('adding morethan2sud column to the databse failed because of {}'.format(e))

    return 

@lD.log(logBase + '.createDF_allRaces_anySUD')
def createDF_allRaces_anySUD(logger):
    '''Creates dataframe for total sample, dependent variable = any sud
    
    This function creates a dataframe for the total sample, where the 
    dependent variable is any sud and the independent variables are: 
    race, age, sex and setting.
    
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
            t2.sud,
            t1.race,
            t1.age,
            t1.sex,
            t1.visit_type
            
        FROM 
            sarah.test2 t1
        INNER JOIN 
            sarah.test3 t2
        ON
            t1.patientid = t2.patientid
        WHERE
            t1.age BETWEEN 12 AND 100
        '''

        data = pgIO.getAllData(query)
        sud_data = [d[0] for d in data]
        race_data = [d[1] for d in data]
        age_data = [d[2] for d in data]
        sex_data = [d[3] for d in data]
        setting_data = [d[4] for d in data]

        d = {'sud': sud_data, 'race': race_data, 'age': age_data, 'sex': sex_data, 'setting': setting_data}
        main = pd.DataFrame(data=d)
        df = main.copy()

        # Change sud column to binary, dummify the other columns
        df.replace({False:0, True:1}, inplace=True)

        dummy_races = pd.get_dummies(main['race'])
        df = df[['sud']].join(dummy_races.ix[:, 'MR':])

        main.replace(to_replace=list(range(12, 18)), value="12-17", inplace=True)
        main.replace(to_replace=list(range(18, 35)), value="18-34", inplace=True)
        main.replace(to_replace=list(range(35, 50)), value="35-49", inplace=True)
        main.replace(to_replace=list(range(50, 100)), value="50+", inplace=True)
        dummy_ages = pd.get_dummies(main['age'])
        df = df[['sud', 'MR', 'NHPI']].join(dummy_ages.ix[:, :'35-49'])

        dummy_sexes = pd.get_dummies(main['sex'])
        df = df[['sud', 'MR', 'NHPI', '12-17', '18-34', '35-49']].join(dummy_sexes.ix[:, 'M':])

        dummy_setting = pd.get_dummies(main['setting'])
        df = df[['sud', 'MR', 'NHPI', '12-17', '18-34', '35-49', 'M']].join(dummy_setting.ix[:, :'Hospital'])
        
        df['intercept'] = 1.0

    except Exception as e:
        logger.error('createDF_allRaces_anySUD failed because of {}'.format(e))

    return df

@lD.log(logBase + '.createDF_allRaces_morethan2SUD')
def createDF_allRaces_morethan2SUD(logger):
    '''Creates dataframe for total sample, dependent variable = more than 2 sud
    
    This function creates a dataframe for the total sample, where the 
    dependent variable is >=2 sud and the independent variables are: 
    race, age, sex and setting.
    
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
            t2.morethan2sud,
            t1.race,
            t1.age,
            t1.sex,
            t1.visit_type
            
        FROM 
            sarah.test2 t1
        INNER JOIN 
            sarah.test4 t2
        ON
            t1.patientid = t2.patientid
        WHERE
            t1.age BETWEEN 12 AND 100
        '''

        data = pgIO.getAllData(query)
        sud_data = [d[0] for d in data]
        race_data = [d[1] for d in data]
        age_data = [d[2] for d in data]
        sex_data = [d[3] for d in data]
        setting_data = [d[4] for d in data]

        d = {'sud': sud_data, 'race': race_data, 'age': age_data, 'sex': sex_data, 'setting': setting_data}
        main = pd.DataFrame(data=d)
        df = main.copy()

        # Change sud column to binary, dummify the other columns
        df.replace({False:0, True:1}, inplace=True)

        dummy_races = pd.get_dummies(main['race'])
        df = df[['sud']].join(dummy_races.ix[:, 'MR':])

        main.replace(to_replace=list(range(12, 18)), value="12-17", inplace=True)
        main.replace(to_replace=list(range(18, 35)), value="18-34", inplace=True)
        main.replace(to_replace=list(range(35, 50)), value="35-49", inplace=True)
        main.replace(to_replace=list(range(50, 100)), value="50+", inplace=True)
        dummy_ages = pd.get_dummies(main['age'])
        df = df[['sud', 'MR', 'NHPI']].join(dummy_ages.ix[:, :'35-49'])

        dummy_sexes = pd.get_dummies(main['sex'])
        df = df[['sud', 'MR', 'NHPI', '12-17', '18-34', '35-49']].join(dummy_sexes.ix[:, 'M':])

        dummy_setting = pd.get_dummies(main['setting'])
        df = df[['sud', 'MR', 'NHPI', '12-17', '18-34', '35-49', 'M']].join(dummy_setting.ix[:, :'Hospital'])
        
        df['intercept'] = 1.0

    except Exception as e:
        logger.error('createDF_allRaces_morethan2SUD failed because of {}'.format(e))

    return df

@lD.log(logBase + '.createDF_byRace_anySUD')
def createDF_byRace_anySUD(logger, race):
    '''Creates dataframe for a sample from a specified race, 
    dependent variable = any sud
    
    This function creates a dataframe for a sample from a specified race, 
    where the  dependent variable is any sud and the independent variables 
    are: age, sex and setting.
    
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
            t1.age,
            t1.sex,
            t1.visit_type
            
        FROM 
            sarah.test2 t1
        INNER JOIN 
            sarah.test3 t2
        ON
            t1.patientid = t2.patientid
        WHERE
            t1.age BETWEEN 12 AND 100
        AND 
            t1.race = {}
        ''').format(
            Literal(race)
        )

        data = pgIO.getAllData(query)
        sud_data = [d[0] for d in data]
        age_data = [d[1] for d in data]
        sex_data = [d[2] for d in data]
        setting_data = [d[3] for d in data]

        d = {'sud': sud_data, 'age': age_data, 'sex': sex_data, 'setting': setting_data}
        main = pd.DataFrame(data=d)
        df = main.copy()

        # Change sud column to binary, dummify the other columns
        df.replace({False:0, True:1}, inplace=True)

        main.replace(to_replace=list(range(12, 18)), value="12-17", inplace=True)
        main.replace(to_replace=list(range(18, 35)), value="18-34", inplace=True)
        main.replace(to_replace=list(range(35, 50)), value="35-49", inplace=True)
        main.replace(to_replace=list(range(50, 100)), value="50+", inplace=True)
        dummy_ages = pd.get_dummies(main['age'])
        df = df[['sud']].join(dummy_ages.ix[:, :'35-49'])

        dummy_sexes = pd.get_dummies(main['sex'])
        df = df[['sud', '12-17', '18-34', '35-49']].join(dummy_sexes.ix[:, 'M':])

        dummy_setting = pd.get_dummies(main['setting'])
        df = df[['sud', '12-17', '18-34', '35-49', 'M']].join(dummy_setting.ix[:, :'Hospital'])
        
        df['intercept'] = 1.0

    except Exception as e:
        logger.error('createDF_byRace_anySUD failed because of {}'.format(e))

    return df

@lD.log(logBase + '.createDF_byRace_morethan2SUD')
def createDF_byRace_morethan2SUD(logger, race):
    '''Creates dataframe for a sample from a specified race, 
    dependent variable = more than 2 sud
    
    This function creates a dataframe for a sample from a specified race, 
    where the  dependent variable is >=2 sud and the independent variables 
    are: age, sex and setting.
    
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
            t2.morethan2sud,
            t1.age,
            t1.sex,
            t1.visit_type
            
        FROM 
            sarah.test2 t1
        INNER JOIN 
            sarah.test4 t2
        ON
            t1.patientid = t2.patientid
        WHERE
            t1.age BETWEEN 12 AND 100
        AND 
            t1.race = {}
        ''').format(
            Literal(race)
        )

        data = pgIO.getAllData(query)
        sud_data = [d[0] for d in data]
        age_data = [d[1] for d in data]
        sex_data = [d[2] for d in data]
        setting_data = [d[3] for d in data]

        d = {'sud': sud_data, 'age': age_data, 'sex': sex_data, 'setting': setting_data}
        main = pd.DataFrame(data=d)
        df = main.copy()

        # Change sud column to binary, dummify the other columns
        df.replace({False:0, True:1}, inplace=True)

        main.replace(to_replace=list(range(12, 18)), value="12-17", inplace=True)
        main.replace(to_replace=list(range(18, 35)), value="18-34", inplace=True)
        main.replace(to_replace=list(range(35, 50)), value="35-49", inplace=True)
        main.replace(to_replace=list(range(50, 100)), value="50+", inplace=True)
        dummy_ages = pd.get_dummies(main['age'])
        df = df[['sud']].join(dummy_ages.ix[:, :'35-49'])

        dummy_sexes = pd.get_dummies(main['sex'])
        df = df[['sud', '12-17', '18-34', '35-49']].join(dummy_sexes.ix[:, 'M':])

        dummy_setting = pd.get_dummies(main['setting'])
        df = df[['sud', '12-17', '18-34', '35-49', 'M']].join(dummy_setting.ix[:, :'Hospital'])
        
        df['intercept'] = 1.0

    except Exception as e:
        logger.error('createDF_byRace_morethan2SUD failed because of {}'.format(e))

    return df