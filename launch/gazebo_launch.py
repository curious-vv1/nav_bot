import os

from ament_index_python import get_package_share_directory

from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration, Command
from launch.actions import DeclareLaunchArgument,IncludeLaunchDescription
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():

    package_name = 'nav_bot'

    description = IncludeLaunchDescription(PythonLaunchDescriptionSource([os.path.join(get_package_share_directory(
        package_name), 'launch', 'description.launch.py')]), launch_arguments={'use_sim_time': 'true'}.items())

    gazebo_params_file = os.path.join(get_package_share_directory(
        package_name))

    gazebo = IncludeLaunchDescription(PythonLaunchDescriptionSource([os.path.join(
        get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]), launch_arguments={'extra_gazebo_args': '--ros-args --params-file ' + gazebo_params_file}.items())

    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py', arguments=[
        '-topic', 'robot_description', '-entity', 'robot'], output='screen')


    return LaunchDescription([
        description,
        gazebo,
        spawn_entity,
    ])