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
logBase = config['logging']['logBase'] + '.modules.fig1.queryDB'


@lD.log(logBase + '.genDiagCount')
def genDiagCount(logger):
    '''
    This function generates the number of patients with a certain diagnosis
    
    Parameters
    ----------
    logger : {logging.Logger}
        The logger used for logging error information
    '''
    try:
        
        results = {
            "AA": 0,
            "NHPI": 0,
            "MR": 0
        }

        disorder = fig1_config["params"]["mood"]
        race = "MR"

        #get csv containing the unique composite keys for each race
        inputCSV = f"../data/raw_data/{race}_keys.csv"

        with open(inputCSV) as f:
            readCSV = csv.reader(f, delimiter=',')
            
            #for each patient
            for row in tqdm(readCSV): 

                query = SQL('''
                SELECT 
                    dsmno
                FROM
                    raw_data.pdiagnose t1
                WHERE
                    t1.siteid = {} AND t1.backgroundid = {}
                ''').format(
                    Literal(row[0]),
                    Literal(row[1])
                )
                data = pgIO.getAllData(query)
                data = [d[0] for d in data]

                #remove duplicates
                patient_dsmo_list = list(dict.fromkeys(data))

                #compare dsmno of patient and of disorder
                if True in [item in patient_dsmo_list for item in disorder]:
                    results[race] += 1

                
        f.close()
            
        print(results)


    except Exception as e:
        logger.error('Failed to generate count {}'.format(e))

    return 