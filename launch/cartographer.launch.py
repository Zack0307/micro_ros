import os
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    # get_packages
    pkg_share = get_package_share_directory('micro_ros')
    
    # use_sim_time 
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    # map resolution
    resolution = LaunchConfiguration('resolution', default='0.05')
    # map publish period sec
    publish_period_sec = LaunchConfiguration('publish_period_sec', default='1.0')
    
    # configuration
    configuration_basename = LaunchConfiguration('configuration_basename', default='carto.lua')

    
    cartographer_node = Node(
        package='cartographer_ros',
        executable='cartographer_node',
        name='cartographer_node',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time}],
        arguments=[
            '-configuration_directory', os.path.join(pkg_share, "config"),
            '-configuration_basename', configuration_basename
        ],
        remappings=[
            ('scan', '/scan'),  # 將你的光達 Topic 對應給 Cartographer
            ('odom', '/odom')   # 將你的里程計 Topic 對應給 Cartographer
        ]
    )

    occupancy_grid_node = Node(
        package='cartographer_ros',
        executable='cartographer_occupancy_grid_node',
        name='cartographer_occupancy_grid_node',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time}],
        arguments=['-resolution', resolution, '-publish_period_sec', publish_period_sec])

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        # arguments=['-d', rviz_config_dir],
        parameters=[{'use_sim_time': use_sim_time}],
        output='screen')
   
    return LaunchDescription([
        cartographer_node,
        occupancy_grid_node,
        rviz_node
    ])