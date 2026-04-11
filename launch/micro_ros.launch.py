from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import  LaunchConfiguration
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription

def generate_launch_description():

    control_node = Node(
        package='micro_ros',
        node_executable='joy',
        emulate_tty=True
    )


    micro_ros_joy_node = Node(
        package='joy',
        node_executable='joy_node',
    )


    return LaunchDescription([
        driver_node,
        micro_ros_joy_node
    ])
