# -*- coding: utf-8 -*-
"""
Created on Tue May 24 18:07:28 2011

@author: Sat Kumar Tomer
@website: www.ambhas.com
@email: satkumartomer@gmail.com
"""

# import required libraries
from __future__ import division
import numpy as np
from errlib import rmse
from scipy.optimize import fmin
from scipy.stats import poisson

class RainDisagg:
    
    
    def __init__(self,rf):
        self.rf = rf
            
        # calculate the length of rainfall series
        len_rf = len(rf)
                  
        # take only that much length of rainfall series which is multiplication of 32 
        rf_1 = rf[0:-np.mod(len_rf,32)]
        
        # summing rainfall for 2 days
        rf_2 = np.sum(rf_1.reshape(-1,2), axis=1)
        
        # summing rainfall for 4 days
        rf_4 = np.sum(rf_2.reshape(-1,2), axis=1)
        
        # summing rainfall for 8 days
        rf_8 = np.sum(rf_4.reshape(-1,2), axis=1)
        
        # summing rainfall for 16 days
        rf_16 = np.sum(rf_8.reshape(-1,2), axis=1)
        
        # summing rainfall for 32 days
        rf_32 = np.sum(rf_16.reshape(-1,2), axis=1)
        
        #generate moments (q varies from 0 to 5)
        # row => time scale
        # column => moments
        M1 = np.zeros((6,11))
        for i in range(11):
            M1[0,i] = np.mean(rf_1**(i/2))
            M1[1,i] = np.mean(rf_2**(i/2))
            M1[2,i] = np.mean(rf_4**(i/2))
            M1[3,i] = np.mean(rf_8**(i/2))
            M1[4,i] = np.mean(rf_16**(i/2))
            M1[5,i] = np.mean(rf_32**(i/2))
        
        self.logM = np.log(M1)
        
        # l is inverse of time scale
        l = [32, 16, 8, 4, 2, 1]
        self.log_lambda = np.log(l)
        
        
        # calculate the tau from the slope of log(M) vs log(l)
        tau_obs = np.zeros(10,)
        for i in range(10):
            tau_obs[i] = -np.polyfit(np.log(l), np.log(M1[:,i+1]),1)[0]
        self.tau_obs = tau_obs
        
        # fit the log-poisson distribution
        self.lp = fmin(self.fun_poisson,np.array([0.4, 0.2]))
        
        # calculate the parameter of log poisson distribution form the parameters
        # of tau function
        self.A = np.exp(self.lp[0]*(1-self.lp[1]))

    #define the log-poisson function
    def fun_poisson(self,par):
        q = np.arange(0.5,5.5,0.5)
        c = abs(par[0])
        beta = abs(par[1])
        b = 2
        tau_pred = q-c*(q*(1-beta)+beta**q-1)/(np.log(b))
        f = rmse(tau_pred,self.tau_obs)
        return f
    
    def disaggregate(self,rf):
        len_rf = len(rf)        
        # generating rainfall from t h to t/2 h
        rf_pre = np.zeros((2,len_rf*2))
        for j in range(2):
            for i in xrange(0,len_rf*2,2):
                W = self.A*(self.lp[1])**poisson.rvs(1, size=2)
                rf_pre[j,i] = rf[int(i/2)]*W[0]/(W[0]+W[1])
                rf_pre[j,i+1] = rf[int(i/2)]*W[1]/(W[0]+W[1])
        
        rf_pre = np.mean(rf_pre, axis=0)

        # rounding up the simulated rainfall to the least count of raingauge 
        for i in xrange(0,len_rf*2,2):
            if np.mod(rf_pre[i],0.5) !=0:
                TB = np.mod(rf_pre[i],0.5)
            else:
                TB = 0
            
            rf_pre[i] -= TB
            rf_pre[i+1] += TB
        
        return rf_pre

