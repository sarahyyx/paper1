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

    #Run these two lines to create sarah.sudcats table (only on first run)
    # queryDB.genSUDUserKeys()
    # queryDB.createSUDcatsTable()

    # Run this to generate user counts with any sud and >=2 SUDs, separated by race
    allAgesGeneralSUDCountDict = queryDB.allAgesGeneralSUD()
    obj = json.dumps(allAgesGeneralSUDCountDict)
    f = open("../data/final/allAgesGeneralSUD.json","w+")
    f.write(obj)
    f.close()

    # Run this to generate user counts for each category of sud, separated by race
    allAgesCategorisedCountDict = queryDB.allAgesCategorisedSUD()
    for category in allAgesCategorisedCountDict:
        for n, i in enumerate(allAgesCategorisedCountDict[category]):
            if i == 0.0:
                allAgesCategorisedCountDict[category][n] = "-"
    obj = json.dumps(allAgesCategorisedCountDict)
    f = open("../data/final/allAgesCategorisedSUD.json","w+")
    f.write(obj)
    f.close()

    # Run this to generate user counts with any sud and >=2 suds, separated by age and race bins
    ageBinnedGeneralSUDCountDict = queryDB.ageBinnedGeneralSUD()
    for category in ageBinnedGeneralSUDCountDict:
        for raceList in ageBinnedGeneralSUDCountDict[category]:
            for n, i in enumerate(raceList):
                if i == 0.0:
                    raceList[n] = "-"
    obj = json.dumps(ageBinnedGeneralSUDCountDict)
    f = open("../data/final/ageBinnedGeneralSUD.json","w+")
    f.write(obj)
    f.close()

    # Run this to generate user counts for each category of sud, separated by age and race
    ageBinnedCategorisedSUDCountDict = queryDB.ageBinnedCategorisedSUD()
    for category in ageBinnedCategorisedSUDCountDict:
        for raceList in ageBinnedCategorisedSUDCountDict[category]:
            for n, i in enumerate(raceList):
                if i == 0.0:
                    raceList[n] = "-"
    obj = json.dumps(ageBinnedCategorisedSUDCountDict)
    f = open("../data/final/ageBinnedCategorisedSUD.json","w+")
    f.write(obj)
    f.close()

    print('Getting out of module table2')
    print('-'*30)

    return

