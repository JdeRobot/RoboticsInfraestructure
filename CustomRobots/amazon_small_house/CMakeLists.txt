cmake_minimum_required(VERSION 3.5)
project(aws_robomaker_small_house_world)

find_package(ros_gz_sim REQUIRED)
find_package(ros_gz_image REQUIRED)
find_package(ros_gz_bridge REQUIRED)
find_package(ament_cmake_ros REQUIRED)

install(DIRECTORY launch models worlds maps photos param routes
    DESTINATION share/${PROJECT_NAME}
)

ament_export_dependencies(ros_gz_sim)
ament_export_dependencies(ros_gz_image)
ament_export_dependencies(ros_gz_bridge)

ament_package()