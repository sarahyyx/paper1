'''Performs logistic regression for any sud against comorbid mental disorders.

This module performs logistic regression for any sud and other comorbid mental disorder 
diagnoses, for users from each race, then returns the odds ratios and confidence 
intervals for each subgroup.

Before you Begin
================

Make sure that the configuration files are properly set, as mentioned in the Specifcations 
section. 

Make sure you have the csv file: DSM Numbers. Convert each sheet in the file into json format 
by using an online csv -> json converter, then copying the json file into the table1.json config
file under ["params"]["categories"].

Also, set the minimum percentage of the sample that has to have the mental disorder 
for logistic regression to be performed, under ["params"]["min_percentage_of_diag"].

Details of Operation
====================

Firstly, the function createDF_byRace_anySUD() from queryDB creates a dataframe which
will be passed into the utils.logRegress() function to be fitted into the logistic 
regression model. Mental disorders that do not have a sufficient number of users are 
dropped before passing into the logRegress() function. 

After passing into the logRegress() function, the odds ratios and confidence intervals 
for each subgroup is returned.

Results
=======

Files created:
../data/final/table4data.json

Specifications:
===============

Specifications for running the module is described below. Note that all the json files
unless otherwise specified will be placed in the folder ``config`` in the main project
folder.

Specifications for ``modules.json``
-----------------------------------

Make sure that the ``execute`` statement within the modules file is set to True. 

.. code-block:: python
    :emphasize-lines: 3

    "moduleName" : "table4",
    "path"       : "modules/table4/table4.py",
    "execute"    : true,
    "description": "",
    "owner"      : ""


Specification for ``table4.json``
-----------------------------------

Ensure that the DSM numbers for each mental disorder are specified under 
["params"]["categories"], and the minimum sample percentage is set under 
["params"]["min_percentage_of_diag"]. 

'''