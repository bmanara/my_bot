import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node


def generate_launch_description():
    package_name = 'my_bot'

    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(
                get_package_share_directory(package_name),
                'launch',
                'rsp.launch.py'
            )
        ]),
        launch_arguments={'use_sim_time': 'true'}.items() 
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(
                get_package_share_directory('ros_gz_sim'),
                'launch',
                'gz_sim.launch.py'
            )
        ]),
        launch_arguments={'gz_args': 'empty.sdf'}.items()
    )

    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-world', 'empty', '-topic', '/robot_description', '-entity', 'my_bot'],
        output='screen'
    )

    return LaunchDescription([
        rsp,
        gazebo,
        spawn_entity
    ])
