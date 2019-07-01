from logs import logDecorator as lD 
import jsonref, pprint
import numpy as np
import matplotlib.pyplot as plt

from psycopg2.sql import SQL, Identifier, Literal
from lib.databaseIO import pgIO
from collections import Counter

from tqdm import tqdm
from multiprocessing import Pool
from time import sleep

config = jsonref.load(open('../config/config.json'))
logBase = config['logging']['logBase'] + '.modules.reportWriter.reportWriter'

@lD.log(logBase + '.genAppendix')
def genAppendix(logger):
    
    report = f'''
    
## Appendix

|Schema          |Tables Used      |
|----------------|-----------------| 
|rwe_version1_1  |background       |
|                |typepatient      |
|                |pdiagnose        |


|Schema          |Tables Created   |
|----------------|-----------------| 
|sarah           |test2            |
|                |test3            |
|                |test4            |
        '''
    with open('../report/paper1Report.md', 'a+') as f:
        f.write( report )

    return

