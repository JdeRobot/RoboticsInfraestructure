# /*******************************************************************************
# * Copyright 2019 ROBOTIS CO., LTD.
# *
# * Licensed under the Apache License, Version 2.0 (the "License");
# * you may not use this file except in compliance with the License.
# * You may obtain a copy of the License at
# *
# *     http://www.apache.org/licenses/LICENSE-2.0
# *
# * Unless required by applicable law or agreed to in writing, software
# * distributed under the License is distributed on an "AS IS" BASIS,
# * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# * See the License for the specific language governing permissions and
# * limitations under the License.
# *******************************************************************************/

# /* Author: Darby Lim */

import os

import launch
from launch import LaunchDescription
from launch.actions import AppendEnvironmentVariable
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    
    package_dir = get_package_share_directory('aws_robomaker_small_house_world')
    ros_gz_sim = get_package_share_directory('ros_gz_sim')

    set_env_vars_resources = AppendEnvironmentVariable('GZ_SIM_RESOURCE_PATH', os.path.join(package_dir,'models'))
    world_file_name = 'small_house.world'

    world = os.path.join(
        get_package_share_directory('aws_robomaker_small_house_world'),
        'worlds',
        world_file_name
    )

    gazebo_client = IncludeLaunchDescription(
	PythonLaunchDescriptionSource(
            os.path.join(ros_gz_sim, 'launch', 'gz_sim.launch.py')),
        launch_arguments={'gz_args': '-g -v4 '}.items()
     )
    gazebo_server = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gz_sim, 'launch', 'gz_sim.launch.py')),
        launch_arguments={'gz_args': ['-r -s -v4 ', world], 'on_exit_shutdown': 'true'}.items()
    )


    ld = LaunchDescription()
    ld.add_action(set_env_vars_resources)
    ld.add_action(gazebo_server)
    ld.add_action(gazebo_client)


if __name__ == '__main__':
    generate_launch_description()
