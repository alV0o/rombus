import os
from ament_index_python.packages import get_package_share_directory
from pathlib import Path
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedSeq
import copy

main_dir = get_package_share_directory("free_fleet_examples")
sim_dir = get_package_share_directory("main_simulation")
maps_dir = get_package_share_directory('test_building_maps')

robots_structure = {}

default_config={
    "charger": None,
    "finishing_request":{},
    "responsive_wait": False,
    "navigation_stack": 2,
    "init_timeout_sec": 5,
    "initial_map": None,
    "maps": [],
    "initial_pose": []
}

initial_map_name = 'L1'
default_coords_config={
    initial_map_name: {
        "rmf":[],
        "robot":[]
    }
}

def override_config(template_path,config_path):
    yaml = YAML()
    yaml.width = 4096  

    with open(template_path, 'r') as file:
        data = yaml.load(file)

    data['rmf_fleet']["robots"] = robots_structure
    
    data['reference_coordinates'] = default_coords_config

    with open(config_path, 'w') as file:
        yaml.dump(data, file)



def fill_robots(map_name):
    path_to_robots_cfg = os.path.join(sim_dir, 'config', f'{map_name}_robot_config.yaml')

    yaml = YAML()

    with open(path_to_robots_cfg, 'r') as file:
        data = yaml.load(file)

    types = []
    for robot in data['robots']:
        if robot['type'] not in types:
            types.append(robot['type'])

    for target_type in types:

        template_path = os.path.join(main_dir, 'config', 'template', f'{target_type}_fleet_config.template.yaml')
        config_path = os.path.join(main_dir, 'config', 'fleet', f'{target_type}_fleet_config.yaml')

        fill_coords(map_name)

        for robot in data['robots']:
            
            if robot['type'] != target_type:
                continue

            robot_name = robot['name']
            x = robot['x_pose']
            y = robot['y_pose']
            theta = robot['yaw']

            robots_structure[robot_name] = default_config.copy()
            robots_structure[robot_name]['charger'] = robot['charger']
            pose = CommentedSeq([x, y, theta])
            pose.fa.set_flow_style()
            robots_structure[robot_name]['initial_pose'] = pose
            robots_structure[robot_name]['initial_map'] = robot['initial_map']
            robots_structure[robot_name]['maps'] = {robot['initial_map']:None}
            robots_structure[robot_name]['finishing_request'] = {
                "type":robot['stay_type'],
                "waypoint_name":robot['stay_waypoint'],
            }
            robots_structure[robot_name]['maps'][robot['initial_map']] = {
            "map_url": os.path.join(maps_dir, 'configs', f"{map_name}_config.yaml"),
            }
        
        override_config(template_path, config_path)
        robots_structure.clear()

def fill_coords(map_name): 
    path_to_coords = os.path.join(sim_dir, 'coords', f'{map_name}_coords.yaml')

    yaml = YAML()

    with open(path_to_coords, 'r') as file:
        data = yaml.load(file)
    
    coords = data.get('coords', [])

    default_coords_config[initial_map_name]["rmf"] = copy.deepcopy(coords)
    default_coords_config[initial_map_name]["robot"] = copy.deepcopy(coords)




    
def main():
    map_name = input("Input map name: ")
    fill_robots(map_name)
    print(f'new map - {map_name}')

if __name__ == "__main__":
    main()