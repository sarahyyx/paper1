from logs import logDecorator as lD 
import jsonref, pprint

import matplotlib.pyplot as plt
from tqdm import tqdm
import operator
import csv
import json

from psycopg2.sql import SQL, Identifier, Literal

from lib.databaseIO import pgIO
from modules.table4 import queryDB
from modules.table4 import utils

config = jsonref.load(open('../config/config.json'))
table4_config = jsonref.load(open('../config/modules/table4.json'))
logBase = config['logging']['logBase'] + '.modules.table4.table4'

@lD.log(logBase + '.main')
def main(logger, resultsDict):
    '''main function for module1
    
    This function finishes all the tasks for the
    main function. This is a way in which a 
    particular module is going to be executed. 
    
    Parameters
    ----------
    logger : {logging.Logger}
        The logger used for logging error information
    resultsDict: {dict}
        A dintionary containing information about the 
        command line arguments. These can be used for
        overwriting command line arguments as needed.
    '''

    print('='*30)
    print('Main function of module table4')
    print('='*30)

    resultsDict = {
        "mood": [],
        "anxiety": [],
        "adjustment": [],
        "adhd": [],
        "psyc": [],
        "pers": [],
        "childhood": [],
        "impulse": [],
        "cognitive": [],
        "eating": [],
        "smtf": [],
        "disso": [],
        "sleep": [],
        "fd": []
    }

    for race in table4_config["inputs"]["races"]:
        print(f"I AM IN {race}!")
        race_df = queryDB.createDF_byRace_anySUD(race)
        race_results, columns_dropped = utils.logRegress(race_df)

        for column in columns_dropped:
            resultsDict[column].append([ "-", "-" , "-"])
        for disorder in resultsDict:
            for i, row in race_results.iterrows():
                if disorder == i:
                    disorder_list = []
                    disorder_list.append(round(row['OR'],2))
                    disorder_list.append(round(row['2.5%'],2))
                    disorder_list.append(round(row['97.5%'],2))
                    resultsDict[disorder].append(disorder_list)

    # Remove odds ratios where odds ratio == 0
    for disorder in resultsDict:
        for n, raceList in enumerate(resultsDict[disorder]):
            if raceList[0] == 0.0:
                resultsDict[disorder][n] = ["-", "-", "-"]

    obj = json.dumps(resultsDict)
    f = open("../data/final/table4data.json","w+")
    f.write(obj)
    f.close()

    print('Getting out of module table4')
    print('-'*30)

    return

