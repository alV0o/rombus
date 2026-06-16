from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

    pickup_names = [
        'storage_pickup_arm_1',
        'pickup_arm_4',
        'pickup_arm_3',
        'pickup_arm_2',
        'pickup_arm_1',
        'pickup_arm_5'
    ]
    
    dropoff_names = [
        'storage_drop_arm_1',
        'drop_arm_1',
        'drop_arm_2',
        'drop_arm_3',
        'drop_arm_4',
        'drop_arm_5'
    ]

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
        
