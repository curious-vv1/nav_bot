This is a set up of a mobile robot (custom urdf) in a Gazebo (Harmonic) simulation using Nav2 in ROS 2 Humble. Nav2 has been used for autonomous navigation, avoiding static and dynamic obstacles while reaching a goal input by user.

# Setup Instructions

Make a workspace and src folder. In the src folder clone this repo using command  
`git clone https://github.com/curious-vv1/nav_bot.git`

Use the command  
`colcon build`  
to make build, install and log files in the ros workspace.

# Steps to build and run the simulation

Run the following command to launch gazebo with customized world and spawned entity:  
`ros2 launch nav_bot gazebo_launch.py world:=./worlds/obstacle.world`

Run the following command to open rviz configured as the requirement:  
`rviz2 -d ./config/navigation.rviz`

Run the following command to make your own map using slam:  
`ros2 launch slam_toolbox online_async_launch.py slam_params_file:=./config/mappers_params_online_async.yaml use_sim_time:=true`

Run the following command for localization using slam:  
`ros2 launch slam_toolbox online_async_launch.py slam_params_file:=./config/mappers_params_online_async.yaml use_sim_time:=true`  
Make sure to make changes in mappers_params_online_async.yaml for localization.

Run the following command for amcl localization:  
`ros2 launch nav_bot localization_launch.py map:=./maps/my_map_save.yaml use_sim_time:=true`  
my_map_save.yaml is generated map that can be used.  
In rviz change fixed frame to map and if the map still doesn't appear change topic -> Durability to transient local.

Run the following command to start navigation with obstacle avoidance:  
`ros2 launch nav_bot navigation_launch.py use_sim_time:=true map_subscribe_transient_local:=true`  
map_subscribe_transient_local:=true if topic -> Durability is set to transient local.

Now run the script to initialize starting position and input goal position(there are three input position in x-axis and y-axis and orientation  which takes a quaternion value):  
`python3 ./src/nav_bot/script/navigation_by_poses.py`  
Once the goal is reached you can input a new goal position as well.

## Following is a sample showing the robot successfully navigating to the goal while avoiding obstacles

Drive Link:- https://drive.google.com/file/d/1PFR9V--mucsstYXugDUwDcRx7oSW2oQ6/view?usp=sharing


## Approach to localization, planning, and obstacle avoidance

1. A customized bot with dimensions 300cm*300cm*150cm was made with 50 cm radius wheels and 50 cm caster wheel

2. Gazebo plugins libgazebo_ros_diff_drive.so for differential drive, libgazebo_ros_ray_sensor.so for lidar and libgazebo_ros_camera.so for camera was used

3. Nav2 documentation was used for localization and mapping using SLAM and AMCL

4. Used simple commander api documentation and its example to understand and make script for user given input static and dynamic obstacle avoidance to rach goal

## Challenges faced and solutions

1. Challenge: ROS convention and camera convention for frame are different  
  Solution: Added a camera_link_optical that to compensate this with rpy="${-pi/2} 0 ${-pi/2}"

2. Challenge: Camera was obtaining images of different color  
  Solution: `<format>R8G8B8</format>` changed the format by hit and trial to get it right

3. Challenge: Map not subscribed on rviz even when topic rviz was published  
  Solution: Put map as fixed frame manually and set topic->Durability to Transient Local

4. Challenge: While using the script the bot sometimes would reach right orientation and sometimes not  
  Solution: Learnt that the orientations are in quaternion and got to know how the orientations are represented by them

