import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    SetEnvironmentVariable,
    AppendEnvironmentVariable,
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():

    x = LaunchConfiguration("x")
    y = LaunchConfiguration("y")
    z = LaunchConfiguration("z")
    roll = LaunchConfiguration("R")
    pitch = LaunchConfiguration("P")
    yaw = LaunchConfiguration("Y")

    package_dir = get_package_share_directory("custom_robots")

    gazebo_models_path = os.path.join(package_dir, "models")

    robot_launch_dir = "/opt/jderobot/Launchers/robots/turtlebot3"
    robot_model_dir = os.path.join(package_dir, "models/turtlebot3_waffle")

    use_sim_time = LaunchConfiguration("use_sim_time", default="true")

    declare_x_cmd = DeclareLaunchArgument("x", default_value="53.462")

    declare_y_cmd = DeclareLaunchArgument("y", default_value="-10.734")

    declare_z_cmd = DeclareLaunchArgument("z", default_value="0.004")

    declare_roll_cmd = DeclareLaunchArgument("R", default_value="0.0")

    declare_pitch_cmd = DeclareLaunchArgument("P", default_value="0.0")

    declare_yaw_cmd = DeclareLaunchArgument("Y", default_value="-1.57079")

    robot_state_publisher_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(robot_launch_dir, "robot_state_publisher.launch.py")
        ),
        launch_arguments={"use_sim_time": use_sim_time}.items(),
    )

    spawn_robot_cmd = Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        arguments=[
            "-topic",
            "robot_description",
            "-entity",
            "f1Renault",
            "-x", 53.462,
            "-y", -10.734,
            "-z", 0.004,
            "-R", 0.0,
            "-P", 0.0,
            "-Y", -1.57079,
        ],
        output="screen",
    )

    ld = LaunchDescription()

    ld.add_action(SetEnvironmentVariable("GZ_SIM_RESOURCE_PATH", gazebo_models_path))
    set_env_vars_resources = AppendEnvironmentVariable(
        "GZ_SIM_RESOURCE_PATH", os.path.join(package_dir, "models")
    )
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
