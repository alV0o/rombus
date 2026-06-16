import os
from ament_index_python.packages import get_package_share_directory
from pathlib import Path
from ruamel.yaml import YAML

yaml = YAML()

maps_dir = get_package_share_directory('main_simulation')



def add_robot():
    
    robot = {}

    robot['name'] = input('Введите имя робота: ')
    robot['x_pose'] = float(input('Введите координату X для робота: '))
    robot['y_pose'] = float(input('Введите координату Y для робота: '))
    robot['z_pose'] = 0.1
    robot['roll'] = 0.0
    robot['pitch']= 0.0
    robot['yaw'] = float(input('Введите угол поворота (yaw): '))
    robot['initial_map'] = "L1"
    robot['charger'] = input('Введите название зарядной станции: ')
    robot['type'] =  input('Введите тип робота: ')
    robot['stay_waypoint'] = input('Введите зону простоя: ')
    robot['stay_type'] = input('Введите тип простоя (park, change, nothing): ')

    return robot

def write_yaml(robot_config_path, robot):
    
    data = None

    try:
        with open(robot_config_path, 'r') as file:
            data = yaml.load(file)
    except:
        data = {'robots':[]}
    
    if data is None:
        data = {'robots':[]}
    
    data['robots'].append(robot)

    with open(robot_config_path, 'w') as file:
        yaml.dump(data, file)




def main():

    map_name = input('Введите название карты для нового робота: ')

    print('---')

    robot = add_robot()

    print('---')

    robot_config_path = os.path.join(maps_dir, 'config', f'{map_name}_robot_config.yaml')

    write_yaml(robot_config_path, robot)
    
    print('Робот добавлен')

if __name__ == "__main__":
    main()