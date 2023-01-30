#!/usr/bin/env python
# coding: utf-8

# In[1]:


import matplotlib.pyplot as plt
import numpy as np
import math

#creat the coefficient of friction tabel with the provided data
coefficient_of_friction = {
    ("rubber", "concrete", "dry"): 0.5,
    ("rubber", "concrete", "wet"): 0.35,
    ("rubber", "ice", "dry"): 0.15,
    ("rubber", "ice", "wet"): 0.08,
    ("rubber", "water", "aquaplaning"): 0.05,
    ("rubber", "gravel", "dry"): 0.35,
    ("rubber", "sand", "dry"): 0.3,
}


# In[2]:


"""THE while true loop is used for one reasone. This is to make sure that the user has inserted the correct inputs before
the code is executed to make sure the user has provided required information to calculate the """
while True:
   
    #inputs from the user reagrding the coefficient of friction 
    Wheel = input("Insert the type of wheel (Rubber): ")
    Road = input("Insert the type of the road (Concrete/Ice/Water/Gravel/Sand): ")
    Condition = input("Insert the condition of the road(Dry/Wet/Aquaplaning): ")
    
    '''the following statements makes sure that the input is all in lowercase to ensures to that 
    there are no mistakes in case the user inserts something in uppercase'''
    Wheel = Wheel.lower()
    Road = Road.lower()
    Condition = Condition.lower()
    
    # Look up coefficient of friction based on user input
    coefficient = coefficient_of_friction.get((Wheel, Road, Condition))

    # Print the result and prompt for new input if not found
    if coefficient:
        print("The coefficient of friction is:", coefficient)
        break
    else:
        print("No coefficient of friction found for the given inputs")
    
    #take input from user to check of the coeff will be entered manually or not
    Manual = input("Coefficient of friction manually entered? enter (yes/no): ")
    Manual = Manual.lower()
    if Manual=="yes":
        coefficient=float(input("Insert the coefficient of friction: "))
        break


# In[3]:


#Now we should take the reset of the inputs from user that will be used to calcuate the breaking distance and time

speed = float(input("Insert the car speed in Km/h: "))
#this is to convert the velocity from km/h to m/s
speed = speed * 0.277778

mass = float(input("Insert the mass of the car in Kg: "))
inclination = float(input("Insert the angle of inclination of the road (degrees): "))
inclination = math.radians(inclination)

#declaration of the gravity 
g= float(9.8)


# In[4]:


print(coefficient)
print(speed)
print(inclination)
print(mass)
print(g)


# In[5]:


from math import cos
#The breaking distance is calculated as follows: BD=(v0**2)/(2*coeff*g*cos(theta))

#we will create a function that calculates the breaking distance based on the velocity, inclination, and friction

Breaking_distance = (speed**2) / (2 * g * coefficient * cos(inclination))

# Breaking distance
print("Breaking distance:", Breaking_distance, "meters")


# In[6]:


#now we will plot the braking distance as a function of the velocity
import matplotlib.pyplot as plt
import numpy as np

#creating the range of the velocity (x-axis). the values of the velocity are in m/s
#the variables are created in a list from 0 to 100 and the range is divided into 100 steps
v = np.linspace(0, 100, 100) 

#creating the function in which the velocity will be substituted
BD = (v**2) / (2 * g * coefficient * cos(inclination))

#creating the plot
plt.plot(v, BD, "-b")

plt.legend(["Fixed Variables: \nAngle={} \nMass={} \nFriction coefficient={}".format(inclination, mass, coefficient)], loc='upper left')

#creating axes labels
plt.xlabel("Velocity (m/s)")
plt.ylabel("Breaking Distance (m)")

# title of the plot
plt.title("Breaking Distance Vs Velocity")

plt.show()


# In[7]:


'''The next step after calculating the breaking distance is calculating the breaking time.
The function used to detrmine the breaking time is from the law of motion where: 𝑠 = 𝑠0 + 𝑣∗𝑡 + (1/2∗𝑎∗𝑡^2).
This equation can be solved as  0 = -𝑠 + 𝑣∗𝑡 + ((𝑎∗𝑡^2)/2)'''

import math
import matplotlib.pyplot as plt

#declaration of the function that solves the quadratic equation and gets the roots
def quad_equ(a, b, c):
    #calculating the discriminant
    d = math.sqrt(b**2 - 4*a*c)
    #calculating the two roots
    root1 = (-b + d) / (2 * a)
    root2 = (-b - d) / (2 * a)
    
    #create an if condition to return the positive root since the correct solution is positive as we dealing with time
    if root1 >0:
        print("Breaking time in sec is: ",root1)
        return (root1)
    elif root2 >0:
        print("Breaking time in sec is: ",root2)
        return (root2)
    else:
        print("No correct solution")
        return (root1,root2)

def plot(a, b, c):
    roots = quad_equ(a, b, c)
    t = range(0,10)
    y = [a*i**2 + b*i + c for i in t]
    plt.plot(t, y)
    plt.xlabel("Time (sec)")
    plt.title("0 = {}t^2 + {}t + {}".format(a,b,c))
    
    #creat grid and draw line on (0,0) in x and y axes
    plt.grid()
    plt.axhline()
    plt.axvline()
    
    #mark the root
    plt.plot(roots, 0, 'go', markersize=10)
    
    plt.show()

plot((coefficient*g/2), speed, -Breaking_distance)


# In[8]:


"""Finally, we want to creat a graphical representation of the distance covered in relation to the time. In addition,
we want to illustrate the velocity of the car as time passes while breaking. This will be implemented by making to arrays
as we know the intial and end value of the velocity, distance, and time from the previous equations"""
import matplotlib.pyplot as plt
import numpy as np

# Create a list of time values in seconds
speed_interval = np.linspace(speed, 0, 100)

# Create a list of time values in seconds
distance_interval = np.linspace(0, Breaking_distance, 100)

# Create a list of time values in seconds
time_interval = np.linspace(0, quad_equ((coefficient*g/2), speed, -Breaking_distance), 100)

# Create a plot of distance vs time
plt.plot(time_interval, distance_interval, "r")
plt.xlabel('Time (s)')
plt.ylabel('Breaking Distance (m)')
plt.title('Breaking Distance vs Time')

# Create a second plot of velocity vs time
plt.figure()
plt.plot(time_interval, speed_interval,"b")
plt.xlabel('Time (s)')
plt.ylabel('Velocity (m/s)')
plt.title('Velocity vs Time')

#create new figure to show both graphs together
plt.figure()

plt.plot(time_interval, speed_interval, 'b', label="Speed")
plt.plot(time_interval, distance_interval, 'r', label="Breaking Distance")

plt.title('Breaking Distance & Velocity vs Time')

plt.xlabel('Time (s)')
plt.ylabel('Velocity (m/s) \nBreaking Distance (m)')

plt.legend()
plt.show()


# Here we are going to plot the equations for the rule of Thumb. 
# Each plot will be for the following rule:
# 1) S normal
# 2) S danger
# 3) S reaction

# In[12]:


# Define the variables and the range for each
v = np.linspace(0, 100, 1000)
s_normal = ((v/10)**2)

# Plot the equation
plt.plot(v, s_normal)

# Add labels to the x and y axes
plt.xlabel('Velocity (m/s)')
plt.ylabel('Displacement (m)')

# Add a title to the plot
plt.title('S normal vs Velocity')

# Show the plot
plt.show()


# In[13]:


# Define the variables and the range for each
v = np.linspace(0, 100, 1000)
s_danger = (((v/10)**2)/2)

# Plot the equation
plt.plot(v, s_danger)

# Add labels to the x and y axes
plt.xlabel('Velocity (m/s)')
plt.ylabel('Displacement (m)')

# Add a title to the plot
plt.title('S danger vs Velocity')

# Show the plot
plt.show()


# In[15]:


# Define the variables and the range for each
v = np.linspace(0, 100, 1000)
s_reaction = ((v/10)*3)

# Plot the equation

plt.plot(v, s_danger)
plt.plot(v, s_reaction)


# Add labels to the x and y axes
plt.xlabel('Velocity (m/s)')
plt.ylabel('Displacement (m)')

# Add a title to the plot
plt.title('S reaction vs Velocity')

# Show the plot
plt.show()


# In[23]:


'''Here we will combine the three plots into one plot for bttter understanding'''
# Plot the equation
plt.plot(v, s_normal, label='S normal')
plt.plot(v, s_danger, label="S danger")
plt.plot(v3, s_reaction, label="S reaction")

# Add labels to the x and y axes
plt.xlabel('Velocity (m/s)')
plt.ylabel('Displacement (m)')

# Add a title and the legends to the plot
plt.title('S reaction vs Velocity')
plt.legend()

# Show the plot
plt.show()


# In[ ]:




