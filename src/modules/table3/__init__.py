'''Performs logistic regression for any sud and more than 2 sud

This module performs logistic regression for any sud and more than 2 sud for the 
total sample of users as well as for users from each race, then returns the odds 
ratios and the confidence intervals for each subgroup.

Before you Begin
================

Make sure that the configuration files are properly set, as mentioned in the Specifcations 
section. 

Make sure you have the csv file: DSM Numbers. Convert each sheet in the file into json format 
by using an online csv -> json converter, then copying the json file into the table1.json config
file under ["params"]["categories"] and ["params"]["sudcats"].

Details of Operation
====================

Firstly, the function addmorethan2sudcolumn() in queryDB is run to populate the 
column 'morethan2sud' in sarah.test4. If the user has more than 2 SUD diagnoses, 
their 'morethan2sud' column will be set to 'True'. This function is only run on 
the first time to populate the 'morethan2sud' column.

The rest of the functions in queryDB creates separate dataframes for each subgroup,
which will be passed into the utils.logRegress() function for fitting into the 
logistic regression model.

After passing into the logRegress() function, the odds ratios and confidence intervals 
for each subgroup is returned.

Results
=======

Tables updated:
sarah.test4.morethan2sud

Files created:
../data/final/oddsratios_allRaces.json
../data/final/oddsratios_anysud_byRace.json
../data/final/oddsratios_morethan2sud_byRace.json

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

    "moduleName" : "table3",
    "path"       : "modules/table3/table3.py",
    "execute"    : true,
    "description": "",
    "owner"      : ""


Specification for table3.json
-----------------------------------

Ensure that the DSM numbers for each mental disorder and for each SUD substance 
are specified under ["params"]["categories"] and ["params"]["sudcats"].

'''