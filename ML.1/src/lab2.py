'''
Created on Sep 29, 2011

@author: jfn
'''
#!/usr/bin/env python
from cvxopt.solvers import qp
from cvxopt.base import matrix
import numpy as np,pylab,random, math
from numpy import linalg

def linear_kernel(x, y):
    k=0
    for i in range(len(x)):
        k+=(x[i]*y[i])
    return k+1

def polynomial_kernel(x, y, p=3):
    k=0
    for i in range(len(x)):
        k=k+(x[i]*y[i])
    return pow((k+1),p)    

def gaussian_kernel(x, y, sigma=2.0,a=0):
    sigma=2
    for i in range(len(x)):
        a=a+(x[i]-y[i])*(x[i]-y[i])
    k=np.exp(-a/(2*sigma*sigma))
    return k

def sigmoid_kernel(x, y, b=0.05, delta=-0.05):
    c=0
    for i in range(len(x)):
        c=c+(b*x[i]*y[i])
    k=math.tanh(c-delta)
    return k    

def ind(alpha,point):
    X2 = 0
    for i in range(0,len(alpha)):
        X2 = X2 + (alpha[i][0] * alpha[i][1][2] * linear_kernel(point,(alpha[i][1][0],alpha[i][1][1])))
    return X2

classA = [(random.normalvariate(-1.5, 1),
           random.normalvariate(0.5, 1),
           1.0)
          for i in range(5)] + \
         [(random.normalvariate(1.5, 1),
           random.normalvariate(0.5, 1),
           1.0)
          for i in range(5)]

classB = [(random.normalvariate(0.0, 0.5),
          random.normalvariate(-0.5, 0.5),
          -1.0)
          for i in range(10)]

#classA = [(-3,3,1),(-3,2,1),(-2,3,1),(-2,2,1)]
#classB = [(3,-3,-1),(3,-2,-1),(2,-3,-1),(2,-2,-1)]
data = classA + classB
random.shuffle(data)
size = len(data)

pylab.hold(True)
pylab.plot([p[0] for p in classA],
           [p[1] for p in classA],
           'bo')
pylab.plot([p[0] for p in classB],
           [p[1] for p in classB],
           'ro')

P = np.ones(shape=(size,size)) # P[i][j] = K(x[i],x[j])
#G = np.zeros(shape=(size,size)) # 1 in diagonal and 0 in the rest
#h = np.zeros(shape=(size,1)) ## all 0
#q = np.ones(shape=(size,1)) # all -1

Q=-1.0*matrix(1.0, (size,1),'d')
G = matrix(0.0, (size,size),'d')
G[::size+1] = -1.0
H = matrix(0.0, (size,1),'d')


#for i in xrange(len(q)):
#    q[i] = q[i] * -1
#
#for i in range(0,size):
#    for j in range(0,size):
#        if(i == j):
#            G[i][j] = 1
            
for i in range(0,size):
    for j in range(0,size):
        kernel = linear_kernel(data[i][0:2],data[j][0:2])
        P[i][j] = (data[i][2] * data[j][2] * kernel)
    
P=matrix(P, (size,size),'d')
   
r = qp(P, Q, G, H)
alpha = list (r['x'])

C = list()
for i in range(len(alpha)):
    if  alpha[i] >= 1e-5:
        C.append((alpha[i],data[i]))

print alpha
xrange = np.arange(-4,4,0.05)
yrange = np.arange(-4,4,0.05) 

grid = matrix([[ind(C,(x,y))
                for x in yrange]
               for y in xrange])   
pylab.hold(True)
pylab.contour(xrange, yrange, grid,
              (-1.0, 0.0, 1.0),
              colors = ('red', 'black', 'blue'),
              linewidths = (1, 3, 1))
pylab.show()