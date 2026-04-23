#final integrate
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import  LaunchConfiguration
from launch_ros.actions import Node
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_path
import os
import xacro

def generate_launch_description():

    pkg_path = get_package_share_path('micro_ros')
    default_model_path = pkg_path / 'urdf/MicroROS.urdf.xacro'
    rviz_path = pkg_path / 'rviz/yahboomcar.rviz'
    world_path = pkg_path / 'world/test.sdf'

    # model_arg = DeclareLaunchArgument(name='model', default_value=str(default_model_path),
    #                                   description='Absolute path to robot urdf file')
    # robot_description = ParameterValue(Command(['xacro ', LaunchConfiguration('model')]),
    #                                    value_type=str)
    doc = xacro.process_file(default_model_path, mappings={'use_sim' : 'true'})
    robot_description = doc.toprettyxml(indent='  ')
    #cartographer
    # use_sim_time 
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    # map resolution
    resolution = LaunchConfiguration('resolution', default='0.05')
    # map publish period sec
    publish_period_sec = LaunchConfiguration('publish_period_sec', default='1.0')
    
    # configuration
    configuration_basename = LaunchConfiguration('configuration_basename', default='carto.lua')

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
        parameters=[{'robot_description': robot_description,
                     'use_sim_time': use_sim_time}]
    )

    joint_state_publisher_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui'
    )

    

    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('ros_gz_sim'),
                'launch',
                'gz_sim.launch.py'
            ])
        ]),
        # gz_args 裡面可以換成你自己畫的 .sdf 世界檔路徑
        # -r 代表啟動後直接開始執行 (Run)，不然預設會是暫停狀態
        launch_arguments={'gz_args': [LaunchConfiguration('world'),'.sdf',' -v 4',' -r']}.items() 
    )

    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-name', 'zack',         # 給你的車子取個名字
            '-world', 'empty',               # 代表要在 Gazebo 的 world 裡面出生
            '-topic', '/robot_description',    # 告訴 Gazebo 去哪裡拿 URDF 模型資料
            '-string', robot_description,
            '-x', '0.0',                      # 出生點 X 座標
            '-y', '0.0',                      # 出生點 Y 座標
            '-z', '0.1'                       # 出生點 Z 座標 (稍微抬高一點避免卡進地板)
        ],
        output='screen'
    )

    bridge_node = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
            '/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan',
            '/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry',
            '/tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V', # 如果 Gazebo 有發佈 TF
            '/joint_states@sensor_msgs/msg/JointState[gz.msgs.Model'  #gz sim to ros
        ],
        output='screen'
    )

    cartographer_node = Node(
        package='cartographer_ros',
        executable='cartographer_node',
        name='cartographer_node',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time}],
        arguments=[
            '-configuration_directory', os.path.join(pkg_path, "config"),
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
        parameters=[{'use_sim_time': use_sim_time}]
    )


    return LaunchDescription([
        # control_node,
        # micro_ros_joy_node,
        # model_arg,
        # joint_state_publisher_gui_node,
        robot_state_publisher_node,
        # cartographer_node,
        # occupancy_grid_node,
        tf_base_footprint_to_base_link,
        gz_sim,
        spawn_robot,
        bridge_node,
        # rviz_node
    ])
