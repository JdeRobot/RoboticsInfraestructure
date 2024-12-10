import os
import time
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition, UnlessCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration, PythonExpression
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():

    # Set the path to the Nav2 package
    pkg_nav2_ros = FindPackageShare(package="nav2_bringup").find("nav2_bringup")

    # Set the path to this package.
    pkg_share = FindPackageShare(package="custom_robots").find("custom_robots")

    # Set the path to the SDF model files.
    gazebo_models_path = os.path.join(pkg_share, "models")
    os.environ["GAZEBO_MODEL_PATH"] = (
        f"{os.environ.get('GAZEBO_MODEL_PATH', '')}:{':'.join(gazebo_models_path)}"
    )

    # Launch configuration variables specific to simulation
    use_sim_time = LaunchConfiguration("use_sim_time")
    slam = LaunchConfiguration("slam")
    map_file = LaunchConfiguration("map")
    params_file = LaunchConfiguration("params_file")

    # Specify the actions

    localization_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_nav2_ros, 'launch', 'localization_launch.py')
        ),
        launch_arguments={
            'use_sim_time': use_sim_time,
            'map': map_file,
            'slam': slam,
            'params_file': params_file
        }.items()
    )

    navigation_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_nav2_ros, 'launch', 'navigation_launch.py')
        ),
        launch_arguments={
            'use_sim_time': use_sim_time,
            'params_file': params_file
        }.items()
    )

    time.sleep(5)

    # Create the launch description and populate
    ld = LaunchDescription()

    ld.add_action(localization_cmd)
    ld.add_action(navigation_cmd)

    return ld
