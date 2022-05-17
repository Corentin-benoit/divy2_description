# Node des moteurs
# Reçoit les paramètres articulaires du MGI et les convertit en force de poussé

import rospy
from std_msgs.msg import String 
from std_msgs.msg import Float64MultiArray
from std_msgs.msg import Float64
from std_msgs.msg import MultiArrayDimension
import time
import numpy as np
from board import SCL, SDA
import busio

# Import the PCA9685 module.
import Adafruit_PCA9685

# Create the I2C bus interface.
#i2c_bus = busio.I2C(SCL, SDA)

# Create a simple PCA9685 class instance.
pwm = Adafruit_PCA9685.PCA9685()


#------------------- VARIABLES GLOBALES--------------------

mat_param_arti = None

# ---------------------------- GESTION ROS ----------------------------


#Callback function to print the subscribed data on the terminal
def matrice_callback(message): 
     # Each subscriber gets 1 callback, and the callback either stores information and/or computes something and/or publishes It _does not!_ return anything
     global mat_param_arti
     rospy.loginfo("Subscribed:")
     rospy.loginfo(message.data)
     mat_param_arti = message.data
     print("\n----------------------\n")
     print("Data reçue et stoquée dans la matrice mat_param_articulaire \n")
     print(mat_param_arti)


#écoute
def messageSubscriber():
     #initialize the subscriber node called 'messageSubNode'
     rospy.init_node("messageSubNode", anonymous=False)    
     #This is to subscribe to the messages from the topic named 'messageTopic'
     rospy.Subscriber("param_articulaire", Float64MultiArray, matrice_callback)    
     #rospy.spin() stops the node from exitind until the node has been shut down
     rospy.spin()

if __name__ == "__main__":
    try:
         messageSubscriber()
    except rospy.ROSInterruptException:
         pass


# ---------------------------- GESTION MOTEURS ----------------------------

# Set the pulse length given in microsec
#Calculs à vérifier
def set_thruster_pulse(channel, pulse_microsec):
     cycle_length = 1000000.0    # 1,000,000 us per second
     cycle_length /= frequency
     time_per_tick = cycle_length / 4096.0     # 12 bits of resolution -> Time per clock tick
     pulse_ticks = int(pulse_microsec / time_per_tick)
     pwm.set_pwm(channel, 0, pulse_ticks)
     print("Setting pwm on channel" , channel, "with pulse from 0 to",pulse_microsec,"(",pulse_ticks,"ticks)")


# Set frequencyset_pwm library adafruit
def set_frequency(freq):
     frequency = freq
     pwm.set_pwm_freq = frequency


# Reset thrusters to 0 and wait 1 sec
def reset_thrusters():
    for channel in channels:
         set_thruster_pulse(channel,thruster_neutral)
         #vars[channel].set(0)
    window.update()
    time.sleep(1)


# Convert percentage into thrust force
def set_thrusters(mat_param_arti):
     vars_int = np.array([var1.get(),var2.get(),var3.get(),var4.get(),var5.get(),var6.get()])
     for channel in channels:

          if mat_param_arti[i]==0.0 :
               pulse =0.0
          else :
               pulse = thruster_neutral + 800 * mat_param_arti[i]

          set_thruster_pulse(channel, pulse)



if __name__ == "__main__":

    # Configure thruster neutral (min = 1100, 1900= max)
    thruster_neutral = 1500

     # All channels used
    channels = [0,1,2,3,4,5]

     # Frequency of command, default : 100 Hz
    frequency = 100
    set_frequency(frequency)

     # ESCs initialization
    reset_thrusters()

    while True:
         set_thrusters(mat_param_arti)
