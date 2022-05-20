#import the rospy package and the String message type
# coding=utf-8
import rospy
from std_msgs.msg import String #float à voir String sinon
from std_msgs.msg import Float64MultiArray
from std_msgs.msg import Float64
from std_msgs.msg import MultiArrayDimension
import numpy as np

#----------------------- VARIABLES GLOBALES ------------------------------------------
data_received = None
commande_vect = None
started = False

#message topic
message_publisher = rospy.Publisher("param_articulaire", Float64MultiArray, queue_size=100)
iteration_geom=1

#----------------------- GESTION CODE -----------------------------------------------

# Modèle pseudo géométrique inverse (MGI)
invrow1 = np.array([-0.7071, 0.7071 , 0     , 113.8442 , 113.8442 , -27.5772])
invrow2 = np.array([0.7071 , 0.7071 , 0     , 113.8442 , -113.8442, 43.8406 ])
invrow3 = np.array([0.7071 , -0.7071, 0     , -113.8442, -113.8442, -43.8406])
invrow4 = np.array([-0.7071, -0.7071, 0     , -113.8442, 113.8442 , 27.5772 ])
invrow5 = np.array([0      , 0      , 1.0000, -150.0000, 19.0000  , 0       ])
invrow6 = np.array([0      , 0      , 1.0000,  149.0000, 85.0000  , 0       ])
invM = np.array([invrow1, invrow2, invrow3, invrow4, invrow5, invrow6])


# Fonction de conversion du vecteur de commande par la manette en valeur des paramètres articulaires
def commande_to_param( commande_vect ) :
     new_param = np.dot(invM,commande_vect)
     return new_param

#---------------------- GESTION ROS ---------------------------------------


#récupération du vecteur de commande Manette
def vecteur_callback(vect):
     # Each subscriber gets 1 callback, and the callback either stores information and/or computes something and/or publishes It _does not!_ return anything
     global data_received, commande_vect, started, iteration_geom
     rospy.loginfo("\n-----------------------\n")
     rospy.loginfo("Subscribed: vecteurde commande reçu de Gamepad")
     rospy.loginfo(vect.data)
     data_received = vect
     commande_vect = vect.data
     rospy.loginfo("\n-----------------------\n")
     rospy.loginfo("iteration :")
     rospy.loginfo(iteration_geom)
     iteration_geom = iteration_geom+1

     #if (not started):
     rospy.loginfo('Started = true')
     started = True

#attente pour publish = non suprposition des commandes ROS
def timer_callback(event):
    global started, message_publisher, commande_vect

    print("dans timer callbakc")

    if (started):
        print("dansleif")
        # calcul des param articulaires à partir du vecteur de commandes de la manette
        pourcentage = commande_vect[0]

        for i in range(1,6):
            if np.abs(commande_vect[i])>pourcentage:
                pourcentage=np.abs(commande_vect[i])

        #paramètres articulaires envoyés dans les moteurs
        #matrice_result = [0,0,0,0,-50,-50]

        matrice_result = commande_to_param( commande_vect )

        valMax = matrice_result[0]
        for i in range(1,6):
            if np.abs(matrice_result[i])>valMax:
                valMax=np.abs(matrice_result[i])

        newmat= [0,0,0,0,0,0]
        if valMax != 0:
            for i in range(1,6):
                newmat[i]=matrice_result[i]*pourcentage/valMax

        rospy.init_node("gazebo", anonymous=True) #Setting anonymous=True will append random integers at the end of our publisher node
        #rate = rospy.Rate(1)
        iteration = 1


        headerone = Header()
        headerone.seq = 0.0
        #headerone.stamp.sec =0.0
        #headerone.stamp.nsec =0.0
        headerone.frame_id = 'test'
        envoi = FloatStamped()
        envoi.header = headerone

        message_publisher = rospy.Publisher("/divy2/thrusters/0/input", FloatStamped, queue_size=1)
        #envoi.data = matrice_result[0]
        envoi.data = newmat[0]
        message_publisher.publish(envoi)

        message_publisher = rospy.Publisher("/divy2/thrusters/1/input", FloatStamped, queue_size=1)
        #envoi.data = matrice_result[1]
        envoi.data = newmat[1]
        message_publisher.publish(envoi)

        message_publisher = rospy.Publisher("/divy2/thrusters/2/input", FloatStamped, queue_size=1)
        #envoi.data = matrice_result[2]
        envoi.data = newmat[2]
        message_publisher.publish(envoi)

        message_publisher = rospy.Publisher("/divy2/thrusters/3/input", FloatStamped, queue_size=1)
        #envoi.data = matrice_result[3]
        envoi.data = newmat[3]
        message_publisher.publish(envoi)

        message_publisher = rospy.Publisher("/divy2/thrusters/4/input", FloatStamped, queue_size=1)
        #envoi.data = matrice_result[4]
        envoi.data = newmat[4]
        message_publisher.publish(envoi)

        message_publisher = rospy.Publisher("/divy2/thrusters/5/input", FloatStamped, queue_size=1)
        #envoi.data = matrice_result[5]
        envoi.data = newmat[5]
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

        #rate.sleep() #will wait enough until the node publishes the message to the topic
        iteration = iteration +1


#reçoit l'information
def vectSubscriber():
     #initialize the subscriber node called 'messageSubNode'
     rospy.init_node("mod_geom_suscriber", anonymous=True)

     #This is to subscribe to the messages from the topic named 'messageTopic'
     rospy.Subscriber("commande_envoyee", Float64MultiArray, vecteur_callback)
     print("before timer")
     timer = rospy.Timer(rospy.Duration(1), timer_callback)
     timer_callback(1);
     print("after timer")

     #rospy.spin() stops the node from exitind until the node has been shut down
     rospy.spin()
     timer.shutdown()

if __name__ == "__main__":
    try:
         vectSubscriber()
    except rospy.ROSInterruptException:
         pass
