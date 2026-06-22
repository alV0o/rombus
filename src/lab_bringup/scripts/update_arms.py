import os
import yaml
from mes_rmf_adapter import utils
from ament_index_python import get_package_share_directory

def main(map_name):
    maps_pkg_name = 'test_building_maps'
    maps_dir = get_package_share_directory(maps_pkg_name)
    points = utils.get_points(map_name, maps_dir, maps_pkg_name)

    dropoff = []
    pickup = []
    for point in points.values():
        if point.get('dropoff_ingestor'):
            dropoff.append(point.get('dropoff_ingestor'))
        if point.get('pickup_dispenser'):
            pickup.append(point.get('pickup_dispenser'))
    
    sim_dir = get_package_share_directory('main_simulation')
    yaml_path = os.path.join(sim_dir, 'config', 'mocks.yaml')

    config_data = {
        'dropoff': dropoff,
        'pickup':pickup
    }
    with open(yaml_path, 'w', encoding='utf-8') as file:
        yaml.dump(config_data, file, default_flow_style=False, sort_keys=False)

if __name__ == '__main__':
    map_name = input('Input map name: ')
    main(map_name)



