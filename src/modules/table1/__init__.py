'''This module obtains the data needed to generate Table 1 of the report, by specifying the sample characteristics of the sample to be taken from the database.

This module creates two tables in the table. 
The first table is generated by filtering users by their race, age, sex and visit_type/setting and selecting those who meet the requirements in these areas.
The second table is then generated as a further filtered subset of the first table, where only users with DSM numbers of Axis I and II disorders are selected
Count functions then calculate the sample subgroup sizes and percentages to generate the data required for Table 1.   

Before you Begin
================

Make sure that the configuration files are properly set, as mentioned in the Specifications 
section. 

Make sure you have the csv file: DSM Numbers. Convert each sheet in the file into json format 
by using an online csv -> json converter, then copying the json file into the table1.json config
file under ["params"]["categories"].

Details of Operation
====================

Firstly, the function getRace() from table1.queryDB is run to generate the csv file raceCount, 
where first column "race" contains the race strings, second column "count" contains their counts, 
and the third column "paper_race" is manually filled in, which contains the overarching race specified in the paper.

Next, the function genRaceDict() from table1 is run to generate a dict that specifies all the str values under each overarching race.
These strings are then saved in the table1.json config file under ["params"]["races"].

TBC **To create the first table:
sarah.newtable1data
in getTable1data() from queryDB, run the query in Postgres ** 

To create the second table:
sarah.diagnoses
Run queryDB.genAllKeys() to generate a list of all the users' siteid, backgroundid in sarah.newtable1data
In Postgres, run a create table SQL query to create the table with the columns: (siteid, backgroundid, 
dsmnos, mood, anxiety, adjustment, adhd, sud, psyc, pers, childhood, impulse, cognitive, eating, smtf, disso, sleep, fd)
Run queryDB.addDiagCols() to add the user rows to the table.
In Postgres, run a delete from SQL Query to remove rows (users) that have no Axis I/II DSM disorder numbers.

Count functions in queryDB include:
countMainRace()
countRaceAge()
countRaceSex()
countRaceSetting()
These count functions generate the data and it is saved in a dict, which is converted into a results 
file: sampleCount.json under data/final.  

Results
=======

Tables created:
sarah.newtable1data
sarah.diagnoses

Files created:
../data/final/sampleCount.json

Specifications:
===============

Specifications for running the module is described below. Note that all the json files
unless otherwise specified will be placed in the folder ``config`` in the main project
folder.

Specifications for the database:
--------------------------------

sarah.newtable1data
sarah.diagnoses

Specifications for ``modules.json``
-----------------------------------

Make sure that the ``execute`` statement within the modules file is set to True. 

.. code-block:: python
    :emphasize-lines: 3

    "moduleName" : "table1",
    "path"       : "modules/table1/table1.py",
    "execute"    : true,
    "description": "",
    "owner"      : ""


Specification for table1.json
-----------------------------------
Ensure that the str values for each race are specified under ["params"]["races"][race]. 
Do the same for sexes, settings and categories (DSM numbers).

'''