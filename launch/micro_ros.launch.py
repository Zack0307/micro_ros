from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import  LaunchConfiguration
from launch_ros.actions import Node
from launch.substitutions import Command, LaunchConfiguration

from launch_ros.parameter_descriptions import ParameterValue


from ament_index_python.packages import get_package_share_path

def generate_launch_description():

    urdf_tutorial_path = get_package_share_path('micro_ros')
    default_model_path = urdf_tutorial_path / 'urdf/MicroROS.urdf'
    rviz_path = urdf_tutorial_path / 'rviz/yahboomcar.rviz'

    model_arg = DeclareLaunchArgument(name='model', default_value=str(default_model_path),
                                      description='Absolute path to robot urdf file')
    robot_description = ParameterValue(Command(['xacro ', LaunchConfiguration('model')]),
                                       value_type=str)

    control_node = Node(
        package='micro_ros',
        executable='joy',
        emulate_tty=True
    )

    micro_ros_joy_node = Node(
        package='joy',
        executable='joy_node',
    )

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description}]
    )

    joint_state_publisher_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui'
    )

    
    tf_base_footprint_to_base_link = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=['0', '0', '0.05', '0.0', '0.0', '0.0', 'base_footprint', 'base_link'],
    )
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_path],
    )


    return LaunchDescription([
        control_node,
        micro_ros_joy_node,
        model_arg,
        joint_state_publisher_gui_node,
        robot_state_publisher_node,
        tf_base_footprint_to_base_link,
        rviz_node
    ])
