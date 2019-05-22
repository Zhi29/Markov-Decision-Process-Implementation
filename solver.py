from envdynamic import *


def policy_evaluation(policy,discount):
    ValueMat=copy.deepcopy(state_space)
    ValueMat_prev=copy.deepcopy(state_space)
    loop=True
    numberofiteration=0
    while(loop):
        numberofiteration+=1
        maxNorm=0
        for k in range(12):
            for i in range(6):
                for j in range(6):
                    s_ind = State(i,j,k)
                    action_ = policy[i,j,k]
                    #sum prob*V_next
                    s_ind_next=next_state(s_ind, action_, 0)
                    temp_prob=prob_sa(s_ind, s_ind_next, action_, pe)
                    ValueMat[s_ind.x,s_ind.y,s_ind.h]=(state_space[s_ind.x,s_ind.y,s_ind.h]+discount*temp_prob*ValueMat[s_ind_next.x,s_ind_next.y,s_ind_next.h])*discount
                    maxNorm=max(maxNorm,abs(ValueMat[s_ind.x,s_ind.y,s_ind.h]-ValueMat_prev[s_ind.x,s_ind.y,s_ind.h]))
                    ValueMat_prev=copy.deepcopy(ValueMat)
        if maxNorm<=1:
            loop=False
        elif numberofiteration>=50:
            loop=False
    print(numberofiteration)
    return ValueMat

def policy_iteration(policylibrary,discount):
    loop=True
    numberofiteration=0
    policy=copy.deepcopy(policylibrary)
    while(loop):
        numberofiteration+=1
        Values_=policy_evaluation(policy,discount)
        changesPolicy=False
        for k in range(12):
            for i in range(6):
                for j in range(6):
                    newMax=None
                    argMax=None
                    s_ind_ = State(i,j,k)
                    for a in action_set:
                        summ=0
                        s_ind_next_ = next_state(s_ind_, a, 0)
                        temp_prob=prob_sa(s_ind_,s_ind_next_,a,pe)
                        summ+=temp_prob*Values_[s_ind_next_.x,s_ind_next_.y,s_ind_next_.h]
                        if (newMax is None) or (summ>newMax):
                            argMax = a
                            newMax = summ
                    summ=0

                    ac=policy[s_ind_.x,s_ind_.y,s_ind_.h]
                    s_ind_next_1 = next_state(s_ind_,ac, 0)
                    temp_prob_=prob_sa(s_ind_,s_ind_next_1,ac,pe)
                    summ+=temp_prob_*Values_[s_ind_next_1.x,s_ind_next_1.y,s_ind_next_1.h]
                    if newMax>summ:
                        policy[s_ind_.x,s_ind_.y,s_ind_.h]=argMax
                        changesPolicy=True

        loop=changesPolicy
        if numberofiteration>50:
            loop=False
    return policy

def value_iteration(discount):
    loop=True
    numberofiteration=0
    Values_vi=np.zeros((6,6,12))
    while(loop):
        numberofiteration+=1
        maxNorm=0
        for k in range(12):
            for i in range(6):
                for j in range(6):
                    s_now=State(i,j,k)
                    v=cell_values(s_now,discount,Values_vi)
                    if not v is None:
                        maxNorm=max(maxNorm,abs(v-Values_vi[s_now.x,s_now.y,s_now.h]))
                    Values_vi[s_now.x,s_now.y,s_now.h]=v
        if maxNorm<0.1:
            loop=False
        elif numberofiteration>100:
            loop=False
        print(Values_vi[:,:,6])
    policy_vi=getpolicy(Values_vi)
    return policy_vi

def cell_values(s_now,discount,Values_vi):
    max_sum=None
    for act in action_set:
        summ=0
        s_now_next = next_state(s_now, act, 0)
        temp_prob=prob_sa(s_now,s_now_next,act,pe)
        summ+=temp_prob*Values_vi[s_now_next.x,s_now_next.y,s_now_next.h]
        if (max_sum is None) or (summ>max_sum):
            max_sum = summ
    res=state_space[s_now.x,s_now.y,s_now.h]+discount*max_sum
    return res

def getpolicy(Values_vi):
    policy_vi=copy.deepcopy(policylibrary)
    for k in range(12):
        for i in range(6):
            for j in range(6):
                newMax=None
                argMax=None
                s_now_=State(i,j,k)
                for act in action_set:
                    summ=0
                    s_now_next_=next_state(s_now_,act,0)
                    temp_prob=prob_sa(s_now_,s_now_next_,act,pe)
                    summ+=temp_prob*Values_vi[s_now_next_.x,s_now_next_.y,s_now_next_.h]
                    if (newMax is None) or (summ>newMax):
                        newMax = summ
                        argMax = act
                policy_vi[s_now_.x,s_now_.y,s_now_.h]=argMax
    return policy_vi


def print3ctrajectoryvalue(s_0):
    traj=trajectory(policylibrary,s_0,0)
    discount=0.9
    Values=policy_evaluation(policylibrary,discount)
    for i in range(len(traj)):
        print(Values[traj[i].x,traj[i].y,traj[i].h])
        print('--------------------------')

def trajectory(policylibrary,s_0,pe):#generate and plot trajectory
    state_list=[]
    state_list.append(s_0)
    s_temp=s_0
    count=0
    loop=True
    while(loop):
        s_temp=next_state(s_temp,policylibrary[s_temp.x,s_temp.y,s_temp.h],pe)
        state_list.append(s_temp)
        print("state.x is %d" % state_list[count].x)
        print("state.y is %d" % state_list[count].y)
        print("state.h is %d" % state_list[count].h)
        print('----------------')
        count=count+1
        if s_temp.x==1 and s_temp.y==3:
            loop=False
    print("state.x is %d" % state_list[count].x)
    print("state.y is %d" % state_list[count].y)
    print("state.h is %d" % state_list[count].h)
    print('----------------')


    for i in range(len(state_list)):
        if i<len(state_list)-1:
            plt.arrow(state_list[i].y,5-state_list[i].x,(state_list[i+1].y-state_list[i].y),((5-state_list[i+1].x)-(5-state_list[i].x)),width=0.05)
    plt.xlim(0,5)
    plt.ylim(0,5)
    plt.show()
    return state_list

def main():
    policylibrary_generator()
    s_0=State(1,1,6)# start state
    act=policylibrary[s_0.x,s_0.y,s_0.h]
    a=next_state(s_0,act,0)
    discount=0.9
    start=time.time()
    #policy=value_iteration(discount)
    policy=policy_iteration(policylibrary,discount)
    end=time.time()
    print("run time is: " ,(end-start))
    traj=trajectory(policy,s_0,0)



main()

