#!/usr/bin/env python3

import math
import rclpy

from rclpy.node import Node
from std_msgs.msg import Int64MultiArray
from nav_msgs.msg import Odometry
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster

from tf_transformations import quaternion_from_euler


class EncoderOdometry(Node):

    def __init__(self):

        super().__init__('encoder_odometry')

        self.subscription = self.create_subscription(
            Int64MultiArray,
            '/encoder_counts',
            self.encoder_callback,
            10
        )

                # Publish Odometry
        self.odom_pub = self.create_publisher(
            Odometry,
            '/odom',
            10
        )

        # TF Broadcaster
        self.tf_broadcaster = TransformBroadcaster(self)

        # Previous encoder counts
        self.prev_left = None
        self.prev_right = None

        # Robot parameters
        self.WHEEL_RADIUS = 0.04      # meters
        self.WHEEL_BASE = 0.26        # meters
        self.CPR = 4684.0

        # Robot pose
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0

        self.get_logger().info("Encoder Odometry Started")


    def encoder_callback(self, msg):
    
        left = msg.data[0]
        right = msg.data[1]
    
        # First encoder reading
        if self.prev_left is None:
            self.prev_left = left
            self.prev_right = right
            return
    
        # Encoder increments
        d_left = left - self.prev_left
        d_right = right - self.prev_right
    
        self.prev_left = left
        self.prev_right = right
    
        # Convert ticks to meters
        left_distance = (
            d_left * (2.0 * math.pi * self.WHEEL_RADIUS)
        ) / self.CPR
    
        right_distance = (
            d_right * (2.0 * math.pi * self.WHEEL_RADIUS)
        ) / self.CPR
    
        # Ignore tiny movements
        if abs(left_distance) < 1e-5 and abs(right_distance) < 1e-5:
            return
    
        # Differential-drive odometry
        d = (left_distance + right_distance) / 2.0
        d_theta = (right_distance - left_distance) / self.WHEEL_BASE
    
        self.x += d * math.cos(self.theta + d_theta / 2.0)
        self.y += d * math.sin(self.theta + d_theta / 2.0)
        self.theta += d_theta

        self.theta = math.atan2(
            math.sin(self.theta),
            math.cos(self.theta)
        )
    
        # Quaternion
        qx, qy, qz, qw = quaternion_from_euler(
            0.0,
            0.0,
            self.theta
        )
    
        # -------------------------
        # Publish Odometry
        # -------------------------
    
        odom = Odometry()
    
        odom.header.stamp = self.get_clock().now().to_msg()
        odom.header.frame_id = "odom"
    
        odom.child_frame_id = "base_link"
    
        odom.pose.pose.position.x = self.x
        odom.pose.pose.position.y = self.y
        odom.pose.pose.position.z = 0.0
    
        odom.pose.pose.orientation.x = qx
        odom.pose.pose.orientation.y = qy
        odom.pose.pose.orientation.z = qz
        odom.pose.pose.orientation.w = qw
    
        self.odom_pub.publish(odom)
    
        # -------------------------
        # Publish TF
        # -------------------------
    
        tf = TransformStamped()
    
        tf.header.stamp = odom.header.stamp
        tf.header.frame_id = "odom"
    
        tf.child_frame_id = "base_link"
    
        tf.transform.translation.x = self.x
        tf.transform.translation.y = self.y
        tf.transform.translation.z = 0.0
    
        tf.transform.rotation.x = qx
        tf.transform.rotation.y = qy
        tf.transform.rotation.z = qz
        tf.transform.rotation.w = qw
    
        self.get_logger().info(
            f"Publishing TF: odom -> base_link ({self.x:.3f}, {self.y:.3f})"
        )
        
        self.tf_broadcaster.sendTransform(tf)
    
        self.get_logger().info(
            f"x={self.x:.3f}  "
            f"y={self.y:.3f}  "
            f"theta={math.degrees(self.theta):.1f}"
        )


def main(args=None):

    rclpy.init(args=args)

    node = EncoderOdometry()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()
