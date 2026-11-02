# Autonomous Mobile Robot — ROS 2 Humble

ROS 2 Humble implementation of the Autonomous Mobile Robot project, developed and tested on a Raspberry Pi 4b.

## Environment

- Hardware: Raspberry Pi 4b
- Operating System: Ubuntu 22.04
- ROS 2 Distribution: Humble
- LiDAR: Slamtec SLLIDAR A2M12
- Drive system: Differential drive
- Odometry: Wheel encoder-based
- Mapping: SLAM Toolbox

## Repository Structure

```text
Autonomous_Mobile_Robot_Humble/
├── src/
│   ├── buggy_description/
│   ├── encoder_odometry/
│   ├── robot_bringup/
│   ├── sllidar_ros2/
│   └── ydlidar_ros2_driver/
├── scripts/
│   └── motor_serial.py
├── slam_config/
│   └── mapper_params_online_async.yaml
└── README.md



 

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/arushiy1300/Autonomous_Vehicle.git
cd Autonomous_Vehicle/Autonomous_Mobile_Robot_Humble
```

### 2. Source ROS 2 Humble

```bash
source /opt/ros/humble/setup.bash
```

### 3. Install dependencies

```bash
rosdep install --from-paths src --ignore-src -r -y
```

### 4. Build the workspace

```bash
colcon build
```

### 5. Source the workspace

```bash
source install/setup.bash
```

## Robot Bringup

Launch the autonomous mobile robot system:

```bash
ros2 launch robot_bringup bringup.launch.py
```

The bringup launch file starts:

- Motor serial communication
- Encoder-based odometry
- SLLIDAR A2M12 driver
- Static transform publisher
- SLAM Toolbox

## Coordinate Frames

```text
map
 └── odom
      └── base_link
           └── laser
```

## Mapping

The project uses SLAM Toolbox in online asynchronous mode.

Configuration file:

```text
slam_config/mapper_params_online_async.yaml
```

Save a generated occupancy grid:

```bash
ros2 run nav2_map_server map_saver_cli -f ~/ros2_ws/maps/c205a
```

This generates:

- `c205a.yaml`
- `c205a.pgm`

## Related Implementation

The ROS 2 Jazzy implementation is maintained separately in the root of this repository.

---

**Autonomous Mobile Robot Project**  
ROS 2 Humble | Raspberry Pi 5
