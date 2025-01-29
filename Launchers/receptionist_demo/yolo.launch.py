import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import SetRemap


def generate_launch_description():
    darknet_ros_dir = get_package_share_directory("darknet_ros")

    # Actions
    yolo_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(darknet_ros_dir, "launch", "darknet_ros.launch.py")
        ),
    )

    ld = LaunchDescription()
    ld.add_action(yolo_cmd)

    return ld
