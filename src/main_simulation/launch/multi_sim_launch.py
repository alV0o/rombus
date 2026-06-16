import os
from pathlib import Path
import tempfile
import yaml

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import (
    AppendEnvironmentVariable,
    DeclareLaunchArgument,
    ExecuteProcess,
    GroupAction,
    IncludeLaunchDescription,
    LogInfo,
    OpaqueFunction,
    RegisterEventHandler,
    TimerAction
)
from launch.conditions import IfCondition
from launch.event_handlers import OnShutdown
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, TextSubstitution
from nav2_common.launch import RewrittenYaml

def load_config(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)
    return config

def generate_launch_description():
    # Get the launch directory
    bringup_dir = get_package_share_directory('main_simulation')
    launch_dir = os.path.join(bringup_dir, 'launch')
    maps_dir = get_package_share_directory('test_building_maps') 
    
    map_name = input("Input map name: ")
    
    config_data = load_config(os.path.join(bringup_dir, 'config', f'{map_name}_robot_config.yaml'))
    models_path = os.path.join(maps_dir, 'maps', map_name)

    robots = config_data["robots"]

    # Simulation settings
    world = LaunchConfiguration('world')

    # On this example all robots are launched with the same settings
    map_yaml_file = LaunchConfiguration('map')

    autostart = LaunchConfiguration('autostart')
    rviz_config_file = LaunchConfiguration('rviz_config')
    use_robot_state_pub = LaunchConfiguration('use_robot_state_pub')
    use_rviz = LaunchConfiguration('use_rviz')
    log_settings = LaunchConfiguration('log_settings', default='true')

    # Declare the launch arguments
    declare_world_cmd = DeclareLaunchArgument(
        'world',
        default_value=os.path.join(maps_dir, 'worlds', f'{map_name}.world'),
        description='Full path to world file to load',
    )

    declare_map_yaml_cmd = DeclareLaunchArgument(
        'map',
        default_value=os.path.join(maps_dir, 'configs', f'{map_name}_config.yaml'),
        description='Full path to map file to load',
    )

    declare_autostart_cmd = DeclareLaunchArgument(
        'autostart',
        default_value='True',
        description='Automatically startup the stacks',
    )

    declare_rviz_config_file_cmd = DeclareLaunchArgument(
        'rviz_config',
        default_value=os.path.join(bringup_dir, 'rviz', 'nav2_namespaced_view.rviz'),
        description='Full path to the RVIZ config file to use.',
    )

    declare_use_robot_state_pub_cmd = DeclareLaunchArgument(
        'use_robot_state_pub',
        default_value='True',
        description='Whether to start the robot state publisher',
    )

    declare_use_rviz_cmd = DeclareLaunchArgument(
        'use_rviz', default_value='False', description='Whether to start RVIZ'
    )

    # Start Gazebo with plugin providing the robot spawning service
    world_sdf = tempfile.mktemp(prefix='nav2_', suffix='.sdf')
    world_sdf_xacro = ExecuteProcess(
        cmd=['xacro', '-o', world_sdf, ['headless:=', 'False'], world])
    start_gazebo_cmd = ExecuteProcess(
        cmd=['gz', 'sim', '-r', '-s', world_sdf],
        output='screen',
    )

    remove_temp_sdf_file = RegisterEventHandler(event_handler=OnShutdown(
        on_shutdown=[
            OpaqueFunction(function=lambda _: os.remove(world_sdf))
        ]))

    # Define commands for launching the navigation instances
    nav_instances_cmds = []
    for i, robot in enumerate(robots):

        if robot['type'] == 'fast_turtlebot3':
            params_file = os.path.join(bringup_dir, 'params', 'nav2_multirobot_params_fast.yaml')
        else:
            params_file = os.path.join(bringup_dir, 'params', 'nav2_multirobot_params_template.yaml')

        configured_params = RewrittenYaml(
            source_file=params_file,
            param_rewrites={
                'topic': f'/{robot["name"]}/scan',
                'amcl.ros__parameters.initial_pose.x': str(robot['x_pose']),
                'amcl.ros__parameters.initial_pose.y': str(robot['y_pose']),
                'amcl.ros__parameters.initial_pose.z': str(robot['z_pose']),
                'amcl.ros__parameters.initial_pose.yaw': str(robot['yaw'])
            },
            convert_types=True,
        )

        group = GroupAction(
            [
                IncludeLaunchDescription(
                    PythonLaunchDescriptionSource(
                        os.path.join(launch_dir, 'rviz_launch.py')
                    ),
                    condition=IfCondition(use_rviz),
                    launch_arguments={
                        'namespace': TextSubstitution(text=robot['name']),
                        'use_namespace': 'True',
                        'rviz_config': rviz_config_file,
                    }.items(),
                ),
                IncludeLaunchDescription(
                    PythonLaunchDescriptionSource(
                        os.path.join(bringup_dir, 'launch', 'tb3_simulation_launch.py')
                    ),
                    launch_arguments={
                        'namespace': robot['name'],
                        'use_namespace': 'True',
                        'map': map_yaml_file,
                        'use_sim_time': 'True',
                        'params_file': configured_params,
                        'autostart': autostart,
                        'use_rviz': 'False',
                        'use_simulator': 'False',
                        'headless': 'False',
                        'use_robot_state_pub': use_robot_state_pub,
                        'x_pose': TextSubstitution(text=str(robot['x_pose'])),
                        'y_pose': TextSubstitution(text=str(robot['y_pose'])),
                        'z_pose': TextSubstitution(text=str(robot['z_pose'])),
                        'roll': TextSubstitution(text=str(robot['roll'])),
                        'pitch': TextSubstitution(text=str(robot['pitch'])),
                        'yaw': TextSubstitution(text=str(robot['yaw'])),
                        'robot_name': TextSubstitution(text=robot['name']),
                    }.items(),
                ),
                LogInfo(
                    condition=IfCondition(log_settings),
                    msg=['Launching ', robot['name']],
                ),
                LogInfo(
                    condition=IfCondition(log_settings),
                    msg=[robot['name'], ' map yaml: ', map_yaml_file],
                ),
                LogInfo(
                    # condition=IfCondition(log_settings),
                    msg=[robot['name'], ' params yaml: ', params_file],
                ),
                LogInfo(
                    condition=IfCondition(log_settings),
                    msg=[robot['name'], ' rviz config file: ', rviz_config_file],
                ),
                LogInfo(
                    condition=IfCondition(log_settings),
                    msg=[
                        robot['name'],
                        ' using robot state pub: ',
                        use_robot_state_pub,
                    ],
                ),
                LogInfo(
                    condition=IfCondition(log_settings),
                    msg=[robot['name'], ' autostart: ', autostart],
                ),
            ]
        )

        # --- НАЧАЛО ИЗМЕНЕНИЙ ---
        # Вычисляем задержку: первый (0) стартует сразу, второй через 4 сек, третий через 8 сек и т.д.
        robot_delay = float(i * 4.0) 
        
        staggered_group = TimerAction(
            period=robot_delay,
            actions=[group]
        )
        
        # Вместо nav_instances_cmds.append(group) добавляем обертку с таймером:
        nav_instances_cmds.append(staggered_group)
        # --- КОНЕЦ ИЗМЕНЕНИЙ ---


    # Create the launch description and populate
    ld = LaunchDescription()

    ld.add_action(AppendEnvironmentVariable(
        name='GZ_SIM_RESOURCE_PATH',
        value=models_path
    ))

    # Declare the launch options
    ld.add_action(declare_world_cmd)
    ld.add_action(declare_map_yaml_cmd)
    ld.add_action(declare_use_rviz_cmd)
    ld.add_action(declare_autostart_cmd)
    ld.add_action(declare_rviz_config_file_cmd)
    ld.add_action(declare_use_robot_state_pub_cmd)

    # Add the actions to start gazebo, robots and simulations
    ld.add_action(world_sdf_xacro)
    ld.add_action(start_gazebo_cmd)
    ld.add_action(remove_temp_sdf_file)

    for simulation_instance_cmd in nav_instances_cmds:
        ld.add_action(simulation_instance_cmd)

    return ld
