from MDPenvironment import *


def prob_sa(s_curr,s_given,action,pe):
	'''
	the inputs of this function are current state, given next state, action
	current state is the state where robot is in right now
	given next state is the state where we want the robot to move into
	action is the chosen for moving the robot into our desired next state
	pe is the error rate specified by this problem.

	The output of this function is the state transition probability given an action
	'''
	if abs(s_curr.x-s_given.x)>1 or abs(s_curr.y-s_given.y)>1:
		return 0
	elif s_given.x==s_curr.x and s_given.y==s_curr.y and s_given.h==s_curr.h and action==0:
		return 1
	elif s_given.x==s_curr.x and s_given.y==s_curr.y and s_given.h==s_curr.h and abs(action)>1:
		return pe
	elif s_given.x==s_curr.x and s_given.y==s_curr.y and s_given.h==s_curr.h and abs(action)==1:
		return 1-2*pe
	elif s_given.x==s_curr.x and s_given.y==s_curr.y and (abs(s_given.h-s_curr.h)==1 or abs(s_given.h-s_curr.h)==11) and abs(action)==1:
		return pe
	elif s_given.x==s_curr.x and s_given.y==s_curr.y and (abs(s_given.h-s_curr.h)==1 or abs(s_given.h-s_curr.h)==11) and abs(action)>1:
		return 1-2*pe
	elif s_given.x==s_curr.x and s_given.y==s_curr.y and (abs(s_given.h-s_curr.h)==2 or abs(s_given.h-s_curr.h)==10) and abs(action)>1:
		return pe
	elif s_given.x<0 or s_given.x>5 or s_given.y<0 or s_given.y>5:
		return 0
	elif (abs(s_curr.h-s_given.h)==2 or abs(s_curr.h-s_given.h)==10) and (abs(action)>1):
		return pe
	elif (abs(s_curr.h-s_given.h)==1 or abs(s_curr.h-s_given.h)==11) and abs(action)==1:#linear no turn
		return pe
	elif (abs(s_curr.h-s_given.h)==1 or abs(s_curr.h-s_given.h)==11) and abs(action)>1:#linear with rotation
		return 1-2*pe
	elif abs(s_curr.h-s_given.h)==0 and abs(action)==1:
		return 1-2*pe
	elif abs(s_curr.h-s_given.h)==0 and abs(action)>1:
		return pe
	else:
		return 0

def h_judge(h_temp):
	# mod 12
	if h_temp==-1:
		return 11
	elif h_temp==12:
		return 0
	else:
		return h_temp


def next_state(s_curr,action,pe):
	'''
	the input of this function is current state, action and pe
	the output of this function is the next state
	'''
	s_next=State(0,0,0) 
	pe_1=pe

	if action==0:
		s_next=s_curr
		return s_next
	else:
		judge_prob=random.random()
		if judge_prob<pe:#left-pre-error
			h_temp=s_curr.h-1
			h_temp=h_judge(h_temp)
		elif judge_prob>1-pe:#right-pre-error
			h_temp=s_curr.h+1
			h_temp=h_judge(h_temp)           
		else: #no prerotation error
			h_temp=s_curr.h

	if h_temp==0 or h_temp==1 or h_temp==11:
		if action>0:#forwards
			s_next.x=s_curr.x-1
			s_next.y=s_curr.y
			if action==1:
				s_next.h=h_temp
			elif action==2:#for left
				s_next.h=h_temp-1
			elif action==3:
				s_next.h=h_temp+1
		elif action<0:#backwards
			s_next.x=s_curr.x+1
			s_next.y=s_curr.y
			if action==-1:
				s_next.h=h_temp
			elif action==-2:#back left
				s_next.h=h_temp-1
			elif action==-3:
				s_next.h=h_temp+1
	elif h_temp==2 or h_temp==3 or h_temp==4:
		if action>0:#forwards
			s_next.x=s_curr.x
			s_next.y=s_curr.y+1
			if action==1:
				s_next.h=h_temp
			elif action==2:#for left
				s_next.h=h_temp-1
			elif action==3:
				s_next.h=h_temp+1
		elif action<0:#backwards
			s_next.x=s_curr.x
			s_next.y=s_curr.y-1
			if action==-1:
				s_next.h=h_temp
			elif action==-2:#back left
				s_next.h=h_temp-1
			elif action==-3:
				s_next.h=h_temp+1
	elif h_temp==5 or h_temp==6 or h_temp==7:
		if action>0:#forwards
			s_next.x=s_curr.x+1
			s_next.y=s_curr.y
			if action==1:
				s_next.h=h_temp
			elif action==2:#for left
				s_next.h=h_temp-1
			elif action==3:
				s_next.h=h_temp+1
		elif action<0:#backwards
			s_next.x=s_curr.x-1
			s_next.y=s_curr.y
			if action==-1:
				s_next.h=h_temp
			elif action==-2:#back left
				s_next.h=h_temp-1
			elif action==-3:
				s_next.h=h_temp+1  
	elif h_temp==8 or h_temp==9 or h_temp==10:
		if action>0:#forwards
			s_next.x=s_curr.x
			s_next.y=s_curr.y-1
			if action==1:
				s_next.h=h_temp
			elif action==2:#for left
				s_next.h=h_temp-1
			elif action==3:
				s_next.h=h_temp+1
		elif action<0:#backwards
			s_next.x=s_curr.x
			s_next.y=s_curr.y+1
			if action==-1:
				s_next.h=h_temp
			elif action==-2:#back left
				s_next.h=h_temp-1
			elif action==-3:
				s_next.h=h_temp+1     

	#judge if s_next out of the grid world
	if s_next.x<0 or s_next.x>5 or s_next.y<0 or s_next.y>5:
		s_next.x=s_curr.x
		s_next.y=s_curr.y

	s_next.h=h_judge(s_next.h)

	return s_next


	print(s_next.x)
	print(s_next.y)
	print('----------------')
		
	judge_psa=random.random()
	if judge_psa<=prob_sa(s_curr,s_next,action,pe_1):
		return s_next
	elif judge_psa>prob_sa(s_curr,s_next,action,pe_1):
		return s_curr

def get_reward(s_curr):
	reward=state_space[s_curr.x,s_curr.y,1]
	return reward

def policylibrary_generator():
	# policy initialization

	# h=0
	for i in range(6):
		for j in range(6):
			if i==0:
				policylibrary[i,j,0]=-3
			if i==0 and j==3:
				policylibrary[i,j,0]=-1
			if i>0 and j<=2:
				policylibrary[i,j,0]=3
			if i>0 and j>3:
				policylibrary[i,j,0]=2
			if i>0 and j==3:
				policylibrary[i,j,0]=1
	
	#h=1
	for i in range(6):
		for j in range(6):
			if i==0:
				policylibrary[i,j,1]=-3
			if i==0 and j==3:
				policylibrary[i,j,1]=-1
			if (i==1 and j!=3) or i>2 or (i==2 and j==3):
				policylibrary[i,j,1]=1
			if i==2 and j!=3:
				policylibrary[i,j,1]=3
	
	#h=2
	for i in range(6):
		for j in range(6):
			if j<4:
				policylibrary[i,j,2]=1
			if j>=4:
				policylibrary[i,j,2]=-1
			if j==2 and i!=1:
				policylibrary[i,j,2]=2
			if j==4 and i!=1:
				policylibrary[i,j,2]=-2
	
	#h=3
	for i in range(6):
		for j in range(6):
			if j<4:
				policylibrary[i,j,3]=3
			if j>=4:
				policylibrary[i,j,3]=-3
			if i==1 and j<3:
				policylibrary[i,j,3]=1
			if i==1 and j>=4:
				policylibrary[i,j,3]=-1

	#h=4
	for i in range(6):
		for j in range(6):
			if j<4:
				policylibrary[i,j,4]=1
			if j>=4:
				policylibrary[i,j,4]=-1
			if j==2 and i!=1:
				policylibrary[i,j,4]=3
			if j==4 and i!=1:
				policylibrary[i,j,4]=-3      

	#h=5
	for i in range(6):
		for j in range(6):
			if i==0:
				policylibrary[i,j,5]=2
			if i==0 and j==3:
				policylibrary[i,j,5]=1
			if (i==1 and j!=3): #or i>2 or (i==2 and j==3):
				policylibrary[i,j,5]=1
			if i>2 or (i==2 and j==3):
				policylibrary[i,j,5]=-1
			if i==2 and j!=3:
				policylibrary[i,j,5]=-2

	#h=6
	for i in range(6):
		for j in range(6):
			if i<2:
				policylibrary[i,j,6]=2
			if i>=2:
				policylibrary[i,j,6]=-2
			if j==3 and i==0:
				policylibrary[i,j,6]=1
			if j==3 and i>1:
				policylibrary[i,j,6]=-1

	#h=7
	for i in range(6):
		for j in range(6):
			if i==0:
				policylibrary[i,j,7]=3
			if i==0 and j==3:
				policylibrary[i,j,7]=1
			if (i==1 and j!=3):
				policylibrary[i,j,7]=1
			if  i>2 or (i==2 and j==3):
				policylibrary[i,j,7]=-1
			if i==2 and j!=3:
				policylibrary[i,j,7]=-3

	#h=8
	for i in range(6):
		for j in range(6):
			if j<3:
				policylibrary[i,j,8]=-1
			if j>=3:
				policylibrary[i,j,8]=1
			if j==2 and i!=1:
				policylibrary[i,j,8]=-2
			if j==4 and i!=1:
				policylibrary[i,j,8]=2
	#h=9
	for i in range(6):
		for j in range(6):
			if j<3:
				policylibrary[i,j,9]=-2
			if j>=3:
				policylibrary[i,j,9]=2
			if i==1 and j<3:
				policylibrary[i,j,9]=-1                 
			if i==1 and j>3:
				policylibrary[i,j,9]=1
	
	#h=10
	for i in range(6):
		for j in range(6):
			if j<3:
				policylibrary[i,j,10]=-1
			if j>=3:
				policylibrary[i,j,10]=1
			if j==2 and i!=1:
				policylibrary[i,j,10]=-3
			if j==4 and i!=1:
				policylibrary[i,j,10]=3 
	
	#h=11
	for i in range(6):
		for j in range(6):
			if i==0:
				policylibrary[i,j,11]=-2
			if i==0 and j==3:
				policylibrary[i,j,11]=-1
			if (i==1 and j!=3):
				policylibrary[i,j,11]=1
			if i>2 or (i==2 and j==3):
				policylibrary[i,j,11]=1
			if i==2 and j!=3:
				policylibrary[i,j,11]=2

	for h in range(12):
		policylibrary[1,3,h]=0