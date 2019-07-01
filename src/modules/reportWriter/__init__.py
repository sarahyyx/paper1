'''Writes the markdown report 

This module will write the different sections of the report according to the figures and 
tables of the paper. 

Before you Begin
================

Make sure that you have run the modules:

 - table1
 - fig1
 - table2
 - table3
 - table4

 and have the final data stored in ../data/final. The specific data files are as below.

Details of Operation
====================

``writeTable1.py``
Data sources that it uses 
-------------------------
 - ../data/final/sampleCount.json

Important operations
--------------------
 - genIntro()
 - genRace()
 - genRaceAge()
 - genRaceSex()
 - genRaceSetting()


``plotFig1.py``
Data sources that it uses 
-------------------------
 - ../data/final/diagnosesCount.json

Important operations
--------------------
 - genIntro()
 - genFig()


``writeTable2.py``
Data sources that it uses 
-------------------------
 - ../data/final/sampleCount.json
 - ../data/final/allAgesGeneralSUD.json
 - ../data/final/allAgesCategorisedSUD.json
 - ../data/final/ageBinnedGeneralSUD.json
 - ../data/final/ageBinnedCategorisedSUD.json

Important operations
--------------------
 - genIntro()
 - genTotalPrev()
 - genAAAgeBinnedPrev()
 - genNHPIAgeBinnedPrev()
 - genMRAgeBinnedPrev()


 ``writeTable3.py``
Data sources that it uses 
-------------------------
 - ../data/final/sampleCount.json
 - ../data/final/oddsratios_allRaces.json
 - ../data/final/oddsratios_anysud_byRace.json
 - ../data/final/oddsratios_morethan2sud_byRace.json

Important operations
--------------------
 - genIntro()
 - oddsRatiosAllRaces()
 - oddsRatiosByRace()


 ``writeTable4.py``
Data sources that it uses 
-------------------------
 - ../data/final/sampleCount.json
 - ../data/final/table4data.json

Important operations
--------------------
 - genIntro()
 - oddsRatiosByRace()

Results
=======

This module will create a Markdown report in the report folder, ../report/paper1Report.md

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

    "moduleName" : "reportWriter",
    "path"       : "modules/reportWriter/reportWriter.py",
    "execute"    : true,
    "description": "",
    "owner"      : ""

'''