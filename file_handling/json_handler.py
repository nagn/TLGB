from __future__ import print_function, division
import os, sys
import json
import config.default_types as default_types


def load_entities(entityTypePath):
    if os.path.exists(entityTypePath):
        with open(entityTypePath, 'r') as entity_dict:
            entityTypes = json.load(entity_dict)
    else:
        entityTypes = {}
    return(entityTypes)

def load_gamemode(entityTypePath):
    if os.path.exists(entityTypePath):
        with open(entityTypePath, 'r') as entity_dict:
            entities = json.load(entity_dict)
    else:
        print("unable to load gamemode")
        entities = []
    return(entities)

def generate_all_entities():
    entityList = []
    entityDict = default_types.return_entity_types()
    
    for categoryIteration in range(len(entityDict['categories'])):
        category = str(entityDict['categories'][categoryIteration]['name'])
        for entityType in entityDict['categories'][categoryIteration]['types']:
            newEntity = Entity()
            #Copy over the dict to the object
            newEntity.attributes = entityType.copy()
            newEntity.attributes['category'] = category
            entityList.append(newEntity)
    
    #Check to see if the icons exist
    for iterate, entity in enumerate(entityList):
        if not os.path.isfile(os.path.join(sys.path[0],entity.attributes['gbImage'])):
            print("path " + entity.attributes['gbImage'] + " does not exist for " + str (entity.attributes["id"]) + "!")
            entityList.pop(iterate)
    return (entityList)
def save_all_entities(entityTypePath, config):
    with open(entityTypePath, 'w') as entity_dict:
        json.dump(config, entity_dict, indent=4)
class Entity (object):
    def __init__(self):
        pass