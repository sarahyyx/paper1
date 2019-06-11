from logs import logDecorator as lD 
import jsonref, pprint
import matplotlib.pyplot as plt
from tqdm import tqdm
import operator
import csv, json

from psycopg2.sql import SQL, Identifier, Literal

from lib.databaseIO import pgIO
from modules.fig1 import utils
from modules.fig1 import queryDB

config = jsonref.load(open('../config/config.json'))
logBase = config['logging']['logBase'] + '.modules.fig1.fig1'


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
    print('Main function of fig1')
    print('='*30)

    countDict = queryDB.genDiagCount()

    print(countDict)

    obj = json.dumps(countDict)
    f = open("../data/final/diagnosesCount.json","w+")
    f.write(obj)
    f.close()

    print('Getting out of fig1')
    print('-'*30)

    return

