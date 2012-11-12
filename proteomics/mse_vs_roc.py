#! /usr/bin/env python
# @Created by Jose Fernandez

from lxml import etree
import os
import getopt
import sys
from pylab import *
from matplotlib import cm
from matplotlib.mlab import griddata
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import scipy.special as sp
from matplotlib.colors import LinearSegmentedColormap
    
def usage():
    print "this script generates reads a tab delimited file containing the values of the grid search of Percolator for fido and generates useful plots"
    print "Usage : mse_vs_roc.py <input.txt>  [-h, --help] [-v, --verbose]"
    
def main(argv):
    if( len(argv) < 1):
        sys.stderr.write("Error: Number of arguments incorrect\n")
        usage()
        sys.exit()
    else:
        verbose = False
        try:
            opts, args = getopt.getopt(sys.argv[2:], "hv", ["help", "verbose"])
        except getopt.GetoptError, err:
            # print help information and exit:
            print str(err) # will print something like "option -a not recognized"
            usage()
            sys.exit(2)
        
        for o, a in opts:
            if o == "-v":
                verbose = True
            elif o in ("-h", "--help"):
                usage()
                sys.exit()
            else:
                assert False, "unhandled option"
        
        if(os.path.isfile(argv[0])):
            infile = argv[0]
        else:
            sys.stderr.write("Error: file not found\n")
            sys.exit()
                
        if(verbose):
            print "Reading " + str(argv[0])   
        
        alpha_list = list()
        beta_list = list()
        gamma_list = list()
        mse_list = list()
        roc_list = list()
        score_list = list()      
        lambdas = [0.1,0.15,0.25,0.35,0.50,0.60,0.75]
        score_lambdas = dict()
        alpha_lambdas = dict()
        beta_lambdas = dict()
        gamma_lambdas = dict()
        for lam in lambdas:
            score_lambdas[lam] = -1000
            alpha_lambdas[lam] = -1000
            beta_lambdas[lam] = -1000
            gamma_lambdas[lam] = -1000
        
        fn = open(infile)
        for line in fn.readlines():
            words = line.split()
            if(line.find("Grid searching") != -1):
                alpha = float(words[3])
                alpha_list.append(alpha)
                beta = float(words[5])
                beta_list.append(beta)
                gamma = float(words[7])
                gamma_list.append(gamma)
            
            if(line.find("ROC") != -1):
                roc = float(words[7])
                roc_list.append(roc)
            
            if(line.find("MSE") != -1):
                mse = abs(float(line.split()[7].split(",")[1]))  #MAE
                #mse = abs(float(line.split()[7].split(",")[3])) # MSE
                mse_list.append(mse)
            
            if(line.find("Objective function") != -1):
                score = float(words[9])
                score_list.append(score)
            
        for lamb in lambdas:
            for x in xrange(len(gamma_list)):
                alpha_local = alpha_list[x]
                beta_local = beta_list[x]
                gamma_local = gamma_list[x]
                mse_local = mse_list[x]
                roc_local = roc_list[x]
                temp_score = lamb * roc_local - abs( (1-lamb) * mse_local)
                if(temp_score > float(score_lambdas[lamb])):
                    score_lambdas[lamb] = temp_score
                    alpha_lambdas[lamb] = alpha_local
                    beta_lambdas[lamb] = beta_local
                    gamma_lambdas[lamb] = gamma_local
        
        for lamb in lambdas:
            print "Best Alpha Beta and Gamma for lambda " + str(lamb) + " is " + str(alpha_lambdas[lamb]) \
            + " " + str(beta_lambdas[lamb]) + " " + str(gamma_lambdas[lamb]) + " with score " + str(score_lambdas[lamb])
                      
        colors = ["red","blue","yellow","black","brown","pink","cyan","darkblue","darkred"]
        

        print "The covariance of gamma and beta is : " + str(np.cov(np.vstack((gamma_list,beta_list))))
        print "The covariance of gamma and alpha is : " + str(np.cov(np.vstack((gamma_list,alpha_list))))
        print "The covariance of alpha and beta is : " + str(np.cov(np.vstack((alpha_list,beta_list))))
        
        ## MSE VS ROC
        clf()   
        scatter(mse_list,roc_list, lw = '2', label = "Mse_vs_roc", color = "blue")
        v = [min(mse_list), max(mse_list), min(roc_list), max(roc_list)] #AXES [x-min, x-max, y-min, y-max]
        axis(v)
        xlabel("MSE FDR divergence score",fontsize=20) #X-label
        ylabel("ROC curve score",fontsize=20) #Y-label   
        legend(loc = 'lower right')
        savefig("mse_vs_roc.png", format='png')  
        
        best_single_alpha = list()
        best_single_beta = list()
        best_single_gamma = list()
        
        best_single_alpha_roc = list()
        best_single_alpha_mse = list()
        best_single_alpha_score = list()
        
        best_single_beta_roc = list()
        best_single_beta_mse = list()
        best_single_beta_score = list()
        
        best_single_gamma_roc = list()
        best_single_gamma_mse = list()
        best_single_gamma_score = list()
        
        best_single_beta_for_alpha = list()
        best_single_beta_for_gamma = list()
        
        best_single_alpha_for_beta = list()
        best_single_alpha_for_gamma = list()
        
        best_single_gamma_for_alpha = list()
        best_single_gamma_for_beta = list()
  
        best_single_score_for_alpha = list()
        best_single_score_for_beta = list()
        best_single_score_for_gamma = list()
        
        for x in xrange(len(gamma_list)):
            if(gamma_list[x] == gamma_lambdas[0.15] and beta_list[x] == beta_lambdas[0.15]):
                best_single_alpha.append(alpha_list[x])
                best_single_alpha_roc.append(roc_list[x])
                best_single_alpha_mse.append(mse_list[x])
                best_single_alpha_score.append(score_list[x])
            if(gamma_list[x] == gamma_lambdas[0.15] and alpha_list[x] == alpha_lambdas[0.15]):
                best_single_beta.append(beta_list[x])
                best_single_beta_roc.append(roc_list[x])
                best_single_beta_mse.append(mse_list[x])
                best_single_beta_score.append(score_list[x])
            if(alpha_list[x] == alpha_lambdas[0.15] and beta_list[x] == beta_lambdas[0.15]):
                best_single_gamma.append(gamma_list[x])
                best_single_gamma_roc.append(roc_list[x])
                best_single_gamma_mse.append(mse_list[x])
                best_single_gamma_score.append(score_list[x])
                
            if(alpha_list[x] == alpha_lambdas[0.15]):
                best_single_gamma_for_alpha.append(gamma_list[x]) 
                best_single_beta_for_alpha.append(beta_list[x])
                best_single_score_for_alpha.append(score_list[x])
            if(beta_list[x] == beta_lambdas[0.15]):
                best_single_gamma_for_beta.append(gamma_list[x])
                best_single_alpha_for_beta.append(alpha_list[x])
                best_single_score_for_beta.append(score_list[x])
            if(gamma_list[x] == gamma_lambdas[0.15]):
                best_single_alpha_for_gamma.append(alpha_list[x])
                best_single_beta_for_gamma.append(beta_list[x])
                best_single_score_for_gamma.append(score_list[x])
            
        ##ALPHA VS MSE, ROC and SCORE FOR LOCAL MAXIMUNS
        clf()
        plot(best_single_alpha, best_single_alpha_mse, lw = '2', color = "blue", label = "alpha_Vs_mse")
        v = [min(best_single_alpha), max(best_single_alpha), min(best_single_alpha_mse), max(best_single_alpha_mse)] #AXES [x-min, x-max, y-min, y-max]
        axis(v)
        ylabel("MSE FDR divergence score",fontsize=20) #X-label
        xlabel("alpha",fontsize=20) #Y-label  
        savefig("alpha_vs_mse.png", format='png')  
        
        clf()  
        plot(best_single_alpha, best_single_alpha_roc, lw = '2', color = "blue", label = "alpha_Vs_roc") 
        v = [min(best_single_alpha), max(best_single_alpha), min(best_single_alpha_roc), max(best_single_alpha_roc)] #AXES [x-min, x-max, y-min, y-max]
        axis(v)
        xlabel("alpha",fontsize=20) #X-label
        ylabel("ROC curve score",fontsize=20) #Y-label   
        legend(loc = 'lower right')
        savefig("alpha_vs_roc.png", format='png')  
        
        clf()  
        plot(best_single_alpha, best_single_alpha_score, lw = '2', color = "blue", label = "alpha_Vs_score")  
        v = [min(best_single_alpha), max(best_single_alpha), min(best_single_alpha_score), max(best_single_alpha_score)] #AXES [x-min, x-max, y-min, y-max]
        axis(v)
        xlabel("alpha",fontsize=20) #X-label
        ylabel("score",fontsize=20) #Y-label   
        legend(loc = 'lower right')
        savefig("alpha_vs_score.png", format='png')  
        
        ##BETA VS MSE, ROC and SCORE
        clf()
        plot(best_single_beta, best_single_beta_mse, lw = '2', color = "blue", label = "beta_Vs_mse")   
        v = [min(best_single_beta), max(best_single_beta), min(best_single_beta_mse), max(best_single_beta_mse)] #AXES [x-min, x-max, y-min, y-max]
        axis(v)
        ylabel("MSE FDR divergence score",fontsize=20) #X-label
        xlabel("beta",fontsize=20) #Y-label   
        legend(loc = 'lower right')
        savefig("beta_vs_mse.png", format='png')  
        
        clf() 
        plot(best_single_beta, best_single_beta_roc, lw = '2', color = "blue", label = "beta_Vs_roc")  
        v = [min(best_single_beta), max(best_single_beta), min(best_single_beta_roc), max(best_single_beta_roc)] #AXES [x-min, x-max, y-min, y-max]
        axis(v)
        xlabel("beta",fontsize=20) #X-label
        ylabel("ROC curve score",fontsize=20) #Y-label   
        legend(loc = 'lower right')
        savefig("beta_vs_roc.png", format='png')  
        
        clf()
        plot(best_single_beta, best_single_beta_score, lw = '2', color = "blue", label = "beta_Vs_score")   
        v = [min(best_single_beta), max(best_single_beta), min(best_single_beta_score), max(best_single_beta_score)] #AXES [x-min, x-max, y-min, y-max]
        axis(v)
        xlabel("beta",fontsize=20) #X-label
        ylabel("score",fontsize=20) #Y-label   
        legend(loc = 'lower right')
        savefig("beta_vs_score.png", format='png')  

        ##GAMMA VS MSE, ROC and SCORE
        clf()
        plot(best_single_gamma, best_single_gamma_mse, lw = '2', color = "blue", label = "gamma_Vs_mse")    
        v = [min(best_single_gamma), max(best_single_gamma), min(best_single_gamma_mse), max(best_single_gamma_mse)] #AXES [x-min, x-max, y-min, y-max]
        axis(v)
        ylabel("MSE FDR divergence score",fontsize=20) #X-label
        xlabel("gamma",fontsize=20) #Y-label   
        legend(loc = 'lower right')
        savefig("gamma_vs_mse.png", format='png')  
        
        clf()   
        plot(best_single_gamma, best_single_gamma_roc, lw = '2', color = "blue", label = "gamma_Vs_roc") 
        v = [min(best_single_gamma), max(best_single_gamma), min(best_single_gamma_roc), max(best_single_gamma_roc)] #AXES [x-min, x-max, y-min, y-max]
        axis(v)
        xlabel("gamma",fontsize=20) #X-label
        ylabel("ROC curve score",fontsize=20) #Y-label   
        legend(loc = 'lower right')
        savefig("gamma_vs_roc.png", format='png')  
        
        clf() 
        plot(best_single_gamma, best_single_gamma_score, lw = '2', color = "blue", label = "gamma_Vs_roc")   
        v = [min(best_single_gamma), max(best_single_gamma), min(best_single_gamma_score), max(best_single_gamma_score)] #AXES [x-min, x-max, y-min, y-max]
        axis(v)
        xlabel("gamma",fontsize=20) #X-label
        ylabel("score",fontsize=20) #Y-label   
        legend(loc = 'lower right')
        savefig("gamma_vs_score.png", format='png')  
        
        
#        clf() 
#        for lamb in [0.1,0.15,0.25,0.35,0.50]:
#            mse_local_list = list()
#            roc_local_list = list()
#            for x in frange(-0.1,1.0,0.01):
#                for y in frange(0.0,1.0,0.01):
#                    mse_local = x
#                    roc_local = y
#                    temp_score = lamb * roc_local - ( (1-lamb) * mse_local)
#                    if(temp_score == 0.1): 
#                        mse_local_list.append(mse_local)
#                        roc_local_list.append(roc_local)      
#            plot(mse_local_list,roc_local_list, lw = '2', label = "F=0.1_lambda("+str(lamb)+")", color = colors[lambdas.index(lamb)])
#        scatter(mse_list,roc_list, lw = '2', label = "Mse_vs_roc", color = "orange")
#        v = [-0.1, 0.1, 0, 1] #AXES [x-min, x-max, y-min, y-max]
#        axis(v)
#        xlabel("MSE FDR divergence score",fontsize=20) #X-label
#        ylabel("ROC curve score",fontsize=20) #Y-label   
#        legend(loc = 'lower left')
#        savefig("mse_vs_roc_vs_lambdas.png", format='png')  
        
        ## 3D SCATTER PLOT MSE and ROC as a FUNCTION of the SCORE
        clf()
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        scat = ax.scatter(mse_list, roc_list, score_list, c=score_list, s=100)
        ax.set_xlim3d(min(mse_list), max(mse_list))
        ax.set_ylim3d(min(roc_list), max(roc_list))
        ax.set_zlim3d(min(score_list), max(score_list))
        ax.set_xlabel('X Label - MSE')
        ax.set_ylabel('Y Label - ROC')
        ax.set_zlabel('Z Label - SCORE')
        savefig("mse_vs_roc_vs_score.png", format='png')  
        
        ## 3D SCATTER PLOT, ALPHA, BETA and GAMMA as function of the score
        clf()
        fig = plt.figure(figsize=(12.0, 8.0))
        ax = fig.add_subplot(111, projection='3d')
        scat = ax.scatter(alpha_list, beta_list, gamma_list, c=score_list, s=100)
        ax.set_xlim3d(min(alpha_list), max(alpha_list))
        ax.set_ylim3d(min(beta_list), max(beta_list))
        ax.set_zlim3d(min(gamma_list), max(gamma_list))
        #ax.set_xticks(np.arange(min(alpha_list), max(alpha_list), 0.01))
        #ax.set_yticks(np.arange(min(beta_list), max(beta_list), 0.01))
        #ax.set_zticks(np.arange(min(gamma_list), max(gamma_list), 0.1))
        ax.set_xlabel('X Label - ALPHA')
        ax.set_ylabel('Y Label - BETA')
        ax.set_zlabel('Z Label - GAMMA')
        fig.colorbar(scat, shrink=0.5, aspect=5)
        savefig("alpha_vs_beta_vs_gamma.png", format='png')  
        
        
        ##PLOTTING ALPHA AND BETA AS A FUNCTION OF DIFFERENT GAMMAS
        gamma_indexs = list()
        different_gammas = list()
        
        for g in gamma_list:
            if g not in different_gammas:
                different_gammas.append(g)
        
        for gindex in different_gammas:
            first_gamma = gamma_list.index(gindex)
            last_gamma = len(gamma_list) - 1 - gamma_list[::-1].index(gindex) - 1
            gamma_indexs.append((first_gamma,last_gamma))

        for init,end in gamma_indexs:
            x = alpha_list[init:end]
            y = beta_list[init:end]
            z = score_list[init:end]
            if( len(x) > 0 and len(y) > 0 and len(z) > 0):
                clf()
                fig = plt.figure()
                xi = np.linspace(min(x), max(x))
                yi = np.linspace(min(y), max(y))
                zi = np.linspace(min(z), max(z))
                X, Y = np.meshgrid(xi, yi)
                Z = griddata(x, y, z, xi, yi)
                scatter(X, Y, s=100, c=Z, marker='o')
                v = [min(x) - 0.01, max(x) + 0.01, min(y) - 0.01, max(y) + 0.01] #AXES [x-min, x-max, y-min, y-max]
                axis(v)
                xlabel("alpha",fontsize=20) #X-label
                ylabel("beta",fontsize=20) #Y-label   
                savefig("alpha_vs_beta_vs_score_gamma_"+str(gamma_list[init])+".png", format='png') 
                
                
                
        clf()
        fig = plt.figure()
        xi = np.linspace(min(best_single_alpha_for_gamma), max(best_single_alpha_for_gamma))
        yi = np.linspace(min(best_single_beta_for_gamma), max(best_single_beta_for_gamma))
        zi = np.linspace(min(best_single_score_for_gamma), max(best_single_score_for_gamma))
        X, Y = np.meshgrid(xi, yi)
        Z = griddata(best_single_alpha_for_gamma, best_single_beta_for_gamma, best_single_score_for_gamma, xi, yi)
        scatter(X, Y, s=100, c=Z, marker='o')
        v = [min(best_single_alpha_for_gamma) - 0.01, max(best_single_alpha_for_gamma) + 0.01, min(best_single_beta_for_gamma) - 0.01, max(best_single_beta_for_gamma) + 0.01] #AXES [x-min, x-max, y-min, y-max]
        axis(v)
        xlabel("alpha",fontsize=20) #X-label
        ylabel("beta",fontsize=20) #Y-label   
        savefig("alpha_vs_beta_vs_gamma_0.png", format='png') 

        clf()
        fig = plt.figure()
        xi = np.linspace(min(best_single_alpha_for_beta), max(best_single_alpha_for_beta))
        yi = np.linspace(min(best_single_gamma_for_beta), max(best_single_gamma_for_beta))
        zi = np.linspace(min(best_single_score_for_beta), max(best_single_score_for_beta))
        X, Y = np.meshgrid(xi, yi)
        Z = griddata(best_single_alpha_for_beta, best_single_gamma_for_beta, best_single_score_for_beta, xi, yi)
        scatter(X, Y, s=100, c=Z, marker='o')
        v = [min(best_single_alpha_for_beta) - 0.01, max(best_single_alpha_for_beta) + 0.01, min(best_single_gamma_for_beta) - 0.01, max(best_single_gamma_for_beta) + 0.01] #AXES [x-min, x-max, y-min, y-max]
        axis(v)
        xlabel("alpha",fontsize=20) #X-label
        ylabel("gamma",fontsize=20) #Y-label   
        savefig("alpha_vs_gamma_vs_beta_0.png", format='png')     
                
        clf()
        fig = plt.figure()
        xi = np.linspace(min(best_single_beta_for_alpha), max(best_single_beta_for_alpha))
        yi = np.linspace(min(best_single_gamma_for_alpha), max(best_single_gamma_for_alpha))
        zi = np.linspace(min(best_single_score_for_alpha), max(best_single_score_for_alpha))
        X, Y = np.meshgrid(xi, yi)
        Z = griddata(best_single_beta_for_alpha, best_single_gamma_for_alpha, best_single_score_for_alpha, xi, yi)
        scatter(X, Y, s=100, c=Z, marker='o')
        v = [min(best_single_beta_for_alpha) - 0.01, max(best_single_beta_for_alpha) + 0.01, min(best_single_gamma_for_alpha) - 0.01, max(best_single_gamma_for_alpha) + 0.01] #AXES [x-min, x-max, y-min, y-max]
        axis(v)
        xlabel("beta",fontsize=20) #X-label
        ylabel("gamma",fontsize=20) #Y-label   
        savefig("beta_vs_gamma_vs_alpha_0.png", format='png')      
        
#        clf()   
#        for i in xrange(len(lambdas)):
#            lamb = lambdas[i]
#            color = colors[i]
#            scatter([(ms * (1 - lamb)) for ms in mse_list],[(roc * lamb) for roc in roc_list], lw = '2', label = "lambda="+str(lamb), color = color)
#        xlabel("MSE(lambda) FDR divergence score",fontsize=20) #X-label
#        ylabel("ROC(lambda) curve score",fontsize=20) #Y-label   
#        legend(loc = 'upper right')
#        savefig("mse(1-lambda)_vs_roc(lambda).png", format='png')  
        
#        clf()   
#        for i in xrange(len(lambdas)):
#            lamb = lambdas[i]
#            scores = list()
#            for x in xrange(len(mse_list)):
#                score = roc * lamb - abs(ms * (1-lamb))
#                scores.append(score)
#            scatter(scores,scores, lw = '2', label = "lambda_vs_score"+str(lamb), color = color)
#        xlabel("Score",fontsize=20) #X-label
#        ylabel("Lambda",fontsize=20) #Y-label   
#        legend(loc = 'lower right')
#        savefig("lambda_vs_score.png", format='png')  
        
        if(verbose):
            print "done"   
        
if __name__ == "__main__":
    main(sys.argv[1:]) 
