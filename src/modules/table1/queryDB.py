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
table1_config = jsonref.load(open('../config/modules/table1.json'))
logBase = config['logging']['logBase'] + '.modules.table1.table1'

@lD.log(logBase + '.getRace')
def getRace(logger):
    '''Generates raceCount.csv
    
    This function was used to generate the data for the raceCount.csv file, which 
    gets the race and count(race) for ALL the races in raw_data.background.
    After manual selection and grouping, the races under each race in the paper (AA, NHPI, MR) were manually entered into the json config file
    Function was deleted from the main after use.
    
    Parameters
    ----------
    logger : {logging.Logger}
        The logger used for logging error information
    '''

    try:
        
        query = '''
        SELECT 
        race,
        COUNT(race)
        FROM raw_data.background
        GROUP BY race
        '''

        data = pgIO.getAllData(query)
        # data = [d[0] for d in data]

    except Exception as e:
        logger.error('getRace failed because of {}'.format(e))

    return data

@lD.log(logBase + '.getTable1data')
def createTest1(logger):
    '''Creates the table sarah.test1
    
    This function gets the number of unique users using their (siteid,backgroundid) key that fit the sample requirements of the paper
    Variables that are used to filter at this stage are age, visit_type, sex and race. 
    Variable values that are to be included are found in the config file
    
    Parameters
    ----------
    logger : {logging.Logger}
        The logger used for logging error information
    '''

    try:
        query = SQL('''
        INSERT INTO sarah.test1(age, visit_type, sex, race, siteid, backgroundid)
        SELECT 
            t1.age,
            t1.visit_type, 
            t2.sex,
            t2.race,
            t1.siteid,
            t1.backgroundid
        FROM 
            raw_data.typepatient t1
        INNER JOIN 
            raw_data.background t2
        ON
            t1.backgroundid = t2.id
        AND
            t1.siteid = t2.siteid
        WHERE 
            CAST (t1.age AS INTEGER) < 100
        AND
            t1.visit_type in {}
        AND
            t2.sex in {}
        AND
            t2.race in {}
        AND 
            t2.ethnicity not ilike 'Hisp%'
        ''').format(
            Literal(tuple(table1_config["params"]["setting"]["all"])),
            Literal(tuple(table1_config["params"]["sexes"]["all"])),
            Literal(tuple(table1_config["params"]["races"]["all"]))
            )
    except Exception as e:
        logger.error('Failed to generate table {}'.format(e))
    return

@lD.log(logBase + '.countMainRace')
def countMainRace(logger):
    '''
    
    This function queries the database and returns the counts of each main race: AA, NHPI, MR   
    
    Parameters
    ----------
    logger : {logging.Logger}
        The logger used for logging error information
    '''

    try:
        total = []
        for race in table1_config["inputs"]["races"]:
            query = SQL('''
            SELECT
                COUNT(*)
            FROM 
                sarah.test2 t1
            INNER JOIN 
                sarah.test3 t2
            ON
                t1.patientid = t2.patientid
            WHERE
                race = {}
            ''').format(
                Literal(race)
            )
            data = [d[0] for d in pgIO.getAllData(query)]
            total.append(data[0])

    except Exception as e:
        logger.error('countMainRace failed because of {}'.format(e))

    return total

@lD.log(logBase + '.countRaceAge')
def countRaceAge(logger):
    '''
    
    This function queries the database and returns the counts of each main race: AA, NHPI, MR sorted into age bins.

    Parameters
    ----------
    logger : {logging.Logger}
        The logger used for logging error information
    '''

    try:
        total = []
        for race in table1_config["inputs"]["races"]:
            counts = []
            for lower, upper in zip(['1', '12', '18', '35', '50'], ['11', '17', '34', '49', '100']):
                query = SQL('''
                SELECT
                    count(*)
                FROM 
                    sarah.test2 t1
                INNER JOIN 
                    sarah.test3 t2
                ON
                    t1.patientid = t2.patientid
                WHERE 
                    t1.age >= {} AND t1.age <= {} and t1.race = {}
                ''').format(
                    Literal(lower),
                    Literal(upper),
                    Literal(race)
                )
                data = [d[0] for d in pgIO.getAllData(query)]
                #print("age range: "+str(lower)+"-"+ str(upper)+" count: "+str(data))
                counts.append(data[0])
            total.append(counts)

    except Exception as e:
        logger.error('countRaceAge failed because of {}'.format(e))

    return total

@lD.log(logBase + '.countRaceSex')
def countRaceSex(logger):
    '''
    
    This function queries the database and returns the counts of each main race: AA, NHPI, MR sorted by sex.

    Parameters
    ----------
    logger : {logging.Logger}
        The logger used for logging error information
    '''

    try:
        total = []
        for race in table1_config["inputs"]["races"]:
            counts = []
            for sex in table1_config["inputs"]["sexes"]:
                query = SQL('''
                SELECT
                    count(*)
                FROM 
                    sarah.test2 t1
                INNER JOIN 
                    sarah.test3 t2
                ON
                    t1.patientid = t2.patientid
                WHERE 
                    t1.sex = {} AND t1.race = {}
                ''').format(
                    Literal(sex),
                    Literal(race)
                )
                data = [d[0] for d in pgIO.getAllData(query)]
                counts.append(data[0])
            total.append(counts)

    except Exception as e:
        logger.error('countRaceSex failed because of {}'.format(e))

    return total

@lD.log(logBase + '.countRaceSetting')
def countRaceSetting(logger):
    '''
    
    This function queries the database and returns the counts of each main race: AA, NHPI, MR sorted by treatment setting.

    Parameters
    ----------
    logger : {logging.Logger}
        The logger used for logging error information
    '''

    try:
        total = []
        for race in table1_config["inputs"]["races"]:
            counts = []
            for setting in table1_config["inputs"]["settings"]:
                query = SQL('''
                SELECT
                    count(*)
                FROM 
                    sarah.test2 t1
                INNER JOIN 
                    sarah.test3 t2
                ON
                    t1.patientid = t2.patientid
                WHERE 
                    t1.visit_type = {} AND t1.race = {}
                ''').format(
                    Literal(setting),
                    Literal(race)
                )
                data = [d[0] for d in pgIO.getAllData(query)]
                counts.append(data[0])
            total.append(counts)

    except Exception as e:
        logger.error('countRaceSetting failed because of {}'.format(e))

    return total

@lD.log(logBase + '.genAllKeys')
def genAllKeys(logger):
    '''
    
    This function generates a .csv file of (siteid, backgroundid) of users after the first filter of age, race, sex and setting are done.
    The .csv file will then be used for the second filter by dsmno.
    
    Parameters
    ----------
    logger : {logging.Logger}
        The logger used for logging error information
    '''
    try: 
        query = '''
        SELECT 
            patientid
        FROM
            sarah.test2
        '''

        data = pgIO.getAllData(query)

        csvfile = "../data/raw_data/firstfilter_allkeys.csv"

        with open(csvfile,'w+') as output:
            csv_output=csv.writer(output)

            for row in data:
                csv_output.writerow(row)
        output.close()

    except Exception as e:
        logger.error('Failed to generate list of patients because of {}'.format(e))

    return 

@lD.log(logBase + '.createTest3')
def createTest3(logger):
    '''Creates sarah.test3 table
    
    Decorators:
        lD.log
    
    Arguments:
        logger {[type]} -- [description]
    '''
    try:
        query = '''
        CREATE TABLE sarah.test3(
            patientid text,
            mood bool,
            anxiety bool,
            adjustment bool,
            adhd bool,
            sud bool,
            psyc bool,
            pers bool,
            childhood bool,
            impulse bool, 
            cognitive bool,
            eating bool,
            smtf bool,
            disso bool,
            sleep bool,
            fd bool
            )'''
        value = pgIO.commitData(query)
        if value == True:
            print("sarah.test3 table has been successfully created")
    except Exception as e:
        logger.error('Unable to create table test3 because {}'.format(e))
    return

@lD.log(logBase + '.popDiagCols')
def popDiagCols(logger):
    '''Populates sarah.test3 table
    
    Using the .csv file of the first filtered users' [siteid, backgroundid], these users' DSM numbers are aggregated into an array and compared against the array of DSM numbers of a specific diagnosis.
    If the user's DSM numbers are found in the diagnosis array, the column representing the diagnosis is filled in with a "True" value for the user, and vice versa.
    The columns created are stored in a new table sarah.test3, then the second filter is completed by removing users that have all their diagnosis columns set to "False" (i.e. they have no mental disorder test3 that we have specified) 
    
    Decorators:
        lD.log
    
    Arguments:
        logger {[type]} -- [description]
    '''
    try:
        all_userkeys = "../data/raw_data/firstfilter_allkeys.csv"

        with open(all_userkeys) as f:
            readCSV = csv.reader(f, delimiter=",")

            for user in tqdm(readCSV):

                getQuery = SQL('''
                SELECT
                    patientid,
                    array_agg(distinct cast(dsmno as text)) && array[{}] as mood,
                    array_agg(distinct cast(dsmno as text)) && array[{}] as anxiety,
                    array_agg(distinct cast(dsmno as text)) && array[{}] as adjustment,
                    array_agg(distinct cast(dsmno as text)) && array[{}] as adhd,
                    array_agg(distinct cast(dsmno as text)) && array[{}] as sud,
                    array_agg(distinct cast(dsmno as text)) && array[{}] as psyc,
                    array_agg(distinct cast(dsmno as text)) && array[{}] as pers,
                    array_agg(distinct cast(dsmno as text)) && array[{}] as childhood,
                    array_agg(distinct cast(dsmno as text)) && array[{}] as impulse,
                    array_agg(distinct cast(dsmno as text)) && array[{}] as cognitive,
                    array_agg(distinct cast(dsmno as text)) && array[{}] as eating,
                    array_agg(distinct cast(dsmno as text)) && array[{}] as smtf,
                    array_agg(distinct cast(dsmno as text)) && array[{}] as disso,
                    array_agg(distinct cast(dsmno as text)) && array[{}] as sleep,
                    array_agg(distinct cast(dsmno as text)) && array[{}] as fd
                FROM
                    rwe_version1_1.pdiagnose
                WHERE
                    patientid = {}
                GROUP BY
                    patientid
                ''').format(
                    Literal(table1_config["params"]["categories"]["mood"]),
                    Literal(table1_config["params"]["categories"]["anxiety"]),
                    Literal(table1_config["params"]["categories"]["adjustment"]),
                    Literal(table1_config["params"]["categories"]["adhd"]),
                    Literal(table1_config["params"]["categories"]["sud"]),
                    Literal(table1_config["params"]["categories"]["psyc"]),
                    Literal(table1_config["params"]["categories"]["pers"]),
                    Literal(table1_config["params"]["categories"]["childhood"]),
                    Literal(table1_config["params"]["categories"]["impulse"]),
                    Literal(table1_config["params"]["categories"]["cognitive"]),
                    Literal(table1_config["params"]["categories"]["eating"]),
                    Literal(table1_config["params"]["categories"]["smtf"]),
                    Literal(table1_config["params"]["categories"]["disso"]),
                    Literal(table1_config["params"]["categories"]["sleep"]),
                    Literal(table1_config["params"]["categories"]["fd"]),
                    Literal(int(user[0]))
                )
                

                data = pgIO.getAllData(getQuery)

                pushQuery = '''
                INSERT INTO 
                    sarah.test3(patientid, mood, anxiety, adjustment, adhd, sud, psyc, pers, childhood, impulse, cognitive, eating, smtf, disso, sleep, fd)
                VALUES
                    %s
                '''
                print(pgIO.commitDataList(pushQuery, data))

                deleteDupliQuery = '''
                DELETE FROM sarah.test3 a USING (
                    SELECT MAX(ctid) as ctid, patientid
                    FROM sarah.test3
                    GROUP BY patientid HAVING count(*) > 1
                    ) b
                WHERE a.patientid = b.patientid
                AND a.ctid <> b.ctid
                '''
                value = pgIO.commitData(deleteDupliQuery)
                if value == True:
                    print("Duplicate values succesfully deleted")
        f.close()


    except Exception as e:
        logger.error('Failed to add columns because of {}'.format(e))
    return

@lD.log(logBase + '.delAllFalseTest3')
def delAllFalseTest3(logger):
    '''
    
    Decorators:
        lD.log
    
    Arguments:
        logger {[type]} -- [description]
    '''
    try:
        query = '''
        DELETE FROM 
            sarah.test3
        WHERE
            mood = false and 
            anxiety = false and
            adjustment = false and
            adhd = false and
            sud = false and
            psyc = false and
            pers = false and
            childhood = false and
            impulse = false and 
            cognitive = false and
            eating = false and
            smtf = false and
            disso = false and
            sleep = false and
            fd = false'''
        value = pgIO.commitData(query)
        if value == True:
            print("sarah.test3 table has been successfully deleted from")
    except Exception as e:
        logger.error('Unable to delete from table test3 because {}'.format(e))
    return

@lD.log(logBase + '.relabelVar')
def relabelVar(logger):
    '''Relabels column values
    
    This function relabels Sex, Race, Settings values to standardised values.
    
    Decorators:
        lD.log
    
    Arguments:
        logger {[type]} -- [description]
    '''
    try:
        # relabel_sex_success = []
        # for sex in table1_config["inputs"]["sexes"]:
        #     sex_query = SQL('''
        #     UPDATE sarah.test2
        #     SET sex = {}
        #     WHERE sex in {}
        #     ''').format(
        #         Literal(sex),
        #         Literal(tuple(table1_config["params"]["sexes"][sex])) 
        #         )
        #     relabel_sex_success.append(pgIO.commitData(sex_query))
        # if False in relabel_sex_success:
        #     print("Relabelling sex not successful!")

        relabel_race_success = []
        for race in table1_config["inputs"]["races"]:
            race_query = SQL('''
            UPDATE sarah.test2
            SET race = {}
            WHERE race in {}
            ''').format(
                Literal(race),
                Literal(tuple(table1_config["params"]["races"][race])) 
                )
            relabel_race_success.append(pgIO.commitData(race_query))
        if False in relabel_race_success:
            print("Relabelling race not successful!")

        relabel_setting_success = []
        for setting in table1_config["inputs"]["settings"]:
            setting_query = SQL('''
            UPDATE sarah.test2
            SET visit_type = {}
            WHERE visit_type in {}
            ''').format(
                Literal(setting),
                Literal(tuple(table1_config["params"]["settings"][setting])) 
                )
            relabel_setting_success.append(pgIO.commitData(setting_query))
        if False in relabel_setting_success:
            print("Relabelling setting not successful!")

    except Exception as e:
        logger.error('Failed to update table test2 because {}'.format(e))

@lD.log(logBase + '.genSampleUserKeys')
def genSampleUserKeys(logger):

    try:
        
        query = '''
        SELECT 
            patientid
        FROM 
            sarah.test3
        '''

        data = pgIO.getAllData(query)

    except Exception as e:
        logger.error('getRace failed because of {}'.format(e))

    return data
