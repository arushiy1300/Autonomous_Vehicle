from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from ament_index_python.packages import get_package_share_directory

import os


def generate_launch_description():

    slam_params = os.path.join(
        os.path.expanduser("~"),
        "arushi_ws",
        "slam_config",
        "mapper_params_online_async.yaml"
    )

    return LaunchDescription([

        # --------------------------
        # Motor Serial
        # --------------------------
        ExecuteProcess(
            cmd=[
                "python3",
                os.path.join(
                    os.path.expanduser("~"),
                    "arushi_ws",
                    "scripts",
                    "motor_serial.py"
                )
            ],
            output="screen"
        ),

        # --------------------------
        # Encoder Odometry
        # --------------------------
        Node(
            package="encoder_odometry",
            executable="odom_node",
            output="screen"
        ),

        # --------------------------
        # SLLIDAR
        # --------------------------
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(
                    get_package_share_directory("sllidar_ros2"),
                    "launch",
                    "sllidar_a2m12_launch.py"
                )
            )
        ),

        # --------------------------
        # Static TF
        # --------------------------
        Node(
            package="tf2_ros",
            executable="static_transform_publisher",
            arguments=[
                "0.12","0","0.18",
                "0","0","0",
                "base_link",
                "laser"
            ]
        ),

        # --------------------------
        # SLAM
        # --------------------------
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(
                    get_package_share_directory("slam_toolbox"),
                    "launch",
                    "online_async_launch.py"
                )
            ),
            launch_arguments={
                "slam_params_file": slam_params
            }.items()
        )

    ])
