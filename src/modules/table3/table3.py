from logs import logDecorator as lD 
import jsonref, pprint

import matplotlib.pyplot as plt
from tqdm import tqdm
import operator
import csv
import json

from psycopg2.sql import SQL, Identifier, Literal

from lib.databaseIO import pgIO
from modules.table3 import queryDB
from modules.table3 import utils

config = jsonref.load(open('../config/config.json'))
table3_config = jsonref.load(open('../config/modules/table3.json'))
logBase = config['logging']['logBase'] + '.modules.table3.table3'

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
    print('Main function of module table3')
    print('='*30)

    ## Run this line to create the column "morethan2sud"
    # queryDB.addmorethan2sudcolumn()

    # First value of each list is for anysud, second value is for morethan2sud
    allRaces_ResultsDict = {
        "NHPI":[],
        "MR":[],
        "12-17":[],
        "18-34":[],
        "35-49":[],
        "M":[],
        "Hospital":[]
    }

    anysud_df = queryDB.createDF_allRaces_anySUD()
    anysud_results = utils.logRegress(anysud_df)

    morethan2sud_df = queryDB.createDF_allRaces_morethan2SUD()
    morethan2sud_results = utils.logRegress(morethan2sud_df)

    for x in allRaces_ResultsDict:

        x_anysud_list = []
        for i in anysud_results.loc[x]:
            x_anysud_list.append(round(i,2))
        allRaces_ResultsDict[x].append(x_anysud_list)

        x_morethan2sud_list = []
        for i in morethan2sud_results.loc[x]:
            x_morethan2sud_list.append(round(i,2))
        allRaces_ResultsDict[x].append(x_morethan2sud_list)

    # print(allRaces_ResultsDict)
    obj = json.dumps(allRaces_ResultsDict)
    f = open("../data/final/oddsratios_allRaces.json","w+")
    f.write(obj)
    f.close()

    anysud_races_ResultsDict = {
        "12-17":[],
        "18-34":[],
        "35-49":[],
        "M":[],
        "Hospital":[]
    }

    for race in table3_config["inputs"]["races"]:
        print(f"I AM IN RACE {race}")

        race_anysud_df = queryDB.createDF_byRace_anySUD(race)
        race_anysud_results = utils.logRegress(race_anysud_df)

        for x in anysud_races_ResultsDict:
            
            x_anysud_list = []
            for i in race_anysud_results.loc[x]:
                x_anysud_list.append(round(i,2))
            anysud_races_ResultsDict[x].append(x_anysud_list)

    # print(anysud_races_ResultsDict)
    obj = json.dumps(anysud_races_ResultsDict)
    f = open("../data/final/oddsratios_anysud_byRace.json","w+")
    f.write(obj)
    f.close()

    morethan2sud_races_ResultsDict = {
        "12-17":[],
        "18-34":[],
        "35-49":[],
        "M":[],
        "Hospital":[]
    }

    for race in table3_config["inputs"]["races"]:
        print(f"I AM IN RACE {race}")

        race_morethan2sud_df = queryDB.createDF_byRace_morethan2SUD(race)
        race_morethan2sud_results = utils.logRegress(race_morethan2sud_df)

        for x in morethan2sud_races_ResultsDict:

            x_morethan2sud_list = []
            for i in race_morethan2sud_results.loc[x]:
                x_morethan2sud_list.append(round(i,2))
            morethan2sud_races_ResultsDict[x].append(x_morethan2sud_list)

    # print(morethan2sud_races_ResultsDict)
    obj = json.dumps(morethan2sud_races_ResultsDict)
    f = open("../data/final/oddsratios_morethan2sud_byRace.json","w+")
    f.write(obj)
    f.close()

    print('Getting out of module table3')
    print('-'*30)

    return

