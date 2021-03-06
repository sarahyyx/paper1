from logs import logDecorator as lD 
import jsonref, pprint

import json

from modules.reportWriter import writeTable1
from modules.reportWriter import plotFig1
from modules.reportWriter import writeTable2
from modules.reportWriter import writeTable3
from modules.reportWriter import writeTable4
from modules.reportWriter import writeAppendix

config = jsonref.load(open('../config/config.json'))
logBase = config['logging']['logBase'] + '.modules.reportWriter.reportWriter'

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

    # Table 1 Info
    with open("../data/final/sampleCount.json") as json_file:  
        table1Dict = json.load(json_file)
    writeTable1.genIntro()
    writeTable1.genRace(table1Dict)
    writeTable1.genRaceAge(table1Dict)
    writeTable1.genRaceSex(table1Dict)
    writeTable1.genRaceSetting(table1Dict)

    # Figure 1 Info
    with open("../data/final/diagnosesCount.json") as json_file:  
        fig1Dict = json.load(json_file)
    plotFig1.genIntro()
    plotFig1.genFig(fig1Dict)

    # Table 2 Info
    with open("../data/final/allAgesGeneralSUD.json") as json_file:  
        table2_dict1 = json.load(json_file)
    with open("../data/final/allAgesCategorisedSUD.json") as json_file:  
        table2_dict2 = json.load(json_file)
    with open("../data/final/ageBinnedGeneralSUD.json") as json_file:  
        table2_dict3 = json.load(json_file)
    with open("../data/final/ageBinnedCategorisedSUD.json") as json_file:  
        table2_dict4 = json.load(json_file)
    writeTable2.genIntro()
    writeTable2.genTotalPrev(table2_dict1,table2_dict2,table1Dict)
    writeTable2.genAAAgeBinnedPrev(table2_dict3,table2_dict4,table1Dict)
    writeTable2.genNHPIAgeBinnedPrev(table2_dict3,table2_dict4,table1Dict)
    writeTable2.genMRAgeBinnedPrev(table2_dict3,table2_dict4,table1Dict)

    # Table 3 Info
    with open("../data/final/oddsratios_allRaces.json") as json_file:  
        table3_dict1 = json.load(json_file)
    with open("../data/final/oddsratios_anysud_byRace.json") as json_file:  
        table3_dict2 = json.load(json_file)
    with open("../data/final/oddsratios_morethan2sud_byRace.json") as json_file:  
        table3_dict3 = json.load(json_file)
    writeTable3.genIntro()
    writeTable3.oddsRatiosAllRaces(table3_dict1,table1Dict)
    writeTable3.oddsRatiosByRace(table3_dict2, table3_dict3, table1Dict)

    # Table 4 Info
    with open("../data/final/table4data.json") as json_file:
        table4Dict = json.load(json_file)
    writeTable4.genIntro()
    writeTable4.oddsRatiosByRace(table4Dict, table1Dict)

    # Appendix (What databases are used)
    writeAppendix.genAppendix()

    print('Getting out of reportWriter module')
    print('-'*30)

    return

