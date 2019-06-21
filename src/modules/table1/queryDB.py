from logs import logDecorator as lD 
import jsonref, pprint
import numpy as np  
import matplotlib.pyplot as plt
import csv

from psycopg2.sql import SQL, Identifier, Literal
from lib.databaseIO import pgIO
from collections import Counter
from textwrap import wrap

from tqdm import tqdm
from multiprocessing import Pool

config = jsonref.load(open('../config/config.json'))
table1_config = jsonref.load(open('../config/modules/table1.json'))
logBase = config['logging']['logBase'] + '.modules.table1.table1'

@lD.log(logBase + '.getRace')
def getRace(logger):
    '''print a line
    
    This function was used to generate the data for the raceCount.csv file, which 
    gets the race and count(race) for ALL the races in raw_data.background.
    After manual selection and grouping, the races under each race in the paper (AA, NHPI, MR) were manually entered into the json config file
    Function was deleted from the main after use
    
    Parameters
    ----------
    logger : {logging.Logger}
        The logger used for logging error information
    '''

    try:
        
        query = '''
        SELECT 
        race,
        COUNT(race)
        FROM raw_data.background
        GROUP BY race
        '''

        data = pgIO.getAllData(query)
        # data = [d[0] for d in data]

    except Exception as e:
        logger.error('getRace failed because of {}'.format(e))

    return data

@lD.log(logBase + '.getTable1data')
def createTable1(logger):
    '''print a line
    
    This function gets the number of unique users using their (siteid,backgroundid) key that fit the sample requirements of the paper
    Variables that are used to filter at this stage are age, visit_type, sex and race. 
    Variable values that are to be included are found in the config file
    
    Parameters
    ----------
    logger : {logging.Logger}
        The logger used for logging error information
    '''

    try:
        query = SQL('''
        SELECT 
            t1.age,
            t1.visit_type, 
            t2.sex,
            t2.race,
            t1.siteid,
            t1.backgroundid
        FROM 
            raw_data.typepatient t1
        INNER JOIN 
            raw_data.background t2
        ON
            t1.backgroundid = t2.id
        AND
            t1.siteid = t2.siteid
        WHERE 
            CAST (t1.age AS INTEGER) < 100
        AND
            t1.visit_type in {}
        AND
            t2.sex in {}
        AND
            t2.race in {}
        ''').format(
            Literal(tuple(table1_config["params"]["setting"]["all"])),
            Literal(tuple(table1_config["params"]["sexes"]["all"])),
            Literal(tuple(table1_config["params"]["races"]["all"]))
            )
    except Exception as e:
        logger.error('Failed to generate table {}'.format(e))
    return

@lD.log(logBase + '.countMainRace')
def countMainRace(logger):
    '''
    This function queries the database and returns the counts of each main race as specified in the paper    
    
    Parameters
    ----------
    logger : {logging.Logger}
        The logger used for logging error information
    '''

    try:
        total = []
        for race in table1_config["inputs"]["races"]:
            query = SQL('''
            SELECT
                COUNT(*)
            FROM 
                sarah.newtable1data t1
            INNER JOIN 
                sarah.diagnoses t2
            ON
                t1.backgroundid = t2.backgroundid
            AND
                t1.siteid = t2.siteid
            WHERE
                race = {}
            ''').format(
                Literal(race)
            )
            data = [d[0] for d in pgIO.getAllData(query)]
            total.append(data[0])

    except Exception as e:
        logger.error('countMainRace failed because of {}'.format(e))

    return total

@lD.log(logBase + '.countRaceAge')
def countRaceAge(logger):
    '''
    
    Parameters
    ----------
    logger : {logging.Logger}
        The logger used for logging error information
    '''

    try:
        total = []
        for race in table1_config["inputs"]["races"]:
            counts = []
            for lower, upper in zip(['1', '12', '18', '35', '50'], ['11', '17', '34', '49', '100']):
                query = SQL('''
                SELECT
                    count(*)
                FROM 
                    sarah.newtable1data t1
                INNER JOIN 
                    sarah.diagnoses t2
                ON
                    t1.backgroundid = t2.backgroundid
                AND
                    t1.siteid = t2.siteid
                WHERE 
                    t1.age >= {} AND t1.age <= {} and t1.race = {}
                ''').format(
                    Literal(lower),
                    Literal(upper),
                    Literal(race)
                )
                data = [d[0] for d in pgIO.getAllData(query)]
                #print("age range: "+str(lower)+"-"+ str(upper)+" count: "+str(data))
                counts.append(data[0])
            total.append(counts)

    except Exception as e:
        logger.error('countRaceAge failed because of {}'.format(e))

    return total

@lD.log(logBase + '.countRaceSex')
def countRaceSex(logger):
    '''
    
    Parameters
    ----------
    logger : {logging.Logger}
        The logger used for logging error information
    '''

    try:
        total = []
        for race in table1_config["inputs"]["races"]:
            counts = []
            for sex in table1_config["inputs"]["sexes"]:
                query = SQL('''
                SELECT
                    count(*)
                FROM 
                    sarah.newtable1data t1
                INNER JOIN 
                    sarah.diagnoses t2
                ON
                    t1.backgroundid = t2.backgroundid
                AND
                    t1.siteid = t2.siteid
                WHERE 
                    t1.sex = {} AND t1.race = {}
                ''').format(
                    Literal(sex),
                    Literal(race)
                )
                data = [d[0] for d in pgIO.getAllData(query)]
                counts.append(data[0])
            total.append(counts)

    except Exception as e:
        logger.error('countRaceSex failed because of {}'.format(e))

    return total

@lD.log(logBase + '.countRaceSetting')
def countRaceSetting(logger):
    '''
    
    Parameters
    ----------
    logger : {logging.Logger}
        The logger used for logging error information
    '''

    try:
        total = []
        for race in table1_config["inputs"]["races"]:
            counts = []
            for setting in table1_config["inputs"]["settings"]:
                query = SQL('''
                SELECT
                    count(*)
                FROM 
                    sarah.newtable1data t1
                INNER JOIN 
                    sarah.diagnoses t2
                ON
                    t1.backgroundid = t2.backgroundid
                AND
                    t1.siteid = t2.siteid
                WHERE 
                    t1.visit_type = {} AND t1.race = {}
                ''').format(
                    Literal(setting),
                    Literal(race)
                )
                data = [d[0] for d in pgIO.getAllData(query)]
                counts.append(data[0])
            total.append(counts)

    except Exception as e:
        logger.error('countRaceSetting failed because of {}'.format(e))

    return total

@lD.log(logBase + '.genAllKeys')
def genAllKeys(logger):
    '''
    This function generates a .csv file for each race's patients' (siteid, backgroundid)
    
    Parameters
    ----------
    logger : {logging.Logger}
        The logger used for logging error information
    '''
    try: 
        query = '''
        SELECT 
            siteid, 
            backgroundid
        FROM
            sarah.test2
        '''

        data = pgIO.getAllData(query)
        data = [(d[0], d[1]) for d in data]

        csvfile = "../data/raw_data/firstfilter_allkeys.csv"

        with open(csvfile,'w+') as output:
            csv_output=csv.writer(output)

            for row in data:
                csv_output.writerow(row)
        output.close()

    except Exception as e:
        logger.error('Failed to generate list of patients because of {}'.format(e))

    return 

@lD.log(logBase + '.addDiagCols')
def addDiagCols(logger):
    '''[summary]
    
    [description]
    
    Decorators:
        lD.log
    
    Arguments:
        logger {[type]} -- [description]
    '''
    try:
        all_userkeys = "../data/raw_data/firstfilter_allkeys.csv"

        with open(all_userkeys) as f:
            readCSV = csv.reader(f, delimiter=",")

            for user in tqdm(readCSV):

                getQuery = SQL('''
                SELECT
                    siteid,
                    backgroundid,
                    array_agg(distinct dsmno) && array[{}] as mood,
                    array_agg(distinct dsmno) && array[{}] as anxiety,
                    array_agg(distinct dsmno) && array[{}] as adjustment,
                    array_agg(distinct dsmno) && array[{}] as adhd,
                    array_agg(distinct dsmno) && array[{}] as sud,
                    array_agg(distinct dsmno) && array[{}] as psyc,
                    array_agg(distinct dsmno) && array[{}] as pers,
                    array_agg(distinct dsmno) && array[{}] as childhood,
                    array_agg(distinct dsmno) && array[{}] as impulse,
                    array_agg(distinct dsmno) && array[{}] as cognitive,
                    array_agg(distinct dsmno) && array[{}] as eating,
                    array_agg(distinct dsmno) && array[{}] as smtf,
                    array_agg(distinct dsmno) && array[{}] as disso,
                    array_agg(distinct dsmno) && array[{}] as sleep,
                    array_agg(distinct dsmno) && array[{}] as fd
                FROM
                    raw_data.pdiagnose
                WHERE
                    siteid = {} and backgroundid = {}
                GROUP BY
                    siteid, backgroundid
                ''').format(
                    Literal(table1_config["params"]["categories"]["mood"]),
                    Literal(table1_config["params"]["categories"]["anxiety"]),
                    Literal(table1_config["params"]["categories"]["adjustment"]),
                    Literal(table1_config["params"]["categories"]["adhd"]),
                    Literal(table1_config["params"]["categories"]["sud"]),
                    Literal(table1_config["params"]["categories"]["psyc"]),
                    Literal(table1_config["params"]["categories"]["pers"]),
                    Literal(table1_config["params"]["categories"]["childhood"]),
                    Literal(table1_config["params"]["categories"]["impulse"]),
                    Literal(table1_config["params"]["categories"]["cognitive"]),
                    Literal(table1_config["params"]["categories"]["eating"]),
                    Literal(table1_config["params"]["categories"]["smtf"]),
                    Literal(table1_config["params"]["categories"]["disso"]),
                    Literal(table1_config["params"]["categories"]["sleep"]),
                    Literal(table1_config["params"]["categories"]["fd"]),
                    Literal(user[0]),
                    Literal(user[1])
                )

                data = pgIO.getAllData(getQuery)

                pushQuery = '''
                INSERT INTO 
                    sarah.test3(siteid, backgroundid, mood, anxiety, adjustment, adhd, sud, psyc, pers, childhood, impulse, cognitive, eating, smtf, disso, sleep, fd)
                VALUES
                    %s
                '''

                print(pgIO.commitDataList(pushQuery, data))
        f.close()


    except Exception as e:
        logger. error('Failed to add columns because of {}'.format(e))
    return
