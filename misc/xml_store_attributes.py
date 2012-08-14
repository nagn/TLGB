#!/usr/bin/env python
import os
import xml.etree.ElementTree as xml
import json
legacyDictFile = open("legacy_dict.json", 'w')
legacyListFile = open("legacy_list.json", 'r')
legacyDict = {}
legacyList = json.load(legacyListFile)
for entityName in legacyList:
    #note that we assume that all the origins are stored as entityName+_ent.xml
    parsedXML = xml.parse("_FromGarrisonBuilder\Sprites\Entities\%s.xml" % (str(entityName)+"_ent"))
    origin = parsedXML.find("origin").attrib
    legacyDict[str(entityName)] = {"filename" : str(os.path.join("sprites/legacy/entities/",str(entityName))),
                                   "mapImageOrigin" : origin
                                   }
json.dump(legacyDict, legacyDictFile, ensure_ascii = True, indent=4)
legacyDictFile.close()
legacyListFile.close()