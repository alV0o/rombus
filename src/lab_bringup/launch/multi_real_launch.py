import os
from pathlib import Path
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, ExecuteProcess, SetEnvironmentVariable, GroupAction
from launch.launch_description_sources import PythonLaunchDescriptionSource, AnyLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory, get_package_prefix

def generate_launch_description():
    
    rmw = SetEnvironmentVariable(name='RMW_IMPLEMENTATION', value='rmw_cyclonedds_cpp')

    rmf_mind_path = os.path.join(get_package_share_directory('free_fleet_examples'), 'turtlebot3_world_rmf_common.launch.xml')
    fleet_adapter_path = os.path.join(get_package_share_directory('free_fleet_examples'), 'nav2_unique_multi_tb3_simulation_fleet_adapter.launch.xml')
    mock_arms_path = os.path.join(get_package_share_directory('main_simulation'), 'launch', 'arms_launch.py')


    map_name_arg = DeclareLaunchArgument(name='map_name', default_value='new_map', description='Название карты для запуска')
    server_uri_arg = DeclareLaunchArgument(name='server_uri', default_value='ws://localhost:8000/_internal', description='Адрес ссылки для подключения')
    config_name_arg = DeclareLaunchArgument(name='config_name', default_value='turtlebot3_fleet_config.yaml', description='Название конфигурационного файла для адаптера')
    graph_name_arg = DeclareLaunchArgument(name='graph', default_value='0.yaml', description='Название карты путей')

    map_name_cfg = LaunchConfiguration('map_name')
    server_uri_cfg = LaunchConfiguration('server_uri')
    config_name_cfg = LaunchConfiguration('config_name')
    graph_name_cfg = LaunchConfiguration('graph')


    start_zenohd = ExecuteProcess(
        cmd=['zenohd'],
        output='screen'
    )

    start_zenohd_bridge = ExecuteProcess(
        cmd=[
            './zenoh-bridge-ros2dds',
            '-c', os.path.join(get_package_share_directory('free_fleet_examples'), 'config', 'zenoh', 'nav2_unique_multi_tb3_zenoh_bridge_ros2dds_client_config.json5')
        ],
        cwd='/home/alvo/test_ws/src',
        output = 'screen'
    )


    group = GroupAction([
        
        SetEnvironmentVariable(name='ROS_DOMAIN_ID', value='55'),
        SetEnvironmentVariable(name='RMW_IMPLEMENTATION', value='rmw_cyclonedds_cpp'),

        IncludeLaunchDescription(
            AnyLaunchDescriptionSource(
                rmf_mind_path
            ),
            launch_arguments={
                'map_name': map_name_cfg
            }.items()
        ),

        IncludeLaunchDescription(
            AnyLaunchDescriptionSource(
                fleet_adapter_path
            ),
            launch_arguments={
                'server_uri': server_uri_cfg,
                'map_name': map_name_cfg,
                'config_name': config_name_cfg,
                'graph': graph_name_cfg
            }.items()
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                mock_arms_path
            )
        )

    ])

    return LaunchDescription([
        rmw,
        map_name_arg,
        server_uri_arg,
        config_name_arg,
        graph_name_arg,
        #start_zenohd,
        start_zenohd_bridge,
        group
    ])