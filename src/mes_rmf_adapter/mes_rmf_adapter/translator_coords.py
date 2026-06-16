import yaml
import os
from pathlib import Path
from ament_index_python.packages import get_package_share_directory


map_name = input('Input map name: ')
maps_dir = get_package_share_directory('test_building_maps')

yaml_path = os.path.join(maps_dir, 'maps', map_name, f'{map_name}.building.yaml')

with open(yaml_path, 'r', encoding='utf-8') as f:
    data = yaml.safe_load(f)

vertices = data['levels']['L1']['vertices']

post_data = {}

for vertex in vertices:
    if vertex[3] == "":
        continue

    name = vertex[3]

    if len(vertex) > 4 and isinstance(vertex[4], dict):
        
        params = vertex[4]
        
        vertex_data = {}

        if 'pickup_dispenser' in params:
            vertex_data['pickup_dispenser'] = params['pickup_dispenser'][1]
        if 'dropoff_ingestor' in params:
            vertex_data['dropoff_ingestor'] = params['dropoff_ingestor'][1]
    
        if vertex_data:
            post_data[name] = vertex_data

print(post_data)


