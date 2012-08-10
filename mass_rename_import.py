#!/usr/bin/env python
"""WARNING ONLY USE THIS FILE WHEN COPYING AND PASTING FROM THE GMKSPLITTED GARRISON BUILDER INT HE RESPECTIVE DIRECTORIES
OR ELSE MASS FILE DELETE"""
import os
import json
json_data=open("legacy_list.json").read()
entityList = json.loads(json_data)
json_data2=open("legacy_dict.json").read()
entityDict = json.loads(json_data2)

for entityName in entityList:
    os.rename(entityDict[entityName] + "_ent.images",entityDict[entityName])