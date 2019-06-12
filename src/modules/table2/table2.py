from logs import logDecorator as lD 
import jsonref, pprint

import matplotlib.pyplot as plt
from tqdm import tqdm
import operator
import csv
import json

from psycopg2.sql import SQL, Identifier, Literal

from lib.databaseIO import pgIO
from modules.table2 import queryDB

config = jsonref.load(open('../config/config.json'))
table2_config = jsonref.load(open('../config/modules/table2.json'))
logBase = config['logging']['logBase'] + '.modules.table2.table2'

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
    print('Main function of module table2')
    print('='*30)

    # #Run these two lines to create sarah.sudcats table
    # genSUDUserKeys()
    # createSUDcatsTable()

    # # Run this to get .csv files of sud users separated by race
    # queryDB.genSUDRaceKeys()

    # # Run this to generate counts of users with any sud and >=2 SUDs, separated by race
    # allAgesGeneralSUDCountDict = queryDB.allAgesGeneralSUD()
    # obj = json.dumps(allAgesGeneralSUDCountDict)
    # f = open("../data/final/allAgesGeneralSUD.json","w+")
    # f.write(obj)
    # f.close()

    # # Run this to generate counts of users for each category of sud, separated by race
    # allAgesCategorisedCountDict = queryDB.allAgesCategorisedSUD()
    # obj = json.dumps(allAgesCategorisedCountDict)
    # f = open("../data/final/allAgesCategorisedSUD.json","w+")
    # f.write(obj)
    # f.close()

    print('Getting out of module table2')
    print('-'*30)

    return

