import numpy as np
import pylab
import random

class Environment:
    def __init__(self ,state=0):
        self.state = state
        self.trans = ((1,3,4,12),
                      (0,2,5,13),
                      (3,1,6,14),
                      (2,0,7,15),
                      (5,7,0,8),
                      (4,6,1,9),
                      (7,5,2,10),
                      (6,4,3,11),
                      (9,11,12,4),
                      (8,10,13,5),
                      (11,9,14,6),
                      (10,8,15,7),
                      (13,15,8,0),
                      (12,14,9,1),
                      (15,13,10,2),
                      (14,12,11,3))
        self.rew = ((1,0,0,0),
                    (0,1,0,0),
                    (1,0,0,0),
                    (0,0,1,0),
                    (0,0,0,1),
                    (1,0,1,0),
                    (1,0,1,0),
                    (0,0,0,1), 
                    (0,0,1,0),
                    (1,0,1,0),
                    (1,0,1,0),
                    (0,1,0,0), 
                    (1,0,0,0),
                    (0,1,0,0),
                    (0,0,0,1),
                    (0,1,0,1));
        
    def go(self,a):
        r = self.rew[self.state][a]
        self.state = self.trans[self.state][a]
        return self.state, r
    
actions = [(0,"MoveRightHorizontal"),(1,"MoveRightVertical"),(2,"MoveLeftHorizontal"),(3,"MoveLeftVertical")]
states = [(0,"RBD-LBD"),(1,"RBU-LBD"),(2,"RFU-LBD"),(3,"RFD-LBD"),(4,"RBD-LBU"),(5,"RBU-LBU"),(6,"RFU-LBU"),
          (7,"RBD-LFU"),(8,"RBU-LFU"),(9,"RFU-LFU"),(10,"RFD-LFU"),(11,"RBD-LFD"),(12,"RBU-LFD"),(13,"RFU-LFD"),
          (14,"RFD-LFD")]

policy = np.zeros((16,),dtype=np.int)
value = np.zeros((16,),dtype=np.int)
Ql = np.zeros((16,4),dtype=np.int)
gamma = 0.9
epsilon = 10
#rew = ((1,0,1,0)
#       (0,1,0,0)
#       (1,0,0,0)
#       (0,0,1,0)
#       (0,0,0,1)
#       (1,0,1,0)
#       (1,0,0,0)
#       (0,0,0,1)
#       (0,0,1,0)
#       (0,0,1,0)
#       (1,0,1,0)
#       (0,0,0,1)
#       (1,0,0,0)
#       (0,1,0,0)
#       (0,1,0,0)
#       (1,0,1,0))

#rew = ((0,-1,0,-1),
#       (-1,1,-1,-1),
#       (0,-1,-1,-1),
#       (-1,-1,1,-1),
#       (-1,-1,-1,1),
#       (0,-1,0,-1),
#       (0,-1,-1,-1),
#       (-1,-1,-1,1),
#       (-1,-1,0,-1),
#       (-1,-1,0,-1),
#       (0,-1,0,-1),
#       (-1,-1,-1,1),
#       (0,-1,-1,-1),
#       (-1,1,-1,0),
#       (0,-1,-1,-1),
#       (1,-1,1,-1))

rew = ((0,0,0,0),
       (0,0,0,0),
       (1,0,0,0),
       (0,0,1,0),
       (0,0,0,0),
       (0,0,0,0),
       (0,0,0,0),
       (0,0,0,1), 
       (0,0,1,0),
       (0,0,0,0),
       (0,0,0,0),
       (0,1,0,0), 
       (1,0,0,0),
       (0,1,0,0),
       (0,0,0,1),
       (0,0,0,0));

#rew = ((0,0,0,0),
#       (0,0,0,0),
#       (0,-1,0,0),
#       (0,0,1,0),
#       (0,0,0,0),
#       (0,0,0,0),
#       (0,0,0,0),
#       (-1,-1,-1,0),
#       (0,0,0,-1),
#       (0,0,0,0),
#       (0,0,0,0),
#       (0,0,0,-1),
#       (1,0,0,0),
#       (-1,0,-1,-1),
#       (-1,-1,0,0),
#       (0,0,0,0))
  
trans = ((1,3,4,12),
         (0,2,5,13),
         (3,1,6,14),
         (2,0,7,15),
         (5,7,0,8),
         (4,6,1,9),
         (7,5,2,10),
         (6,4,3,11),
         (9,11,12,4),
         (8,10,13,5),
         (11,9,14,6),
         (10,8,15,7),
         (13,15,8,0),
         (12,14,9,1),
         (15,13,10,2),
         (14,12,11,3))


def argmax(f, args):
    mi = None
    m = -1e10
    for i in args:
        v = f(i)
        if v > m:
            m = v
            mi = i
    return mi

def policyIteration(iterations,gamma):
    for p in range(iterations):
        for s in range(len(policy)):
            policy[s] = argmax(
                lambda(a):
                    rew[s][a] + gamma * value[trans[s][a]],
                range(4))
            
        for s in range(len(value)):
            a = policy[s]
            value[s] = rew[s][a] + gamma * value[trans[s][a]]   
            

def maxa(Ql,state):
    maxv = 0
    maxi = 0
    for i in range(len(Ql[state])):
        if (Ql[state][i] > maxv):
            maxv = Ql[state][i]
            maxi = i
    return maxi
 
def Q(iterations,init,gamma,epsilon,n):
    s = init
    a = 0
    r = 0
    next_state = 0
    e = Environment(s)
    for i in range(iterations):
        a = maxa(Ql,s)
        if(random.random() < epsilon):
            indices = [x!=0 for x in trans[s]]
            a = np.random.randint(0,len(indices))
        else:
            a = maxa(Ql,s)
            
        next_state,r = e.go(a)
        next_action = maxa(Ql,next_state)
        Ql[s][a] = Ql[s][a] + (n * (r + gamma*Ql[next_state][next_action] - Ql[s][a]))
        s = next_state
        

def drawImage(test):
    images = (pylab.imread('step1.png'),
              pylab.imread('step2.png'),
              pylab.imread('step3.png'),
              pylab.imread('step4.png'),
              pylab.imread('step5.png'),
              pylab.imread('step6.png'),
              pylab.imread('step7.png'),
              pylab.imread('step8.png'),
              pylab.imread('step9.png'),
              pylab.imread('step10.png'),
              pylab.imread('step11.png'),
              pylab.imread('step12.png'),
              pylab.imread('step13.png'),
              pylab.imread('step14.png'),
              pylab.imread('step15.png'),
              pylab.imread('step16.png'))

    comic = np.concatenate([images[i] for i in test], axis=1)

    pylab.imshow(comic)
    pylab.show()   

policyIteration(100,gamma)
Q(10000,0,gamma,epsilon,1)
print Ql 
start = 0
walk_steps = 25
stages = np.zeros((walk_steps),dtype=np.int)
stagesq = np.zeros((walk_steps),dtype=np.int)
stages[0] = start;
stagesq[0] = start;

for i in range(start+1,walk_steps):
    s = stages[i-1]
    a = policy[s]
    stages[i] = trans[s][a]
    
    sq = stagesq[i-1]
    aq = maxa(Ql,sq)
    print sq
    print aq
    stagesq[i] = trans[sq][aq]
    
drawImage(stages)