from logs import logDecorator as lD 
import jsonref, pprint

from psycopg2.sql import SQL, Identifier, Literal
from lib.databaseIO import pgIO
from collections import Counter

from tqdm import tqdm
from multiprocessing import Pool
from time import sleep

config = jsonref.load(open('../config/config.json'))
dbSummary_config = jsonref.load(open('../config/modules/table1.json'))
logBase = config['logging']['logBase'] + '.modules.table1.reportWriter'

@lD.log(logBase + '.genIntro')
def genIntro(logger):
    
    report = f'''

# Report on Paper 1: Comorbid Substance Use Disorders

## Abstract: 
This report will generate the information required for Table 1 of the paper.

## Description of Table 1:
The three races considered and their abbreviations are as follows:
Asian Americans - AA
Native Hawaiian/Pacific Islander - NH/PI
Multi-Racial - MR

Other variables of interest are:
Age
Sex
Setting

        '''
    with open('../report/table1Report.md', 'w+') as f:
        f.write( report )

    return

@lD.log(logBase + '.genRace')
def genRace(logger, r):

    report = f'''
|Race |Count          |
|-----|---------------| 
|AA   |{r["AA"][0]}   |
|NH/PI|{r["NH/PI"][0]}|
|MR   |{r["MR"][0]}   |
'''

    with open('../report/table1Report.md', 'a+') as f:
        f.write( report )

    return

@lD.log(logBase + '.genPC')
def genPC(logger, n, d):
    result = round((n/d)*100, 1)
    return result


@lD.log(logBase + '.genRaceAge')
def genRaceAge(logger, r):

    report = f'''
### Number of patients grouped by race and age
|Age  |AA|%|NH/PI|%|MR|%|
|-----|--|-|-----|-|--|-|
|1-11 |{r["AA"][1][0]}|{genPC(r["AA"][1][0],r["AA"][0])}|{r["NH/PI"][1][0]}|{genPC(r["NH/PI"][1][0],r["NH/PI"][0])}|{r["MR"][1][0]}|{genPC(r["MR"][1][0],r["MR"][0])}|
|12-17|{r["AA"][1][1]}|{genPC(r["AA"][1][1],r["AA"][0])}|{r["NH/PI"][1][1]}|{genPC(r["NH/PI"][1][1],r["NH/PI"][0])}|{r["MR"][1][1]}|{genPC(r["MR"][1][1],r["MR"][0])}|
|18-34|{r["AA"][1][2]}|{genPC(r["AA"][1][2],r["AA"][0])}|{r["NH/PI"][1][2]}|{genPC(r["NH/PI"][1][2],r["NH/PI"][0])}|{r["MR"][1][2]}|{genPC(r["MR"][1][2],r["MR"][0])}|
|35-49|{r["AA"][1][3]}|{genPC(r["AA"][1][3],r["AA"][0])}|{r["NH/PI"][1][3]}|{genPC(r["NH/PI"][1][3],r["NH/PI"][0])}|{r["MR"][1][3]}|{genPC(r["MR"][1][3],r["MR"][0])}|
|50+  |{r["AA"][1][4]}|{genPC(r["AA"][1][4],r["AA"][0])}|{r["NH/PI"][1][4]}|{genPC(r["NH/PI"][1][4],r["NH/PI"][0])}|{r["MR"][1][4]}|{genPC(r["MR"][1][4],r["MR"][0])}|
'''

    with open('../report/table1Report.md', 'a+') as f:
        f.write( report )

    return

@lD.log(logBase + '.genRaceSex')
def genRaceSex(logger, r):

    report = f'''
### Number of patients grouped by race and sex
|Sex|AA|%|NH/PI|%|MR|%|
|---|--|-|-----|-|--|-|
|Male  |{r["AA"][2][0]}|{genPC(r["AA"][2][0],r["AA"][0])}%|{r["NH/PI"][2][0]}|{genPC(r["NH/PI"][2][0],r["NH/PI"][0])}%|{r["MR"][2][0]}|{genPC(r["MR"][2][0],r["MR"][0])}%|
|Female|{r["AA"][2][1]}|{genPC(r["AA"][2][1],r["AA"][0])}%|{r["NH/PI"][2][1]}|{genPC(r["NH/PI"][2][1],r["NH/PI"][0])}%|{r["MR"][2][1]}|{genPC(r["MR"][2][1],r["MR"][0])}%|
'''

    with open('../report/table1Report.md', 'a+') as f:
        f.write( report )

    return

@lD.log(logBase + '.genRaceSetting')
def genRaceSetting(logger, r):

    report = f'''
### Number of patients grouped by race and setting
|Setting|AA|%|NH/PI|%|MR|%|
|-------|--|-|-----|-|--|-|
|Hospital            |{r["AA"][3][0]}|{genPC(r["AA"][3][0],r["AA"][0])}|{r["NH/PI"][3][0]}|{genPC(r["NH/PI"][3][0],r["NH/PI"][0])}|{r["MR"][3][0]}|{genPC(r["MR"][3][0],r["MR"][0])}|
|Mental Health Center|{r["AA"][3][1]}|{genPC(r["AA"][3][1],r["AA"][0])}|{r["NH/PI"][3][1]}|{genPC(r["NH/PI"][3][1],r["NH/PI"][0])}|{r["MR"][3][1]}|{genPC(r["MR"][3][1],r["MR"][0])}|
'''

    with open('../report/table1Report.md', 'a+') as f:
        f.write( report )

    return
