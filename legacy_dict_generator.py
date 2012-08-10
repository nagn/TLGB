#!/usr/bin/env python
import xml.etree.ElementTree as xml
import json
#This is hacky, but hopefully this will only need to be used once
def getValues(tree):
    return [thing for thing in tree]
tree = xml.parse("_FromGarrisonBuilder/Sprites/Entities/_resources.list.xml")
wat = list(tree.iter())
resourceList = []
for element in wat:
    if element.get('name') !=  None:
        #slice out the "_ent"
        resourceList.append(element.get('name')[:-4])
resourceDict = {}
for entityName in resourceList:
    resourceDict[entityName] = "sprites/legacy/entities/%s" %entityName

legacyEntityDict = open("legacy_dict.json", "w")
legacyEntityDict.write(json.dumps(resourceDict, sort_keys=True, indent=4))
legacyEntityDict.close()

legacyEntityList = open("legacy_list.json", "w")
legacyEntityList.write(json.dumps(resourceList,indent=4))
legacyEntityList.close()