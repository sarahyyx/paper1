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
table2_config = jsonref.load(open('../config/modules/table2.json'))
logBase = config['logging']['logBase'] + '.modules.table2.table2'

@lD.log(logBase + '.genSUDUserKeys')
def genSUDUserKeys(logger):
    '''
    This function generates a .csv file for each SUD patients' (siteid, backgroundid)
    
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
            sarah.diagnoses
        WHERE 
            
        '''

        data = pgIO.getAllData(query)
        data = [(d[0], d[1]) for d in data]

        csvfile = "../data/raw_data/All_keys.csv"

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
        all_userkeys = "../data/raw_data/All_keys.csv"

        with open(all_userkeys) as f:
            readCSV = csv.reader(f, delimiter=",")

            for user in tqdm(readCSV):

                getQuery = SQL('''
                SELECT
                    siteid,
                    backgroundid,
                    array_agg(distinct dsmno) && array[{}] as alc,
                    array_agg(distinct dsmno) && array[{}] as cannabis,
                    array_agg(distinct dsmno) && array[{}] as amphe,
                    array_agg(distinct dsmno) && array[{}] as halluc,
                    array_agg(distinct dsmno) && array[{}] as nicotin,
                    array_agg(distinct dsmno) && array[{}] as cocaine,
                    array_agg(distinct dsmno) && array[{}] as opioids,
                    array_agg(distinct dsmno) && array[{}] as sedate,
                    array_agg(distinct dsmno) && array[{}] as others,
                    array_agg(distinct dsmno) && array[{}] as polysub,
                    array_agg(distinct dsmno) && array[{}] as inhalant
                FROM
                    raw_data.pdiagnose
                WHERE
                    siteid = {} and backgroundid = {}
                GROUP BY
                    siteid, backgroundid
                ''').format(
                    Literal(table2_config["params"]["categories"]["mood"]),
                    Literal(table2_config["params"]["categories"]["anxiety"]),
                    Literal(table2_config["params"]["categories"]["adjustment"]),
                    Literal(table2_config["params"]["categories"]["adhd"]),
                    Literal(table2_config["params"]["categories"]["sud"]),
                    Literal(table2_config["params"]["categories"]["psyc"]),
                    Literal(table2_config["params"]["categories"]["pers"]),
                    Literal(table2_config["params"]["categories"]["childhood"]),
                    Literal(table2_config["params"]["categories"]["impulse"]),
                    Literal(table2_config["params"]["categories"]["cognitive"]),
                    Literal(table2_config["params"]["categories"]["eating"]),
                    Literal(table2_config["params"]["categories"]["smtf"]),
                    Literal(table2_config["params"]["categories"]["disso"]),
                    Literal(table2_config["params"]["categories"]["sleep"]),
                    Literal(table2_config["params"]["categories"]["fd"]),
                    Literal(user[0]),
                    Literal(user[1])
                )

                data = pgIO.getAllData(getQuery)

                pushQuery = '''
                INSERT INTO 
                    sarah.diagnoses(siteid, backgroundid, dsmnos, mood, anxiety, adjustment, adhd, sud, psyc, pers, childhood, impulse, cognitive, eating, smtf, disso, sleep, fd)
                VALUES
                    %s
                '''

                print(pgIO.commitDataList(pushQuery, data))


    except Exception as e:
        logger. error('Failed to add columns because of {}'.format(e))
    return

@lD.log(logBase + '.test')
def test(logger):
    print("This is a test")
    return
