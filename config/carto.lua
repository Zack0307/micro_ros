include "map_builder.lua"
include "trajectory_builder.lua"

options = {
  map_builder = MAP_BUILDER,
  trajectory_builder = TRAJECTORY_BUILDER,
  map_frame = "map",
  tracking_frame = "base_link",          -- 機器人的中心座標
  published_frame = "base_link",         -- TF 樹中作為子節點發布的座標系
  odom_frame = "odom",                   -- 里程計座標系
  provide_odom_frame = true,             -- 如果你沒有外部里程計節點提供 odom->base_link，可設為 true 讓 Cartographer 提供
  publish_frame_projected_to_2d = true,  -- publish 2D information
  use_pose_extrapolator = true,
  use_odometry = true,                   -- 是否使用外部的里程計 (odom) 主題
  use_nav_sat = false,
  use_landmarks = false,
  num_laser_scans = 1,                   -- 接收的光達感測器數量
  num_multi_echo_laser_scans = 0,
  num_subdivisions_per_laser_scan = 1,
  num_point_clouds = 0,
  lookup_transform_timeout_sec = 0.2,
  submap_publish_period_sec = 0.3,
  pose_publish_period_sec = 5e-3,
  trajectory_publish_period_sec = 30e-3,
  rangefinder_sampling_ratio = 1.,
  odometry_sampling_ratio = 1.,
  fixed_frame_pose_sampling_ratio = 1.,
  imu_sampling_ratio = 1.,
  landmarks_sampling_ratio = 1.,
}

-- 如果你的機器人只有 2D 光達且沒有 IMU，請加入以下覆寫：
MAP_BUILDER.use_trajectory_builder_2d = true
TRAJECTORY_BUILDER_2D.use_imu_data = false
TRAJECTORY_BUILDER_2D.min_range = 0.3 -- 光達最小有效距離
TRAJECTORY_BUILDER_2D.max_range = 8.0 -- 光達最大有效距離

return options