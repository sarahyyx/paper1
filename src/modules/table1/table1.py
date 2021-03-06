from logs import logDecorator as lD 
import jsonref, pprint

import matplotlib.pyplot as plt
from tqdm import tqdm
import operator
import csv
import json

from psycopg2.sql import SQL, Identifier, Literal

from lib.databaseIO import pgIO
from modules.table1 import queryDB

config = jsonref.load(open('../config/config.json'))
table1_config = jsonref.load(open('../config/modules/table1.json'))
logBase = config['logging']['logBase'] + '.modules.table1.table1'


@lD.log(logBase + '.genRaceDict')
def genRaceDict(logger, inputCSV):
    '''generates a dictionary with the race str values under each race
    
    This function generates a dict with all the str values under a race from the raceCount CSV
    
    Decorators:
        lD.log
    
    Arguments:
        logger {logging.Logger} -- The logger used for logging error information
        inputCSV {filepath that contains the csv} -- first column "race" contains the race strings, second column "count" contains their counts, and the third column "paper_race" contains the overarching race specified in the paper

    Returns:
        raceDict -- dictionary that contains all the race strings under each specified race in the paper
    '''

    try:
        raceDict = {
                'AA': [],
                'NHPI': [],
                'MR': []
        }

        with open(inputCSV) as f:
            readCSV = csv.reader(f, delimiter=',')
            for row in readCSV:
                for race in table1_config["inputs"]["races"]:
                    if row[2] == race:
                        raceDict[race].append((row[0], row[1]))

    except Exception as e:
        logger.error('genRaceDict failed because of {}'.format(e))

    return raceDict

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
    print('Main function of module table1')
    print('='*30)

    countDict = {
        "AA": [],
        "NHPI":[],
        "MR":[]
    }

    # Run these lines to create sarah.test2 table
    # queryDB.createTest2()

    # Run these lines to create sarah.test3 table
    # queryDB.genAllKeys()
    # queryDB.createTest3()
    # queryDB.popDiagCols()
    # queryDB.delAllFalseTest3()

    queryDB.relabelVar()

    raceCounts = queryDB.countMainRace()
    countDict["AA"].append(raceCounts[0])
    countDict["NHPI"].append(raceCounts[1])
    countDict["MR"].append(raceCounts[2])

    raceAgeCounts = queryDB.countRaceAge()
    countDict["AA"].append(raceAgeCounts[0])
    countDict["NHPI"].append(raceAgeCounts[1])
    countDict["MR"].append(raceAgeCounts[2])

    raceSexCounts = queryDB.countRaceSex()
    countDict["AA"].append(raceSexCounts[0])
    countDict["NHPI"].append(raceSexCounts[1])
    countDict["MR"].append(raceSexCounts[2])

    raceSettingCounts = queryDB.countRaceSetting()
    countDict["AA"].append(raceSettingCounts[0])
    countDict["NHPI"].append(raceSettingCounts[1])
    countDict["MR"].append(raceSettingCounts[2])

    print(countDict)

    obj = json.dumps(countDict)
    f = open("../data/final/sampleCount.json","w+")
    f.write(obj)
    f.close()

    print('Getting out of module table1')
    print('-'*30)

    return

