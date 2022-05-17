#import the rospy package and the String message type
# coding=utf-8
import rospy
from std_msgs.msg import String #float à voir String sinon
from std_msgs.msg import Float64MultiArray
from std_msgs.msg import Float64
from std_msgs.msg import Header
from std_msgs.msg import MultiArrayDimension

#from naoqi_bridge_msgs.msg import FloatStamped
#sys.path.append('D:tmp/uuv_simulator/uuv_gazebo_plugins/uuv_gazebo_ros_plugins_msg/')
from uuv_gazebo_ros_plugins_msgs.msg import FloatStamped

from std_msgs.msg import Float32
import numpy as np

def Gazebo_Publisher():

     #define a topic to which the messages will be published
     message_publisher = rospy.Publisher("/divy2/thrusters/4/input", FloatStamped, queue_size=1) #message topic

     #initialize the Publisher node.
     rospy.init_node("gazebo", anonymous=True) #Setting anonymous=True will append random integers at the end of our publisher node

     #publishes at a rate of
     rate = rospy.Rate(1)
     iteration = 1

     matrice_result = [20,20,20,20,20,20]

     #Keep publishing the messages until the user interrupts
     while not rospy.is_shutdown():

	 
         headerone = Header()
         headerone.seq = 0.0
         #headerone.stamp.sec =0.0
         #headerone.stamp.nsec =0.0
         headerone.frame_id = 'test'
	 

         envoi = FloatStamped()
         envoi.data = matrice_result[0]
         envoi.header = headerone

         message_publisher.publish(envoi)
         rospy.loginfo("iteration")
         rospy.loginfo(iteration)
         rospy.loginfo("\n")
         rospy.loginfo("Published: ") #display the message on the terminal

         rospy.loginfo(envoi.data) 
         rospy.loginfo("\n-------------------------\n")

         rate.sleep() #will wait enough until the node publishes the message to the topic
         iteration = iteration +1


if __name__ == "__main__":
     try:
         Gazebo_Publisher()
     #capture the Interrupt signals
     except rospy.ROSInterruptException:
         pass
