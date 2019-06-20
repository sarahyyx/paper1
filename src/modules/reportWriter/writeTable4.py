from logs import logDecorator as lD 
import jsonref, pprint

from psycopg2.sql import SQL, Identifier, Literal
from lib.databaseIO import pgIO
from collections import Counter

from tqdm import tqdm
from multiprocessing import Pool
from time import sleep

config = jsonref.load(open('../config/config.json'))
logBase = config['logging']['logBase'] + '.modules.reportWriter.reportWriter'

@lD.log(logBase + '.genIntro')
def genIntro(logger):
    
    report = f'''
***
## Description of Table 4:
This table contains the odds ratios and confidence intervals after a logistic regression is performed for each race:
* Asian Americans, aged 12 and older
* Native Hawaiian, aged 12 and older
* Mixed Race, aged 12 and older

Logistic regression is performed for comorbidity of any SUD with other mental health disorders in the list below:
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
    with open('../report/paper1Report.md', 'a+') as f:
        f.write( report )

    return

@lD.log(logBase + '.oddsRatiosByRace')
def oddsRatiosByRace(logger, r1, r2):

    sampleabove12 = {
        "AA": 0,
        "NHPI": 0,
        "MR": 0
    }

    for race in r2:
        for i in range(1,5):
            sampleabove12[race] += r2[race][1][i]

    report = f'''

### Asian Americans, aged 12 or older
|Logistic Regression, Any SUD|N = {sampleabove12["AA"]}   |          |
|----------------------------|----------------------------|----------|
|**DSM-IV Diagnosis**        |**Odds Ratio**              |**95% CI**|'''
    
    for disorder in r1:
        report = report + f'''
|{disorder}                  |{r1[disorder][0][0]}        |{r1[disorder][0][1]} - {r1[disorder][0][2]}|'''

    report = report + f'''
***'''

    report = report + f'''
### Native Hawaiians/Pacific Islanders, aged 12 or older
|Logistic Regression, Any SUD|N = {sampleabove12["NHPI"]} |          |
|----------------------------|----------------------------|----------|
|**DSM-IV Diagnosis**        |**Odds Ratio**              |**95% CI**|'''

    for disorder in r1:
        report = report + f'''
|{disorder}                  |{r1[disorder][1][0]}        |{r1[disorder][1][1]} - {r1[disorder][1][2]}|'''

    report = report + f'''
***'''

    report = report + f'''
### Mixed Race, aged 12 or older
|Logistic Regression, Any SUD|N = {sampleabove12["MR"]}   |          |
|----------------------------|----------------------------|----------|
|**DSM-IV Diagnosis**        |**Odds Ratio**              |**95% CI**|'''

    for disorder in r1:
        report = report + f'''
|{disorder}                  |{r1[disorder][2][0]}        |{r1[disorder][2][1]} - {r1[disorder][2][2]}|'''

    report = report + f'''
***'''

    with open('../report/paper1Report.md', 'a+') as f:
        f.write( report )

    return

