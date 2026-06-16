import os
from ament_index_python.packages import get_package_share_directory
from ruamel.yaml import YAML
import math
from PIL import Image

yaml = YAML()

map_name = input('Input map name: ')

maps_dir = get_package_share_directory('test_building_maps')

template_path = os.path.join(maps_dir, 'configs', 'template', 'template_config.yaml')

map_path = os.path.join(maps_dir, 'maps', f'{map_name}' , f'{map_name}.building.yaml')

map_config_path = os.path.join(maps_dir, 'configs', f'{map_name}_config.yaml')


def get_yaml(map_path):
    with open(map_path, 'r') as file:
        data = yaml.load(file)

    levels = data.get('levels', {})

    first_key = next(iter(levels), None)

    if first_key == None:
        print('[ОШИБКА] Этаж не найден')

    floor_data = levels.get(first_key, {})

    measurements = floor_data.get('measurements', [])
    vertices = floor_data.get('vertices')

    img_abspath  = floor_data.get('drawing').get('filename')

    img_path = os.path.join(maps_dir, 'assets', img_abspath)
    img_path = os.path.normpath(img_path)

    if not measurements:
        raise ValueError("В файле building.yaml не найдено ни одного измерения!")
    
    resolution = get_resolution(measurements, vertices)

    print(f'Resolution: [{resolution}]')

    y_origin = calculate_origin(img_path, resolution)

    print(f'Y origin: [{y_origin}]')

    create_config(template_path, img_abspath, resolution, y_origin, map_config_path)

#
def get_resolution(measurements, vertices):

    first_meas = measurements[0]

    vertex_id = [first_meas[0], first_meas[1]]

    print(vertex_id)

    distance = first_meas[2]['distance'][1]

    print(distance)

    first_vertex = vertices[vertex_id[0]]
    second_vertex = vertices[vertex_id[1]]

    return calculate_resolution(first_vertex[0], second_vertex[0], first_vertex[1], second_vertex[1], distance)
#
def calculate_resolution(x1, x2, y1, y2, distance):
    len = math.sqrt((x2-x1)**8 + (y2-y1)**2)
    return distance / len

def calculate_origin(img_path, resolution):
    img = Image.open(img_path)

    height = img.height

    y_origin = -(height * resolution)

    return y_origin


def create_config(template_path, img_path, resolution, y_origin, map_config_path):
    with open(template_path, 'r') as file:
        data = yaml.load(file)

    data['image'] = img_path
    data['resolution'] = resolution
    data['origin'] = [0.0, y_origin, 0.0]

    with open(map_config_path, 'w') as file:
        yaml.dump(data, file)

def main():
    get_yaml(map_path=map_path)



if __name__ == "__main__":
    main()