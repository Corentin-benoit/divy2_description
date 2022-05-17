cmake_minimum_required(VERSION 2.8.3)
project(divy2_description)

find_package(catkin REQUIRED)
#INCLUDE_DIRECTORIES(tmp/uuv_simulator/uuv_gazebo_plugins/uuv_gazebo_ros_plugins_msg)
#find_package(catkin uuv_gazebo_ros_plugins_msgs REQUIRED roscpp rospy std_msgs message_generation)
find_package(uuv_gazebo_ros_plugins_msgs REQUIRED)
catkin_package()

install(DIRECTORY meshes robots urdf launch
        DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
        PATTERN "*~" EXCLUDE)


install(DIRECTORY launch meshes robots urdf
        DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
        PATTERN "*~" EXCLUDE)


if(CATKIN_ENABLE_TESTING)
  find_package(rostest REQUIRED)
  find_package(xacro REQUIRED)
  find_package(rosunit REQUIRED)
  foreach(T
      )
     add_rostest(${T})
  endforeach()
endif()
