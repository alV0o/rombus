from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python import get_package_share_directory
import yaml
import os

def generate_launch_description():

    sim_dir = get_package_share_directory('main_simulation')
    mock_path = os.path.join(sim_dir, 'config', 'mocks.yaml')

    with open(mock_path, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)

    pickup_names = data['pickup']
    
    dropoff_names = data['dropoff']

    launch_actions = []

    for name in pickup_names:
        node = Node(
            package='main_simulation',
            executable='arm_mock_dispenser',
            name=name,
            output='screen',
            parameters=[{
                'rmf_dispenser_name': name
            }]
        )

        launch_actions.append(node)
    
    for name in dropoff_names:
        node = Node(
            package='main_simulation',
            executable='arm_mock_ingestor',
            name=name,
            output='screen',
            parameters=[{
                'rmf_ingestor_name': name
            }]
        )
        
        launch_actions.append(node)
    
    return LaunchDescription(launch_actions)
        
