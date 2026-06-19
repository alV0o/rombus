import os
import yaml


class MapPackageNotFoundError(Exception):
    """Вызывается, если не найден сам пакет с картами."""
    pass

class MapFileNotFoundError(Exception):
    """Вызывается, если файл конкретной карты отсутствует."""
    pass

def get_points(map_name, maps_dir, maps_pkg_name):
    if maps_dir == None:
        raise MapPackageNotFoundError(f"Пакет [{maps_pkg_name}] не найден")

    yaml_path = os.path.join(maps_dir, 'maps', map_name, f'{map_name}.building.yaml')

    if not os.path.exists(yaml_path):
        raise MapFileNotFoundError(f"Карта [{map_name}] не найдена")

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

    return post_data