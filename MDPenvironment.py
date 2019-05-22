import random as random
import numpy as np
import matplotlib.pyplot as plt
import time
import copy


NO_MOTION = 0
FORWARDS = 1
BACKWARDS = -1
FORWARDS_LEFT = 2
FORWARDS_RIGHT = 3
BACKWARDS_LEFT = -2
BACKWARDS_RIGHT = -3

#Here we define the action set and assign numbers for each action for easier operation
action_set=[NO_MOTION,FORWARDS,BACKWARDS,FORWARDS_LEFT,FORWARDS_RIGHT,BACKWARDS_LEFT,BACKWARDS_RIGHT]

#error probability
pe=0.25

# create the state space the dimension of the state space is 6*6*12
state_space=np.zeros((6,6,12))

#create a policy library for policy initialization and updating
policylibrary=np.zeros((6,6,12))

#according to the given rewards, assign rewards for each grid
state_space[0:6,0,:]=-100
state_space[0:6,5,:]=-100
state_space[0,0:6,:]=-100
state_space[5,0:6,:]=-100
state_space[1:4,2,:]=-10
state_space[1:4,4,:]=-10
state_space[1,3,:]=0
state_space[1,3,4:7]=1

# Create a class State
class State:
    x=0
    y=0
    h=0

    def __init__(self,x_,y_,h_):
        self.x=x_
        self.y=y_
        self.h=h_