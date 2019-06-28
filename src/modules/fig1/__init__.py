'''This module generates the data for Figure 1 and plots the bar charts.

This module finds the prevalence of each disorder among the races, as a percentage of the 
total number of people in that race. This data is then plotted on a bar chart and the figure is saved. 

Before you Begin
================

Make sure that the configuration files are properly set, as mentioned in the Specifcations 
section. 

Make sure you have the csv file: DSM Numbers. Convert each sheet in the file into json format 
by using an online csv -> json converter, then copying the json file into the table1.json config
file under ["params"]["categories"].

Details of Operation
====================

Firstly, the function genDiagCount() from fig1.queryDB is run to generate the percentage of 
each race that have a particular mental disorder diagnosis. The percentage counts for each 
mental disorder is saved to a dictionary 'countDict'. 

Next, the function removeLowPrev() will then remove those mental disorders that have a
prevalence that is lower than a user-specified percentage, which is found in:
fig1_config["params"]["min_prevalence"], returning a dict of the remaining disorders, 
which is then saved to a json file.

Results
=======

Files created:
../data/final/diagnosesCount.json

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

    "moduleName" : "fig1",
    "path"       : "modules/fig1/fig1.py",
    "execute"    : true,
    "description": "",
    "owner"      : ""


Specification for ``fig1.json``
-----------------------------------

Ensure that the str values for each race are specified under ["params"]["races"][race]. 
Do the same for sexes, settings and categories (DSM numbers).

'''