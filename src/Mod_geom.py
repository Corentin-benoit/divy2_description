#import the rospy package and the String message type
# coding=utf-8
import rospy
from std_msgs.msg import String #float à voir String sinon
from std_msgs.msg import Float64MultiArray
from std_msgs.msg import Float64
from std_msgs.msg import MultiArrayDimension

from naoqi_bridge_msgs.msg import FloatStamped

from std_msgs.msg import Float32
import numpy as np


#----------------------- VARIABLES GLOBALES ------------------------------------------

data_received = None
commande_vect = None
started = False
#message topic

iteration_geom=1
message_publisher = rospy.Publisher("/divy2/thrusters/0/input", FloatStamped, queue_size=100)
#message_publisher = rospy.Publisher("/divy2/thrusters/0/thrust uuv_gazebo_ros_plugins_msgs/FloatStamped/header", Float64MultiArray, queue_size=100)



#----------------------- GESTION CODE -----------------------------------------------

# Modèle pseudo géométrique inverse (MGI)
invrow1 = np.array([ 0.1037,  0.0113,  0.0060,  0.0159,  0.1242, -0.0071])
invrow2 = np.array([ 0.2489,  0.0174,  0.0119, -0.0266,  0.2897,  0.0071])
invrow3 = np.array([ 0.2452,  0.0107,  0.0117, -0.0198,  0.2854, -0.0071])
invrow4 = np.array([ 0.1013,  0.0028,  0.0059, -0.0074,  0.1224,  0.0071])
invrow5 = np.array([-0.2727, -0.0218, -0.0112,  0.0360, -0.3200,  0.0000])
invrow6 = np.array([-0.2689, -0.0109, -0.0110,  0.0180, -0.3157,  0.0000])
invM = np.array([invrow1, invrow2, invrow3, invrow4, invrow5, invrow6])


# Fonction de conversion du vecteur de commande par la manette en valeur des paramètres articulaires
def commande_to_param( commande_vect ) :

     new_param = np.dot(invM,commande_vect)
     return new_param
#new_param devra être published dans le topic PARAM_ARTICULAIRE pour le suscriber MOTEURS


#----------------------- GESTION ROS ---------------------------------------


#récupération du vecteur de commande Manette
def vecteur_callback(vect):
     # Each subscriber gets 1 callback, and the callback either stores information and/or computes something and/or publishes It _does not!_ return anything
     global data_received, commande_vect, started, iteration_geom

     rospy.loginfo("\n-----------------------\n")
     rospy.loginfo("Subscribed: vecteurde commande reçu de Gamepad")
     rospy.loginfo(vect.data)

     data_received = vect
     commande_vect = vect.data
     commande_vect = [1,0,0,0,0,0]

     rospy.loginfo("\n-----------------------\n")
     rospy.loginfo("iteration :")
     rospy.loginfo(iteration_geom)
     iteration_geom = iteration_geom+1

     if (not started):
        started = True


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#attente pour publish = non suprposition des commandes ROS
def timer_callback(event):
    global started, commande_vect, message_publisher

    rospy.loginfo("dans timer callback")
    print("danstime")
    if (started):

        #param_arti = Float64 MultiArray()
        #param_arti.data = commande_to_param( commande_vect )
    	#envoi = Float64
    	#matrice = commande_to_param( commande_vect )


        rospy.loginfo("Data envoyée dans les moteurs:")
        matrice_result = [20,20,20,20,20,20]
        rospy.loginfo(matrice_result)
        #commande_to_param( commande_vect );

        message_publisher = rospy.Publisher("/divy2/thrusters/5/input", FloatStamped, queue_size=100)

        headerone = Header()
        headerone.seq = 0.0
        headerone.stamp.sec =0.0
        headerone.stamp.nsec =0.0
        headerone.frame_id = 'test'

        envoi = FloatStamped()
        envoi.data = matrice_result[0]
        envoi.header = headerone

        message_publisher.publish(envoi)



    		#envoi.data=matrice[i]
    		#message_publisher.publish(envoi.data)
        #rospy.loginfo("Data envoyée dans les moteurs:")
            #rospy.loginfo(i)
            #rospy.loginfo("tq")
        #rospy.loginfo(matrice_result)

        # message_publisher.publish(param_arti)

	#changermat into float

    #rospy.loginfo("Last message published // Matrice transformée envoyée dans les moteurs :")
        #rospy.logingo(param_arti.data)
        #rospy.loginfo("\n-----------------------\n")




#reçoit l'information
def vectSubscriber():
     #initialize the subscriber node called 'messageSubNode'
     rospy.init_node("mod_geom_suscriber", anonymous=False)

     #This is to subscribe to the messages from the topic named 'messageTopic'
     rospy.Subscriber("commande_envoyee", Float64MultiArray, vecteur_callback)

     timer = rospy.Timer(rospy.Duration(0.1), timer_callback)

     #rospy.spin() stops the node from exitind until the node has been shut down
     rospy.spin()
     timer.shutdown()


if __name__ == "__main__":
    try:
         vectSubscriber()
    except rospy.ROSInterruptException:
         pass
