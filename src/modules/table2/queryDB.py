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
            sud = true
        '''

        data = pgIO.getAllData(query)
        data = [(d[0], d[1]) for d in data]

        csvfile = "../data/raw_data/SUDUser_keys.csv"

        with open(csvfile,'w+') as output:
            csv_output=csv.writer(output)

            for row in data:
                csv_output.writerow(row)
        output.close()

    except Exception as e:
        logger.error('Failed to generate list of SUD users because of {}'.format(e))

    return 

@lD.log(logBase + '.createSUDcatsTable')
def createSUDcatsTable(logger):
    '''[summary]
    
    [description]
    
    Decorators:
        lD.log
    
    Arguments:
        logger {[type]} -- [description]
    '''
    try:
        all_userkeys = "../data/raw_data/SUDUser_keys.csv"

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
                    Literal(table2_config["params"]["sudcats"]["alc"]),
                    Literal(table2_config["params"]["sudcats"]["cannabis"]),
                    Literal(table2_config["params"]["sudcats"]["amphe"]),
                    Literal(table2_config["params"]["sudcats"]["halluc"]),
                    Literal(table2_config["params"]["sudcats"]["nicotin"]),
                    Literal(table2_config["params"]["sudcats"]["cocaine"]),
                    Literal(table2_config["params"]["sudcats"]["opioids"]),
                    Literal(table2_config["params"]["sudcats"]["sedate"]),
                    Literal(table2_config["params"]["sudcats"]["others"]),
                    Literal(table2_config["params"]["sudcats"]["polysub"]),
                    Literal(table2_config["params"]["sudcats"]["inhalant"]),
                    Literal(user[0]),
                    Literal(user[1])
                )

                data = pgIO.getAllData(getQuery)

                pushQuery = '''
                INSERT INTO 
                    sarah.sudcats(siteid, backgroundid, alc, cannabis, amphe, halluc, nicotin, cocaine, opioids, sedate, others, polysub, inhalant)
                VALUES
                    %s
                '''

                print(pgIO.commitDataList(pushQuery, data))


    except Exception as e:
        logger. error('Failed to create sudcats table because of {}'.format(e))
    return

@lD.log(logBase + '.allAgesGeneralSUD')
def allAgesGeneralSUD(logger):
    try:

        countDict = {
            "any_sud": [],
            "morethan2_sud": []
        }

        # Find number of users in each race who have any SUD
        any_sud = []
        for race in table2_config["inputs"]["races"]:
            query = SQL('''
            SELECT 
                count(*)
            FROM 
                sarah.newtable1data t1
            INNER JOIN
                sarah.sudcats t2
            ON
                t1.siteid = t2.siteid 
            AND
                t1.backgroundid = t2.backgroundid
            WHERE 
                t1.race = {}
            ''').format(
                Literal(race)
            )
            data = [d[0] for d in pgIO.getAllData(query)]
            countDict["any_sud"].append(data[0])

        # Find number of users in each race who have >2 SUD
        count = {
            "AA": 0,
            "NHPI": 0,
            "MR": 0
        }

        for race in table2_config["inputs"]["races"]:
            query = SQL('''
            SELECT 
                t2.alc,
                t2.cannabis,
                t2.amphe,
                t2.halluc,
                t2.nicotin,
                t2.cocaine,
                t2.opioids,
                t2.sedate,
                t2.others,
                t2.polysub,
                t2.inhalant
            FROM
                sarah.newtable1data t1
            INNER JOIN 
                sarah.sudcats t2
            ON
                t1.siteid = t2.siteid 
            AND
                t1.backgroundid = t2.backgroundid
            WHERE 
                t1.race = {}
            ''').format(
                Literal(race)
            )
            data = pgIO.getAllData(query)
            for tuple in data:
                if sum(list(tuple))>=2:
                    count[race]+=1
        for race in count:
            countDict["morethan2_sud"].append(count[race])
        print(countDict)

    except Exception as e:
        logger.error('Failed to find general SUD counts because of {}'.format(e))

    return countDict

@lD.log(logBase + '.allAgesCategorisedSUD')
def allAgesCategorisedSUD(logger):
    try:
        countDict = {
            "alc":[],
            "cannabis":[],
            "amphe":[],
            "halluc":[],
            "nicotin":[],
            "cocaine":[],
            "opioids":[],
            "sedate":[],
            "others":[],
            "polysub":[],
            "inhalant":[]
        }

        for race in table2_config["inputs"]["races"]:
            for sudcat in table2_config["params"]["sudcats"]:
                query = SQL('''
                SELECT 
                    count(*) 
                FROM 
                    sarah.newtable1data t1
                INNER JOIN 
                    sarah.sudcats t2
                ON 
                    t1.siteid = t2.siteid 
                AND 
                    t1.backgroundid = t2.backgroundid
                WHERE 
                    t1.race = {}
                AND 
                    t2.{} = true
                ''').format(
                    Literal(race),
                    Identifier(sudcat)
                )
                data = [d[0] for d in pgIO.getAllData(query)]
                countDict[sudcat].append(data[0])

    except Exception as e:
        logger.error('Failed to find categorised SUD counts because of {}'.format(e))

    return countDict

@lD.log(logBase + '.ageBinnedGeneralSUD')
def ageBinnedGeneralSUD(logger):
    try:

        countDict = {
            "any_sud": [],
            "morethan2_sud": []
        }

        # Find number of users in each race who have any SUD, separated into age bins
        any_sud = []
        for race in table2_config["inputs"]["races"]:
            counts = []
            for lower, upper in zip(['1', '12', '18', '35', '50'], ['11', '17', '34', '49', '100']):
                query = SQL('''
                SELECT 
                    count(*)
                FROM 
                    sarah.newtable1data t1
                INNER JOIN 
                    sarah.diagnoses t2
                ON 
                    t1.siteid = t2.siteid 
                AND 
                    t1.backgroundid = t2.backgroundid
                WHERE 
                    t1.race = {} 
                AND 
                    t1.age BETWEEN {} AND {}
                AND
                    t2.sud = true
                ''').format(
                    Literal(race),
                    Literal(lower),
                    Literal(upper)
                )
                data = [d[0] for d in pgIO.getAllData(query)]
                counts.append(data[0])
            countDict["any_sud"].append(counts)

        # Find number of users in each race who have >2 SUD, separated into age bins
        count = {
            "AA": {
                "1": 0,
                "12": 0,
                "18": 0,
                "35": 0,
                "50": 0
            },
            "NHPI": {
                "1": 0,
                "12": 0,
                "18": 0,
                "35": 0,
                "50": 0
            },
            "MR": {
                "1": 0,
                "12": 0,
                "18": 0,
                "35": 0,
                "50": 0
            }
        }

        for race in table2_config["inputs"]["races"]:
            for lower, upper in zip(['1', '12', '18', '35', '50'], ['11', '17', '34', '49', '100']):

                query = SQL('''
                SELECT 
                    t2.alc,
                    t2.cannabis,
                    t2.amphe,
                    t2.halluc,
                    t2.nicotin,
                    t2.cocaine,
                    t2.opioids,
                    t2.sedate,
                    t2.others,
                    t2.polysub,
                    t2.inhalant
                FROM
                    sarah.newtable1data t1
                INNER JOIN 
                    sarah.sudcats t2
                ON
                    t1.siteid = t2.siteid 
                AND
                    t1.backgroundid = t2.backgroundid
                WHERE 
                    t1.race = {}
                AND
                    t1.age BETWEEN {} AND {}
                ''').format(
                    Literal(race),
                    Literal(lower),
                    Literal(upper)
                )
                data = pgIO.getAllData(query)
                for tuple in data:
                    if sum(list(tuple))>=2:
                        count[race][lower]+=1

        for race in count:
            countDict["morethan2_sud"].append(list(count[race].values()))

    except Exception as e:
        logger.error('Failed to find general SUD counts because of {}'.format(e))

    return countDict

@lD.log(logBase + '.ageBinnedCategorisedSUD')
def ageBinnedCategorisedSUD(logger):
    try:
        countDict = {}

        for sudcat in table2_config["params"]["sudcats"].keys():
            list1 = []
            for race in table2_config["inputs"]["races"]:
                list2 = []
                for lower, upper in zip(['1', '12', '18', '35', '50'], ['11', '17', '34', '49', '100']):
                    query = SQL('''
                    SELECT 
                        count(*) 
                    FROM 
                        sarah.newtable1data t1
                    INNER JOIN 
                        sarah.sudcats t2
                    ON 
                        t1.siteid = t2.siteid 
                    AND 
                        t1.backgroundid = t2.backgroundid
                    WHERE 
                        t1.race = {}
                    AND 
                        t1.age BETWEEN {} AND {}
                    AND 
                        t2.{} = true
                    ''').format(
                        Literal(race),
                        Literal(lower),
                        Literal(upper),
                        Identifier(sudcat)
                    )
                    data = [d[0] for d in pgIO.getAllData(query)]
                    list2.append(data[0])
                list1.append(list2)
            countDict[sudcat] = list1

        # print(countDict)

    except Exception as e:
        logger.error('Failed to find categorised SUD counts because of {}'.format(e))

    return countDict 