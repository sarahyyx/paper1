from logs import logDecorator as lD 
import jsonref, pprint
import matplotlib.pyplot as plt
from tqdm import tqdm
import operator
import csv

from psycopg2.sql import SQL, Identifier, Literal

from lib.databaseIO import pgIO
from modules.fig1 import utils
from modules.fig1 import queryDB

config = jsonref.load(open('../config/config.json'))
logBase = config['logging']['logBase'] + '.modules.fig1.fig1'


@lD.log(logBase + '.doSomething')
def doSomething(logger):
    '''print a line
    
    This function simply prints a single line
    
    Parameters
    ----------
    logger : {logging.Logger}
        The logger used for logging error information
    '''

    print('We are in module 1')

    return

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

    countDict = {}

    # utils.genStr("../data/raw_data/dsmno.txt")
    # utils.genPatients()

    queryDB.genDiagCount()


    print('Getting out of fig1')
    print('-'*30)

    return

