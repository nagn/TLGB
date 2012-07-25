from __future__ import print_function, division
import os, sys
import json
import entities

class JsonHandler(object):
    def __init__(self):
        self.entityList = []
        
        self.generate_all_entities()
        self.save_all_entities()
        #self.save_entities()
    def load_entities(self):
        if os.path.exists('entity_types.json'):
            with open('entity_types.json', 'r') as entity_dict:
                self.exampleObject = json.load(entity_dict)
        else:
            self.exampleObject = {}

    def generate_all_entities(self):
        self.exampleObject = {
            'categories' :[
            {
                'name' : 'Control Points',
                'types' : [
                        entities.controlpoint_1,
                        entities.controlpoint_2,
                ]
            },
            {
                'name' : 'Spawn points',
                'types' : [
                    entities.spawn_red,
                    entities.spawn_blue,
                ]
                
            },
            ]
        }
        for categoryIteration in range(len(self.exampleObject['categories'])):
            category = str(self.exampleObject['categories'][categoryIteration]['name'])
            for entityType in self.exampleObject['categories'][categoryIteration]['types']:
                newEntity = Entity()
                #Copy over the dict to the object
                newEntity.attributes = entityType.copy()
                newEntity.category = category
                self.entityList.append(newEntity)
                
        for entity in self.entityList:
            print(entity.category + ": " + str(entity.attributes['humanReadableName']))
            
    def save_all_entities(self):
        with open('entity_types.json', 'w') as entity_dict:
            json.dump(self.exampleObject, entity_dict, indent=4)
class Entity (object):
    def __init__(self):
        pass