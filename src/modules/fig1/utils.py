from logs import logDecorator as lD 
import jsonref, pprint

from psycopg2.sql import SQL, Identifier, Literal
from lib.databaseIO import pgIO
from collections import Counter
from textwrap import wrap
import csv

from tqdm import tqdm
from multiprocessing import Pool

config = jsonref.load(open('../config/config.json'))
fig1_config = jsonref.load(open('../config/modules/fig1.json'))
logBase = config['logging']['logBase'] + '.modules.fig1.utils'

@lD.log(logBase + '.genStr')
def genStr(logger, dir):
    '''print a line
    
    This function simply prints a single line
    
    Parameters
    ----------
    logger : {logging.Logger}
        The logger used for logging error information
    dir : 
        The file directory you want to obtain your concencated string from
    '''
    try: 
        
        dsmnoList = []
        dsmnoStr = ""

        f = open(dir, "r")

        for line in tqdm(f):
            number = line.rstrip()
            dsmnoList.append(number)

        dsmnoList = list(dict.fromkeys(dsmnoList))
        print(dsmnoList)

        for number in dsmnoList:
            dsmnoStr = dsmnoStr + "\"" + number + "\"" + ","
        print(dsmnoStr)

        f.close()
    except Exception as e:
        logger.error('Failed to generate str of dsmno because of {}'.format(e))

    return 

@lD.log(logBase + '.genPatients')
def genPatients(logger):
    '''
    This function generates a .csv file for each race's patients' (siteid, backgroundid)
    
    Parameters
    ----------
    logger : {logging.Logger}
        The logger used for logging error information
    '''
    try: 
        for race in utils_config["inputs"]["races"]: 
            query = SQL('''
            SELECT 
                siteid, 
                backgroundid
            FROM
                sarah.newtable1data t1
            WHERE
                race = {}
            ''').format(
                Literal(race)
            )

            data = pgIO.getAllData(query)
            data = [(d[0], d[1]) for d in data]

            csvfile = f"../data/raw_data/{race}_keys.csv"

            with open(csvfile,'w+') as output:
                csv_output=csv.writer(output)

                for row in data:
                    csv_output.writerow(row)
            output.close()

    except Exception as e:
        logger.error('Failed to generate list of patients because of {}'.format(e))

    return 