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
logBase = config['logging']['logBase'] + '.modules.table1.reportWriter'

@lD.log(logBase + '.genIntro')
def genIntro(logger):
    
    report = f'''

## Description of Figure 1:
The Axis I/II disorders that are considered and their abbreviations are as follows:
Mood - mood
Anxiety - anxiety
Adjustment - adjustment
ADHD/CD/ODD/DBD - adhd
Substance Use Disorder - sud
Psychotic - psyc
Personality - pers
Childhood-onset - childhood
Impulse-control - impulse
Cognitive - cognitive
Eating - eating
Somatoform - smtf
Dissociation - disso
Sleep - sleep
Factitious Disorders - fd

        '''
    with open('../report/table1Report.md', 'a+') as f:
        f.write( report )

    return

@lD.log(logBase + '.genFig')
def genFig(logger, r):
    try:
        print("Plotting Figure 1...")

        barWidth = 0.25
        
        print(r)

        AAbars = []
        NHPIbars = []
        MRbars = []
        
        for category in r:
            AAbars.append(r[category][0])
            NHPIbars.append(r[category][1])
            MRbars.append(r[category][2])

        print(AAbars, NHPIbars, MRbars)

        r1 = np.arange(len(AAbars))
        r2 = [x + barWidth for x in r1]
        r3 = [x + barWidth for x in r2]

        plt.bar(r1, AAbars, color='#000000', width=barWidth, edgecolor='white', label='AA')
        plt.bar(r2, NHPIbars, color='#3360CC', width=barWidth, edgecolor='white', label='NHPI')
        plt.bar(r3, MRbars, color='#A2D729', width=barWidth, edgecolor='white', label='MR')

        plt.xticks([r + barWidth for r in range(len(AAbars))], list(r.keys()), fontsize=8, rotation=30)

        plt.legend()

        plt.savefig('../results/diagnosesPercentageGraph.png', dpi=300)
        plt.close()

    except Exception as e:
        logger.error('Failed to generate figure {}'.format(e))
    return

