'''
Created on Sep 29, 2011

@author: jfn
'''
from cvxopt.solvers import qp
from cvxopt.base import matrix
import numpy as np, pylab, random, math
from numpy import linalg

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

data = classA + classB
random.shuffle(data)

pylab.hold(True)
pylab.plot([p[0] for p in classA],
           [p[1] for p in classA],
           'bo')
pylab.plot([p[0] for p in classB],
           [p[1] for p in classB],
           'ro')

def linear_kernel(x1, x2):
    return np.dot(x1, x2)

def polynomial_kernel(x, y, p=2):
    return (1 + np.dot(x, y)) ** p

def gaussian_kernel(x, y, sigma=5.0):
    return  np.exp(-linalg.norm(np.array(x)-np.array(y))**2 / (2 * (sigma ** 2)))

def ind(alpha,X,point):
    X2 = 0
    for i in range(0,len(alpha)):
        X2 = X2 + alpha[i] * X[i][2] * linear_kernel(point,(X[i][0],X[i][1]))
    return X2


     

size = len(data)
P = np.zeros(shape=(size,size)) # P[i][j] = K(x[i],x[j])
G = np.zeros(shape=(size,size)) # 1 in diagonal and 0 in the rest
h = np.zeros(shape=(size,1)) ## all 0
q = np.ones(shape=(size,1)) # all -1
W = np.ones(shape=(1,size))


for i in range(0,len(q)):
    q[i] = q[i] * -1



for i in range(0,size):
    for j in range(0,size):
        if(i == j):
            G[i][j] = 1

            
for i in range(0,size):
    for j in range(0,size):
        P[i][j] = data[i][2] * data[j][2] * linear_kernel((data[i][0],data[i][1]),(data[j][0],data[j][1]))
        


r = qp(matrix(P), matrix(q), matrix(G), matrix(h))
alpha = list (r['x'])

index = 0
C = list()
C2 = list()
for a in alpha:
    if a >= 0.00001 or a <= 0.00001 :
        C.append(a)
        C2.append((data[index][0],data[index][1],data[index][2]))
    index = index + 1

xrange = np.arange(-4, 4, 0.05)
yrange = np.arange(-4, 4, 0.05)

grid = matrix([[ind(C,C2,(x,y))
                for x in yrange]
               for y in xrange])

pylab.hold(True)

pylab.contour(xrange, yrange, grid,
              (-1.0, 0.0, 1.0),
              colors = ('red', 'black', 'blue'),
              linewidths = (1, 3, 1))

pylab.show()