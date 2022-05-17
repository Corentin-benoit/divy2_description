# coding=utf-8

#from dataclasses import dataclass
import rospy
from std_msgs.msg import String #float à voir String sinon
from std_msgs.msg import Float64MultiArray
from std_msgs.msg import Float64
from std_msgs.msg import MultiArrayDimension

# Xbox360 gamepad library
#from inputs import get_gamepad

import numpy as np
import math
import threading

# ---------------------------- VARIABLES GLOBALES ---------------------------

vecteur_commande = np.array([1.0, 1.0, 0.0, 0.0, 0.0, 0.0])

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
'''
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
            vecteur_commande[2] = -0.4 # facteur arbitraire

        #Pression joystick gauche, MONTER selon Z
        elif event.code == 'BTN_THUMBR':
            print('+Z')
            vecteur_commande[2] = 0.4

    #--------------- Autre version pour plus de confort -----------------------

        #selon X
        elif event.code == 'BTN_TRIGGER_HAPPY3':
            print('+X')
            vecteur_commande[0] = 0.4
        elif event.code == 'BTN_TRIGGER_HAPPY4':
            print('-X')
            vecteur_commande[0] = -0.4

        #lacet
        elif event.code == 'BTN_TRIGGER_HAPPY1':
            print('LACET +')
            vecteur_commande[5] = 0.4
        elif event.code == 'BTN_TRIGGER_HAPPY2':
            print('LACET -')
            vecteur_commande[5] = -0.4

        #tangage
        elif event.code == 'BTN_WEST':
            print('TANGAGE +')
            vecteur_commande[4] = 0.4
        elif event.code == 'BTN_SOUTH':
            print('TANGAGE -')
            vecteur_commande[4] = -0.4

        #roulis
        elif event.code == 'BTN_EAST':
            print('ROULIS -')
            vecteur_commande[3] = -0.4
        elif event.code == 'BTN_NORTH':
            print('ROULIS +')
            vecteur_commande[3] = 0.4

        #Selon Z
        elif event.code == 'BTN_TL':
            print('-Z')
            vecteur_commande[2] = -0.4
        elif event.code == 'BTN_TR':
            print('+Z')
            vecteur_commande[2] = 0.4

        # Eteinte du ROV
        elif event.code == 'BTN_SELECT' :
            print('SHUTDOWN')
            quit()
    return vecteur_commande


'''
# ---------------------------- GESTION ROS ----------------------------

def Gamepad_Publisher():

     #define a topic to which the messages will be published
     vect_publisher = rospy.Publisher("commande_envoyee", Float64MultiArray, queue_size=100) #message topic

     #initialize the Publisher node.
     rospy.init_node("mod_geom_suscriber", anonymous=True) #Setting anonymous=True will append random integers at the end of our publisher node

     #publishes at a rate of 2 messages per second
     rate = rospy.Rate(10)
     iteration = 1
     #Keep publishing the messages until the user interrupts
     while not rospy.is_shutdown():

         vect = Float64MultiArray() #fichier type message envoyé
         #commande_envoyee = vectorization_info_recue( vecteur_commande )
         commande_envoyee = vecteur_commande
         vect.data = commande_envoyee #fonction qui retourne un vecteur 6*1 tq translation x y z rotation x y z

         rospy.loginfo("iteration")
         rospy.loginfo(iteration)
         rospy.loginfo("\n")
         rospy.loginfo("Published: ") #display the message on the terminal

         rospy.loginfo(vect) # peut pas concatener string et float
         vect_publisher.publish(vect)    #publish the message to the topic
         rospy.loginfo("\n-------------------------\n")

         #rate.sleep() will wait enough until the node publishes the message to the topic
         iteration = iteration +1


         ABS_X = 0
         ABS_Lacet = 0
         ABS_Tanguage = 0
         ABS_Roulis = 0

         vect = np.array([ABS_X, 0.0, 0.0, ABS_Roulis, ABS_Tanguage, ABS_Lacet])

         rate.sleep()


if __name__ == "__main__":
     try:
         Gamepad_Publisher()
     #capture the Interrupt signals
     except rospy.ROSInterruptException:
         pass
