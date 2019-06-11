from logs import logDecorator as lD 
import jsonref, pprint

import json

from modules.reportWriter import writeTable1
from modules.reportWriter import plotFig1

config = jsonref.load(open('../config/config.json'))
logBase = config['logging']['logBase'] + '.modules.module1.module1'


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
    print('Main function of reportWriter module')
    print('='*30)

    with open("../data/final/sampleCount.json") as json_file:  
        table1Dict = json.load(json_file)
    
    writeTable1.genIntro()
    writeTable1.genRace(table1Dict)
    writeTable1.genRaceAge(table1Dict)
    writeTable1.genRaceSex(table1Dict)
    writeTable1.genRaceSetting(table1Dict)

    with open("../data/final/diagnosesCount.json") as json_file:  
        fig1Dict = json.load(json_file)
    
    plotFig1.genIntro()
    plotFig1.genFig(fig1Dict)

    print('Getting out of reportWriter module')
    print('-'*30)

    return

