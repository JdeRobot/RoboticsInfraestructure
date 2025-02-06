import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    SetEnvironmentVariable,
    AppendEnvironmentVariable
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():

    x = LaunchConfiguration('x')
    y = LaunchConfiguration('y')
    z = LaunchConfiguration('z')
    roll = LaunchConfiguration('R')
    pitch = LaunchConfiguration('P')
    yaw = LaunchConfiguration('Y')

    package_dir = get_package_share_directory('custom_robots')

    gazebo_models_path = os.path.join(package_dir, "models")

    robot_launch_dir = "/opt/jderobot/Launchers/robots/turtlebot3"
    robot_model_dir = os.path.join(package_dir, 'models/turtlebot3_waffle')
    
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    x_pose = LaunchConfiguration('x_pose', default='1.0')
    y_pose = LaunchConfiguration('y_pose', default='-1.5')
    z_pose = LaunchConfiguration('z_pose', default='0.6')

    declare_x_cmd = DeclareLaunchArgument(
        'x', default_value='1.0'
    )

    declare_y_cmd = DeclareLaunchArgument(
        'y', default_value='-1.5'
    )

    declare_z_cmd = DeclareLaunchArgument(
        'z', default_value='0.6'
    )

    declare_roll_cmd = DeclareLaunchArgument(
        'R', default_value='0.0'
    )

    declare_pitch_cmd = DeclareLaunchArgument(
        'P', default_value='0.0'
    )

    declare_yaw_cmd = DeclareLaunchArgument(
        'Y', default_value='1.57079'
    )

    robot_state_publisher_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(robot_launch_dir, 'robot_state_publisher.launch.py')
        ),
        launch_arguments={'use_sim_time': use_sim_time}.items()
    )

    spawn_robot_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(robot_launch_dir, 'spawn_robot.launch.py')
        ),
        launch_arguments={
            'x_pose': x_pose,
            'y_pose': y_pose,
            'z_pose': z_pose
        }.items()
    )

    ld = LaunchDescription()

    ld.add_action(SetEnvironmentVariable('GZ_SIM_RESOURCE_PATH', gazebo_models_path))
    set_env_vars_resources = AppendEnvironmentVariable('GZ_SIM_RESOURCE_PATH', os.path.join(package_dir,'models'))
    ld.add_action(set_env_vars_resources)
    ld.add_action(declare_x_cmd)
    ld.add_action(declare_y_cmd)
    ld.add_action(declare_z_cmd)
    ld.add_action(declare_roll_cmd)
    ld.add_action(declare_pitch_cmd)
    ld.add_action(declare_yaw_cmd)
    ld.add_action(robot_state_publisher_cmd)
    ld.add_action(spawn_robot_cmd)

    return ld
