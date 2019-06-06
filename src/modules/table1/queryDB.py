from logs import logDecorator as lD 
import jsonref, pprint
import numpy as np  
import matplotlib.pyplot as plt

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
    
    This function was used to get the race and count(race) for ALL the races in raw_data.background
    After manucal selection and grouping, the races under each race in the paper (AA, NHPI, MR) were manually entered into the json config file
    Function was delected from the main after use
    
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
                sarah.newtable1data
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
                    sarah.newtable1data
                WHERE 
                    age >= {} AND age <= {} and race = {}
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
                    sarah.newtable1data
                WHERE 
                    sex = {} AND race = {}
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
                    sarah.newtable1data
                WHERE 
                    visit_type = {} AND race = {}
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

@lD.log(logBase + '.pushData')
def pushData(logger, dataTuple):
    '''print a line
    
    This function takes in a tuple containing the data to be inserted
    
    Parameters
    ----------
    logger : {logging.Logger}
        The logger used for logging error information
    '''

    try:
        
        query = SQL('''
        INSERT INTO test (age, visit_type, sex, race, siteid, backgroundid)
        VALUES {};
        ''').format(
            Literal(dataTuple)
        )

        status = pgIO.commitData(query)
        print(status)

    except Exception as e:
        logger.error('pushData failed because of {}'.format(e))

    return

@lD.log(logBase + '.getTable1dataPP')
def getTable1dataPP(logger, data):
    try: 
        data = [d[0] for d in data]
    except Exception as e:
        logger.error(f'{e}')
        return Counter([])


@lD.log(logBase + '.getTable1data')
def getTable1data(logger):
    '''print a line
    
    This function simply prints a single line
    
    Parameters
    ----------
    logger : {logging.Logger}
        The logger used for logging error information
    '''
    p = Pool()

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

        dataIter = pgIO.getDataIterator(query, chunks= 1000)


    except Exception as e:
        logger.error('createTable1data failed because of {}'.format(e))

    return
