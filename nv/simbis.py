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

# Xbox360 gamepad library
from inputs import get_gamepad
import math
import threading

# ---------------------------- VARIABLES GLOBALES ---------------------------

vecteur_commande = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
message_publisher = rospy.Publisher("/divy2/thrusters/0/input", FloatStamped, queue_size=50)

# Buttons
BTN_A = False
BTN_B = False
BTN_X = False
BTN_Y = False

BTN_SELECT=False

# Gachette L et R
BTN_L = False     # Left Bumper
BTN_R = False     # Right Bumper

#PRESSION Joysticks gauche et droite
BTN_TH_Gauche = False # Left Joystick Button
BTN_TH_Droite = False # Right Joystick Button

# Joystick de GAUCHE
ABS_Lacet = 0  # Left X Stick (left/right)
ABS_X = 0  # Left Y Stick (up/down)

#Joystick de DROITE
ABS_Tanguage = 0 # Right X Stick UPDOWN
ABS_Roulis = 0 # Right Y Stick, gauchedroite

# CROIX
Croix_Bas_X = False
Croix_Haut_X = False
Croix_Droite_Y = False
Croix_Gauche_Y = False

MAX_TRIG_VAL = math.pow(2,8)
MAX_JOY_VAL = math.pow(2,15)

# ---------------------------- GESTION CODE ---------------------------

def vectorization_info_recue( vecteur_commande ) :

    gamepad = get_gamepad() # Set up the gamepad processor

    for event in gamepad :
        # DEPLACEMENT SUR X
        if event.code == 'ABS_Y':
            print('X')
            ABS_X = -event.state/MAX_JOY_VAL # normalisation entre -1 et 1
            vecteur_commande[0] = ABS_X

        # LACET
        elif event.code == 'ABS_X':
            print('LACET')
            ABS_Lacet = -event.state/MAX_JOY_VAL # normalisation entre -1 et 1
            vecteur_commande[5] = ABS_Lacet

        # TANGAGE
        elif event.code == 'ABS_RY':
            print('TANGAGE')
            ABS_Tanguage = -event.state/MAX_JOY_VAL # normalisation entre -1 et 1
            vecteur_commande[4] = ABS_Tanguage

        # ROULIS
        elif event.code == 'ABS_RX':
            print('ROULIS')
            ABS_Roulis = event.state/MAX_JOY_VAL # normalisation entre -1 et 1
            vecteur_commande[3] = ABS_Roulis

        #Pression joystick gauche, DÉCENDRE selon Z
        elif event.code == 'BTN_THUMBL':
            print('-Z')
            if event.state == 1 :
                vecteur_commande[2] = -0.4 # facteur arbitraire
            if event.state == 0 :
                vecteur_commande[2] = 0 # arrete le mouvement sur -Z

        #Pression joystick gauche, MONTER selon Z
        elif event.code == 'BTN_THUMBR':
            print('+Z')
            if event.state == 1 :
                vecteur_commande[2] = 0.4 # facteur arbitraire
            if event.state == 0 :
                vecteur_commande[2] = 0 # arrete le mouvement sur -Z

        # Eteinte du ROV
        elif event.code == 'BTN_SELECT' :
            print('SHUTDOWN')
            quit()

    return vecteur_commande

#------------------------------------------------------------------------------

#V2
invrow1 = np.array([-0.7071, 0.7071 , 0     , 113.8442 , 113.8442 , -27.5772])
invrow2 = np.array([0.7071 , 0.7071 , 0     , 113.8442 , -113.8442, 43.8406 ])
invrow3 = np.array([0.7071 , -0.7071, 0     , -113.8442, -113.8442, -43.8406])
invrow4 = np.array([-0.7071, -0.7071, 0     , -113.8442, 113.8442 , 27.5772 ])
invrow5 = np.array([0      , 0      , 1.0000, -150.0000, 19.0000  , 0       ])
invrow6 = np.array([0      , 0      , 1.0000,  149.0000, 85.0000  , 0       ])

invM = np.array([invrow1, invrow2, invrow3, invrow4, invrow5, invrow6])


# Calcul des param articulaires à partir des commandes envoyées par la manette
def commande_to_param( commande_vect ) :
     new_param = np.dot(invM,commande_vect)
     return new_param


def Gazebo_Publisher():

     #"manette" compris entre -100 et 100
     #commande_vect = [0,20,0,0,0,0]
     #paramètres articulaires envoyés dans les moteurs
     #matrice_result = [0,0,0,0,-50,-50]
     #matrice_result = commande_to_param( commande_vect )

     rospy.init_node("simulation_manette", anonymous=True) #Setting anonymous=True will append random integers at the end of our publisher node
     rate = rospy.Rate(10)
     iteration = 1

     #Keep publishing the messages until the user interrupts
     while not rospy.is_shutdown():

         commande_envoyee = vectorization_info_recue( vecteur_commande )
         commande_envoyee=100*commande_envoyee

         rospy.loginfo("iteration")
         rospy.loginfo(iteration)
         rospy.loginfo("Entrée manette tq [x,y,z,Rx,Ry,Rz]: ") #display the message on the terminal
         rospy.loginfo(commande_envoyee) # peut pas concatener string et float

         matrice_result = commande_to_param( commande_envoyee )
         pourcentage = commande_envoyee[0]

         for i in range(1,6):
            if np.abs(commande_envoyee[i])>pourcentage:
                pourcentage=np.abs(commande_envoyee[i])

         valMax = matrice_result[0]
         for i in range(1,6):
           if np.abs(matrice_result[i])>valMax:
               valMax=np.abs(matrice_result[i])

         newmat= [0,0,0,0,0,0]
         if valMax != 0:
            for i in range(1,6):
               newmat[i]=matrice_result[i]*pourcentage/valMax

         headerone = Header()
         headerone.seq = 0.0
         #headerone.stamp.sec =0.0
         #headerone.stamp.nsec =0.0
         headerone.frame_id = 'test'
         envoi = FloatStamped()
         envoi.header = headerone

         message_publisher = rospy.Publisher("/divy2/thrusters/0/input", FloatStamped, queue_size=50)
         #envoi.data = matrice_result[0]
         envoi.data = newmat[0]
         message_publisher.publish(envoi)

         message_publisher = rospy.Publisher("/divy2/thrusters/1/input", FloatStamped, queue_size=50)
         #envoi.data = matrice_result[1]
         envoi.data = newmat[1]
         message_publisher.publish(envoi)

         message_publisher = rospy.Publisher("/divy2/thrusters/2/input", FloatStamped, queue_size=50)
         #envoi.data = matrice_result[2]
         envoi.data = newmat[2]
         message_publisher.publish(envoi)

         message_publisher = rospy.Publisher("/divy2/thrusters/3/input", FloatStamped, queue_size=50)
         #envoi.data = matrice_result[3]
         envoi.data = newmat[3]
         message_publisher.publish(envoi)

         message_publisher = rospy.Publisher("/divy2/thrusters/4/input", FloatStamped, queue_size=50)
         #envoi.data = matrice_result[4]
         envoi.data = newmat[4]
         message_publisher.publish(envoi)

         message_publisher = rospy.Publisher("/divy2/thrusters/5/input", FloatStamped, queue_size=50)
         #envoi.data = matrice_result[5]
         envoi.data = newmat[5]
         message_publisher.publish(envoi)


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


if __name__ == "__main__":
     try:
         Gazebo_Publisher()
     #capture the Interrupt signals
     except rospy.ROSInterruptException:
         pass
