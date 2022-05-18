#import the rospy package and the String message type
# coding=utf-8
import rospy
from std_msgs.msg import String
from std_msgs.msg import Float64MultiArray
from std_msgs.msg import Float64
from std_msgs.msg import Header
from std_msgs.msg import MultiArrayDimension
from uuv_gazebo_ros_plugins_msgs.msg import FloatStamped
from std_msgs.msg import Float32
import numpy as np



# Modèle pseudo géométrique inverse (MGI)
#V1
#invrow1 = np.array([ 0.1037,  0.0113,  0.0060,  0.0159,  0.1242, -0.0071])
#invrow2 = np.array([ 0.2489,  0.0174,  0.0119, -0.0266,  0.2897,  0.0071])
#invrow3 = np.array([ 0.2452,  0.0107,  0.0117, -0.0198,  0.2854, -0.0071])
#invrow4 = np.array([ 0.1013,  0.0028,  0.0059, -0.0074,  0.1224,  0.0071])
#invrow5 = np.array([-0.2727, -0.0218, -0.0112,  0.0360, -0.3200,  0.0000])
#invrow6 = np.array([-0.2689, -0.0109, -0.0110,  0.0180, -0.3157,  0.0000])

#V2

invrow1 = np.array([0.003236363154712,  -0.001496237387059,  -0.001321626234291,   0.000566917252094,  -0.000973738668841,  -0.007001057239471])
invrow2 = np.array([0.001246299062173,  -0.001124714898755,  -0.001463773669472,   0.000095441789022,  -0.003416620025856,   0.007001057239471])
invrow3 = np.array([0.001246299062173,   0.000275128293093,  -0.001463773669472,  -0.001304401402825,  -0.003416620025856,  -0.007001057239471])
invrow4 = np.array([0.003236363154712,   0.000729154353827,  -0.001321626234291,  -0.001658474488792,  -0.000973738668841,   0.007001057239471])
invrow5 = np.array([0.004333101660993,  -0.002161672848377,   0.000309507261499,  -0.003076055053748,  -0.004243877774392,  -0.000000000000000])
invrow6 = np.array([0.004362182880194,   0.000593698078125,   0.000311584491442,   0.000844830879468,  -0.004272360175562,  -0.000000000000000])

invM = np.array([invrow1, invrow2, invrow3, invrow4, invrow5, invrow6])

def commande_to_param( commande_vect ) :

     new_param = np.dot(invM,commande_vect)
     return new_param

def Gazebo_Publisher():

     #"manette" compris entre -100 et 100
     #commande_vect = [0,0,-100000,0,0,0]

     pourcentage = 1 #commande_vect[0]
     '''
     for i in range(1,6):
        if np.abs(commande_vect[i])>pourcentage:
            pourcentage=np.abs(commande_vect[i])

     '''


     #paramètres articulaires envoyés dans les moteurs
     matrice_result = [0,0,0,0,-50,-50]



     #matrice_result = commande_to_param( commande_vect )

     valMax = matrice_result[0]
     for i in range(1,6):
        if np.abs(matrice_result[i])>valMax:
            valMax=np.abs(matrice_result[i])

     newmat= [0,0,0,0,0,0]
     if valMax != 0:
         for i in range(1,6):
            newmat[i]=matrice_result[i]*pourcentage/valMax

     rospy.init_node("gazebo", anonymous=True) #Setting anonymous=True will append random integers at the end of our publisher node
     rate = rospy.Rate(1)
     iteration = 1

     #Keep publishing the messages until the user interrupts
     while not rospy.is_shutdown():

         headerone = Header()
         headerone.seq = 0.0
         #headerone.stamp.sec =0.0
         #headerone.stamp.nsec =0.0
         headerone.frame_id = 'test'
         envoi = FloatStamped()
         envoi.header = headerone

         message_publisher = rospy.Publisher("/divy2/thrusters/0/input", FloatStamped, queue_size=1)
         envoi.data = matrice_result[0]
         #envoi.data = newmat[0]
         message_publisher.publish(envoi)

         message_publisher = rospy.Publisher("/divy2/thrusters/1/input", FloatStamped, queue_size=1)
         envoi.data = matrice_result[1]
         #envoi.data = newmat[1]
         message_publisher.publish(envoi)

         message_publisher = rospy.Publisher("/divy2/thrusters/2/input", FloatStamped, queue_size=1)
         envoi.data = matrice_result[2]
         #envoi.data = newmat[2]
         message_publisher.publish(envoi)

         message_publisher = rospy.Publisher("/divy2/thrusters/3/input", FloatStamped, queue_size=1)
         envoi.data = matrice_result[3]
         #envoi.data = newmat[3]
         message_publisher.publish(envoi)

         message_publisher = rospy.Publisher("/divy2/thrusters/4/input", FloatStamped, queue_size=1)
         envoi.data = matrice_result[4]
         #envoi.data = newmat[4]
         message_publisher.publish(envoi)

         message_publisher = rospy.Publisher("/divy2/thrusters/5/input", FloatStamped, queue_size=1)
         envoi.data = matrice_result[5]
         #envoi.data = newmat[5]
         message_publisher.publish(envoi)

         rospy.loginfo("iteration")
         rospy.loginfo(iteration)
         #rospy.loginfo("commande manette: ") #display the message on the terminal
         #rospy.loginfo(commande_vect)
         rospy.loginfo("\n")
         rospy.loginfo("Modèle géom inverse: ") #display the message on the terminal
         rospy.loginfo(matrice_result)
         rospy.loginfo("\n")
         rospy.loginfo("val max à ce tour: ") #display the message on the terminal
         rospy.loginfo(valMax)
         rospy.loginfo("\n")
         rospy.loginfo("valeurs calculées en pourcentage: ") #display the message on the terminal
         rospy.loginfo(newmat)

         rospy.loginfo("\n-------------------------\n")

         rate.sleep() #will wait enough until the node publishes the message to the topic
         iteration = iteration +1


if __name__ == "__main__":
     try:
         Gazebo_Publisher()
     #capture the Interrupt signals
     except rospy.ROSInterruptException:
         pass
