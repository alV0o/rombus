import os
from pathlib import Path
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    
    start_zenohd = ExecuteProcess(
        cmd=['zenohd'],
        output='screen'
    )

    start_zenohd_bridge = ExecuteProcess(
        cmd=[
            './zenoh-bridge-ros2dds',
            '-c', os.path.join(get_package_share_directory('free_fleet_adapter'), 'config', 'zenoh', 'nav2_unique_multi_tb3_zenoh_bridge_ros2dds_client_config.json5')
        ],
        cwd='/home/alvo/test_ws/src',
        output = 'screen'
    )

    start_simulation = IncludeLaunchDescription(
        
    )