'''This module obtains the data needed to generate Table 2 of the report

This module creates a new table in the database which contains all the SUD users and the specific 
substance which they have a disorder for.

Before you Begin
================

Make sure that the configuration files are properly set, as mentioned in the Specifcations 
section. 

Make sure you have the csv file: DSM Numbers. Convert each sheet in the file into json format 
by using an online csv -> json converter, then copying the json file into the table1.json config
file under ["params"]["sudcats"].

Make sure that the functions below are un-commented if it is your first time running the code.
.. code-block:: python
    queryDB.genSUDUserKeys()
    queryDB.createTest4Table()
    queryDB.popTest4()

Details of Operation
====================

Firstly, the function genSUDUserKeys() from table2.queryDB generates a csv file of of 
all the users who have a SUD from sarah.test3. Then, createTest4Table() creates the 
table sarah.test4 in the database, and is populated by popTest4().

The count functions:
allAgesGeneralSUD()
allAgesCategorisedSUD()
ageBinnedGeneralSUD()
ageBinnedCategorisedSUD()
then use the data from sarah.test3 and sarah.test4 to generate the required prevalences.

Results
=======

Tables created:
sarah.test4

Files created:
../data/final/allAgesGeneralSUD.json
../data/final/allAgesCategorisedSUD.json
../data/final/ageBinnedGeneralSUD.json
../data/final/ageBinnedCategorisedSUD.json

Specifications:
===============

Specifications for running the module is described below. Note that all the json files
unless otherwise specified will be placed in the folder ``config`` in the main project
folder.

Specifications for the database:
--------------------------------

sarah.test4

Specifications for ``modules.json``
-----------------------------------

Make sure that the ``execute`` statement within the modules file is set to True. 

.. code-block:: python
    :emphasize-lines: 3

    "moduleName" : "table2",
    "path"       : "modules/table2/table2.py",
    "execute"    : true,
    "description": "",
    "owner"      : ""


Specification for ``table2.json``
-----------------------------------

Ensure that the DSM number str values for each mental disorder are specified under 
["params"]["sudcats"]. 

'''