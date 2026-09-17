#!/usr/bin/env python3

import threading
import serial

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from std_msgs.msg import Int64MultiArray


class MotorSerial(Node):

    def __init__(self):

        super().__init__('motor_serial')

        # ---------------------------------------
        # Open Serial Port
        # ---------------------------------------

        self.serial_port = serial.Serial(
            '/dev/ttyACM0',      # Change if Arduino appears on another port
            115200,
            timeout=0.05
        )

        self.get_logger().info("Connected to Arduino")

        # ---------------------------------------
        # ROS Subscriber
        # ---------------------------------------

        self.subscription = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_callback,
            10
        )

        # ---------------------------------------
        # ROS Publisher
        # ---------------------------------------

        self.encoder_pub = self.create_publisher(
            Int64MultiArray,
            '/encoder_counts',
            10
        )

        # ---------------------------------------
        # Current command
        # ---------------------------------------

        self.last_command = 'S'

        # ---------------------------------------
        # Send command every 50 ms
        # Keeps Arduino watchdog alive
        # ---------------------------------------

        self.timer = self.create_timer(
            0.05,
            self.send_command
        )

        # ---------------------------------------
        # Background thread to read encoder data
        # ---------------------------------------

        self.reader = threading.Thread(
            target=self.read_serial,
            daemon=True
        )

        self.reader.start()

        self.get_logger().info("Motor Serial Node Ready")


    #==========================================================
    # Receive cmd_vel
    #==========================================================

    def cmd_callback(self, msg):

        if msg.linear.x > 0.05:
            self.last_command = 'F'

        elif msg.linear.x < -0.05:
            self.last_command = 'B'

        elif msg.angular.z > 0.05:
            self.last_command = 'L'

        elif msg.angular.z < -0.05:
            self.last_command = 'R'

        else:
            self.last_command = 'S'


    #==========================================================
    # Send command to Arduino
    #==========================================================

    def send_command(self):

        try:

            self.serial_port.write(
                (self.last_command + '\n').encode()
            )

        except Exception as e:

            self.get_logger().error(f"Serial Write Error: {e}")


    #==========================================================
    # Read Encoder Data
    #==========================================================

    def read_serial(self):

        while rclpy.ok():

            try:

                line = self.serial_port.readline().decode(
                    errors='ignore'
                ).strip()

                if not line:
                    continue

                # Expected format:
                # E,1234,1256

                parts = line.split(',')

                if len(parts) != 3:
                    continue

                if parts[0] != 'E':
                    continue

                left = int(parts[1])
                right = int(parts[2])

                msg = Int64MultiArray()
                msg.data = [left, right]

                self.encoder_pub.publish(msg)

                # Uncomment only for debugging
                # self.get_logger().info(f"L={left} R={right}")

            except Exception:
                continue


#==========================================================
# Main
#==========================================================

def main(args=None):

    rclpy.init(args=args)

    node = MotorSerial()

    try:

        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:

        node.serial_port.close()

        node.destroy_node()

        rclpy.shutdown()


if __name__ == '__main__':
    main()
