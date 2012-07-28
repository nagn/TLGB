from __future__ import print_function, division
"""
here the default configuration of everything is stored
"""
def return_entity_types():
    entity_dict = {
        'categories' :[
        {
            'name' : 'Control Points',
            'types' : [
                controlpoint_1,
                controlpoint_2,
                controlpoint_3,
                controlpoint_4,
                controlpoint_5,
            ]
        },
        {
            'name' : 'Spawn points',
            'types' : [
                spawn_red,
                spawn_blue,
            ]
            
        },
        {
            'name' : 'Intelligence',
            'types' : [
                intel_red,
                intel_blue,
            ]
        },
        {
            'name' : 'Kill Boxes',
            'types' : [
                box_frag,
                box_kill,
                box_pitfall,
            ]
        },
        {
            'name' : 'Walls',
            'types' : [
                wall_player,
                wall_red,
                wall_blue,
                wall_bullet,
            ]
        },
        {
            'name' : 'Floors',
            'types' : [
                floor_player,
                floor_red,
                floor_blue,
                floor_bullet,
            ]
        },
        {
            'name' : 'Arena Control Point',
            'types' : [
                controlpoint_arena,
            ]
        },
        
        ]
    }
    return (entity_dict)
controlpoint_1 = {
    'name': 'controlpoint_1',
    'humanReadableName': 'Control Point 1',
    'id': 'controlpoint_1', 
    'mapImage': 'sprites/entities/controlpoint_1.png',
    'gbImage' : 'icons/entities/controlpoint_1.png',
    'mapImageOrigin': { 'x': 0, 'y': 0 }, 
}
controlpoint_2 = {
    'name': 'controlpoint_2',
    'id': 'controlpoint_2',
    'mapImage': 'sprites/entities/controlpoint_2.png',
    'gbImage' : 'icons/entities/controlpoint_2.png',
    'humanReadableName' : 'Control Point 2',
    'mapImageOrigin': {'x' : 0, 'y' : 0},
    }
controlpoint_3 = {
    'name': 'controlpoint_3',
    'id': 'controlpoint_3',
    'mapImage': 'sprites/entities/controlpoint_3.png',
    'gbImage' : 'icons/entities/controlpoint_3.png',
    'humanReadableName' : 'Control Point 3',
    'mapImageOrigin': {'x' : 0, 'y' : 0},
    }
controlpoint_4 = {
    'name': 'controlpoint_4',
    'id': 'controlpoint_4',
    'mapImage': 'sprites/entities/controlpoint_4.png',
    'gbImage' : 'icons/entities/controlpoint_4.png',
    'humanReadableName' : 'Control Point 4',
    'mapImageOrigin': {'x' : 0, 'y' : 0},
    }
controlpoint_5 = {
    'name': 'controlpoint_5',
    'id': 'controlpoint_4',
    'mapImage': 'sprites/entities/controlpoint_5.png',
    'gbImage' : 'icons/entities/controlpoint_5.png',
    'humanReadableName' : 'Control Point 5',
    'mapImageOrigin': {'x' : 0, 'y' : 0},
    }
controlpoint_arena = {
    'name': 'controlpoint_arena',
    'humanReadableName' : 'Arena Control Point',
    'id': 'controlpoint_arena',
    'mapImage': 'sprites/entities/controlpoint_arena.png',
    'gbImage' : 'icons/entities/controlpoint_arena.png',
    'mapImageOrigin': {'x' : 0, 'y' : 0},
    }
spawn_red = {
    'name': 'spawn_point_red',
    'humanReadableName' : 'Red Spawn',
    'id': 'spawn_red',
    'mapImage': 'sprites/entities/spawn_point_red.png',
    'gbImage' : 'icons/entities/spawn_point_red.png',
    'mapImageOrigin': {'x' : 29, 'y' : 40},
    }
spawn_blue = {
    'name': 'spawn_point_blue',
    'humanReadableName' : 'Blue Spawn',
    'id': 'spawn_blue',
    'mapImage': 'sprites/entities/spawn_point_blue.png',
    'gbImage' : 'icons/entities/spawn_point_blue.png',
    'mapImageOrigin': {'x' : 29, 'y' : 40},
    }
intel_red = {
    'name': 'intel red',
    'humanReadableName' : 'Red Intel',
    'id': 'intel_red',
    'mapImage': 'sprites/entities/intel_red.png',
    'gbImage' : 'icons/entities/intel_red.png',
    'mapImageOrigin': {'x' : 0, 'y' : 0},
    }
intel_blue = {
    'name': 'intel blue',
    'humanReadableName' : 'Blue Intel',
    'id': 'intel_blue',
    'mapImage': 'sprites/entities/intel_blue.png',
    'gbImage' : 'icons/entities/intel_blue.png',
    'mapImageOrigin': {'x' : 0, 'y' : 0},
    }
box_frag = {
    'name': 'frag box',
    'humanReadableName' : 'Frag Box',
    'id': 'box_frag',
    'mapImage': 'sprites/entities/box_frag.png',
    'gbImage' : 'icons/entities/box_frag.png',
    'mapImageOrigin': {'x' : 0, 'y' : 0},
    }
box_pitfall = {
    'name': 'pitfall box',
    'humanReadableName' : 'Pitfall Box',
    'id': 'box_pitfall',
    'mapImage': 'sprites/entities/box_pitfall.png',
    'gbImage' : 'icons/entities/box_pitfall.png',
    'mapImageOrigin': {'x' : 0, 'y' : 0},
    }
box_kill = {
    'name': 'kill box',
    'humanReadableName' : 'Kill Box',
    'id': 'box_kill',
    'mapImage': 'sprites/entities/box_kill.png',
    'gbImage' : 'icons/entities/box_kill.png',
    'mapImageOrigin': {'x' : 0, 'y' : 0},
    }
floor_player = {
    'name': 'player floor',
    'humanReadableName' : 'Player Floor (Blocks Players)',
    'id': 'floor_player',
    'mapImage': 'sprites/entities/floor_player.png',
    'gbImage' : 'icons/entities/floor_player.png',
    'mapImageOrigin': {'x' : 0, 'y' : 0},
    }
floor_bullet = {
    'name': 'bullet floor',
    'humanReadableName' : 'Bullet Floor (Blocks Bullets)',
    'id': 'floor_bullet',
    'mapImage': 'sprites/entities/floor_bullet.png',
    'gbImage' : 'icons/entities/floor_bullet.png',
    'mapImageOrigin': {'x' : 0, 'y' : 0},
    }
floor_red = {
    'name': 'red team floor',
    'humanReadableName' : 'Red Team Floor',
    'id': 'floor_red',
    'mapImage': 'sprites/entities/floor_red.png',
    'gbImage' : 'icons/entities/floor_red.png',
    'mapImageOrigin': {'x' : 0, 'y' : 0},
}
floor_blue = {
    'name': 'blue team floor',
    'humanReadableName' : 'Blue Team Floor',
    'id': 'floor_blue',
    'mapImage': 'sprites/entities/floor_blue.png',
    'gbImage' : 'icons/entities/floor_blue.png',
    'mapImageOrigin': {'x' : 0, 'y' : 0},
}

wall_player = {
    'name': 'player wall',
    'humanReadableName' : 'Player Wall (Blocks Players)',
    'id': 'wall_player',
    'mapImage': 'sprites/entities/wall_player.png',
    'gbImage' : 'icons/entities/wall_player.png',
    'mapImageOrigin': {'x' : 0, 'y' : 0},
    }
wall_bullet = {
    'name': 'bullet wall',
    'humanReadableName' : 'Bullet Wall (Blocks Bullets)',
    'id': 'wall_bullet',
    'mapImage': 'sprites/entities/wall_bullet.png',
    'gbImage' : 'icons/entities/wall_bullet.png',
    'mapImageOrigin': {'x' : 0, 'y' : 0},
    }
wall_red = {
    'name': 'red team wall',
    'humanReadableName' : 'Red Team Wall',
    'id': 'wall_red',
    'mapImage': 'sprites/entities/wall_red.png',
    'gbImage' : 'icons/entities/wall_red.png',
    'mapImageOrigin': {'x' : 0, 'y' : 0},
}

wall_blue = {
    'name': 'blue team wall',
    'humanReadableName' : 'Blue Team Wall',
    'id': 'wall_blue',
    'mapImage': 'sprites/entities/wall_blue.png',
    'gbImage' : 'icons/entities/wall_blue.png',
    'mapImageOrigin': {'x' : 0, 'y' : 0},
}
