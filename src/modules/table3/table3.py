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
from modules.table3 import queryDB_race

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

    # First value of each list is for any_sud, second value is for more_than2_sud
    allResultsDict = {
        "races":{
            "AA":[],
            "NHPI":[],
            "MR":[]
        },
        "ageBins":{
            "12-17":[],
            "18-34":[],
            "35-49":[],
            "50+":[]
        },
        "sexes":{
            "M":[],
            "F":[]
        },
        "settings":{
            "Hospital":[],
            "Mental Health Center":[]
        }
    }

    # race_anySUD_df = queryDB.getRaceSUDdata()
    # results = utils.logRegress(race_anySUD_df)
    # for race in allResultsDict["races"]:
    #     allResultsDict["races"][race].append(results[race])

    # agebins_anySUD_df = queryDB.getAgeSUDdata()
    # results = utils.logRegress(agebins_anySUD_df)
    # for agebin in allResultsDict["ageBins"]:
    #     allResultsDict["ageBins"][agebin].append(results[agebin])

    # sex_anySUD_df = queryDB.getSexSUDdata()
    # results = utils.logRegress(sex_anySUD_df)
    # for sex in allResultsDict["sexes"]:
    #     allResultsDict["sexes"][sex].append(results[sex])

    # setting_anySUD_df = queryDB.getSettingSUDdata()
    # results = utils.logRegress(setting_anySUD_df)
    # for setting in allResultsDict["settings"]:
    #     allResultsDict["settings"][setting].append(results[setting])

    # race_2SUD_df = queryDB.getRace2SUDdata()
    # results = utils.logRegress(race_2SUD_df)
    # for race in allResultsDict["races"]:
    #     allResultsDict["races"][race].append(results[race])

    # agebins_2SUD_df = queryDB.getAge2SUDdata()
    # results = utils.logRegress(agebins_2SUD_df)
    # for agebin in allResultsDict["ageBins"]:
    #     allResultsDict["ageBins"][agebin].append(results[agebin])

    # sex_2SUD_df = queryDB.getSex2SUDdata()
    # results = utils.logRegress(sex_2SUD_df)
    # for sex in allResultsDict["sexes"]:
    #     allResultsDict["sexes"][sex].append(results[sex])

    # setting_2SUD_df = queryDB.getSetting2SUDdata()
    # results = utils.logRegress(setting_2SUD_df)
    # for setting in allResultsDict["settings"]:
    #     allResultsDict["settings"][setting].append(results[setting])

    # print(allResultsDict)

    raceResultsDict = {
        "any_sud":{
            "ageBins": [],
            "sexes": [],
            "settings": []
        },
        "morethan2_sud":{
            "agebins": [],
            "sexes": [],
            "settings": []
        }
    }

    for race in allResultsDict["races"]:
        print(f"I AM IN {race}")

        ageList = []
        agebins_anySUD_race_df = queryDB_race.getAgeSUDdata(race)
        results = utils.logRegress(agebins_anySUD_race_df)
        for agebin in allResultsDict["ageBins"]:
            ageList.append(results[agebin])
        raceResultsDict["any_sud"]["ageBins"].append(ageList)

        sexList = []
        sex_anySUD_race_df = queryDB_race.getSexSUDdata(race)
        results = utils.logRegress(sex_anySUD_race_df)
        for sex in allResultsDict["sexes"]:
            sexList.append(results[sex])
        raceResultsDict["any_sud"]["sexes"].append(sexList)

        # # Singular Matrix Error for AA only
        # settingList = []
        # setting_anySUD_race_df = queryDB_race.getSettingSUDdata(race)
        # results = utils.logRegress(setting_anySUD_race_df)
        # for setting in allResultsDict["settings"]:
        #     settingList.append(results[setting])
        # raceResultsDict["any_sud"]["settings"].append(settingList)

        # # Singular Matrix Error
        # age2List = []
        # agebins_2SUD_race_df = queryDB_race.getAge2SUDdata(race)
        # results = utils.logRegress(agebins_2SUD_race_df)
        # for agebin in allResultsDict["ageBins"]:
        #     age2List.append(results[agebin])
        # raceResultsDict["morethan2_sud"]["ageBins"].append(ageList)

        sex2List = []
        sex_2SUD_race_df = queryDB_race.getSex2SUDdata(race)
        results = utils.logRegress(sex_2SUD_race_df)
        for sex in allResultsDict["sexes"]:
            sex2List.append(results[sex])
        raceResultsDict["morethan2_sud"]["sexes"].append(sex2List)

        # # Singular Matrix Error
        # setting2List = []
        # setting_2SUD_race_df = queryDB_race.getSetting2SUDdata(race)
        # results = utils.logRegress(setting_2SUD_race_df)
        # for setting in allResultsDict["settings"]:
        #     setting2List.append(results[setting])
        # raceResultsDict["morethan2_sud"]["settings"].append(setting2List)

    print(raceResultsDict)

    print('Getting out of module table3')
    print('-'*30)

    return

