# Autonomous Vehicle

ROS 2 workspace for the autonomous mobile robot.

## Packages

- `buggy_description` — Robot URDF/Xacro
- `encoder_odometry` — Encoder-based odometry
- `robot_bringup` — Main bringup launch
- `sllidar_ros2` — SLLIDAR driver
- `ydlidar_ros2_driver` — YDLIDAR driver

## Setup

```bash
git clone https://github.com/arushiy1300/Autonomous_Vehicle.git
cd Autonomous_Vehicle
source /opt/ros/<ros2_distro>/setup.bash
colcon build
source install/setup.bash
```

## Run

```bash
ros2 launch robot_bringup bringup.launch.py
```

## TF

```text
map → odom → base_link → laser
```

## SLAM

SLAM Toolbox is configured using:

```text
slam_config/mapper_params_online_async.yaml
```
