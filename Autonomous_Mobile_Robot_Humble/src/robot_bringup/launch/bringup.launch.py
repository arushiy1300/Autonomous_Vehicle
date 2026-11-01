import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
    project_dir = os.path.expanduser(
        "~/ros2_ws/src/Autonomous_Vehicle/Autonomous_Mobile_Robot_Humble"
    )

    slam_params = os.path.join(
        project_dir, "slam_config", "mapper_params_online_async.yaml"
    )
    motor_script = os.path.join(
        project_dir, "scripts", "motor_serial.py"
    )
    sllidar_launch = os.path.join(
        get_package_share_directory("sllidar_ros2"),
        "launch",
        "sllidar_a2m12_launch.py",
    )

    return LaunchDescription([
        ExecuteProcess(
            cmd=["python3", motor_script],
            output="screen",
        ),

        Node(
            package="encoder_odometry",
            executable="odom_node",
            output="screen",
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(sllidar_launch),
            launch_arguments={
                "serial_port": (
                    "/dev/serial/by-id/"
                    "usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_"
                    "4d129d87a554b14eabedef55218d5403-if00-port0"
                ),
                "serial_baudrate": "256000",
                "frame_id": "laser",
                "scan_mode": "Sensitivity",
            }.items(),
        ),

        Node(
            package="tf2_ros",
            executable="static_transform_publisher",
            arguments=[
                "0.12", "0", "0.18",
                "0", "0", "0",
                "base_link", "laser",
            ],
            output="screen",
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(
                    get_package_share_directory("slam_toolbox"),
                    "launch",
                    "online_async_launch.py",
                )
            ),
            launch_arguments={
                "slam_params_file": slam_params,
            }.items(),
        ),
    ])
