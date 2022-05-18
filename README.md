# Projet-industriel_forssea

## Lancement du projet 



- Terminal 1 : roscore (Communication des noeuds)
- Terminal 2 : roslaunch uuv_gazebo_worlds empty_underwater_world.launch (Démarre l'environnement de simulation)
- (OU de préférence) roslaunch uuv_gazebo_worlds ocean_waves.launch
- Terminal 3 : roslaunch divy2_description upload_divy2.launch (Simulation du robot)



https://github.com/itu-auv/uuv-simulator-guide



```
rostopic pub /<robot_name>/thrusters/<index>/input uuv_gazebo_ros_plugins_msgs/FloatStamped "header:  
  seq: 0
  stamp:
    secs: 0
    nsecs: 0
  frame_id: ''
data: 1700.0"
```



rostopic pub /divy2/thrusters/0/input uuv_gazebo_ros_plugins_msgs/FloatStamped "header:  
  seq: 0
  stamp:
    secs: 0
    nsecs: 0
  frame_id: ''
data: 10.0"



