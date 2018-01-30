# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 14:25:50 2011

@author: Sat Kumar Tomer
@website: www.ambhas.com
@email: satkumartomer@gmail.com
"""
from __future__ import division
import numpy as np
from ambhas.err import L

class GW_1D():
    """
    This class perform the groundwater modelling
    """
    
    def __init__(self, R, Dnet=0):
        """
        R: rainfall
        Dnet: net groundwater draft
        """
        self.R = R
        self.Dnet = 0
        
    def set_parameters(self, F, G, r, hmin=0):
        """
        F: model parameter
        G: model parameter
        r: recharge factor
        hmin: groundwater level at which based flow ceases
        
        sy: specific yield
        lam: decay constant
        """
        self.F = F
        self.G = G
        self.r = r
        self.hmin = hmin
        
        self.lam = (1-F)**2/G
        self.sy = (1-F)/G
            
    def run_model(self, hini, t):
        """
        hini: initial groundwater level
        t: time
        """
        u = self.r*self.R-self.Dnet # net input
        
        h = np.empty(t+1) # create empty array
        h[0] = hini  - self.hmin       # set the initial condition
                
        for k in range(t):
            h[k+1] = self.F*h[k] + self.G*u[k]
            
            
        self.h = h + self.hmin # simulated gw levels
        self.discharge = u[:t] - self.sy*np.diff(h) # simulated discharge
        
 
    
    def ens(self, F_lim, G_lim, r_lim, hmin_lim, ens, hini, h_obs, t):
        """
        generate ensemble based on ensemble of parameters
        Input:
            F: min and max of F
            G: min and max of G
            r: min and max of r
            hmin: min and max of hmin
            ens: no. of ensembles
            hini: initial gw level
            t: final time
        """
        F_ens = F_lim[0] + (F_lim[1]-F_lim[0]) * np.random.rand(ens)
        G_ens = G_lim[0] + (G_lim[1]-G_lim[0]) * np.random.rand(ens)
        r_ens = r_lim[0] + (r_lim[1]-r_lim[0]) * np.random.rand(ens)
        hmin_ens = hmin_lim[0] + (hmin_lim[1]-hmin_lim[0]) * np.random.rand(ens)

        self.F_ens = F_ens
        self.G_ens = G_ens
        self.r_ens = r_ens
        self.hmin_ens = hmin_ens        
        
        self.L = np.empty(ens)
        for i in range(ens):
            self.set_parameters(F_ens[i], G_ens[i], r_ens[i], hmin_ens[i])
            self.run_model(hini, t)
            self.L[i] = L(self.h, h_obs[:t+1])
    
        # select best ensembles        
        ind = self.L.argmax()
                
        self.set_parameters(F_ens[ind], G_ens[ind], r_ens[ind], hmin_ens[ind])
        self.run_model(hini, t)
        self.best_h = self.h
        self.best_ind = ind
  

class GW_2D():
    """
    This class perform the groundwater modelling
    """
    
    def __init__(self, R, Dnet=0):
        """
        R: rainfall
        Dnet: net groundwater draft
        """
        self.R = R
        self.Dnet = 0
    
    def set_parameters(self, lam, sy, r, hmin=0):
        """
        F: model parameter
        G: model parameter
        r: recharge factor
        hmin: groundwater level at which based flow ceases
        
        sy: specific yield
        lam: decay constant
        """
        if len(lam) != len(sy):
            raise ValueError('The lenght of F and G should be same')
        
        nlayer = len(lam) # number of verticle profiles
        self.nlayer = nlayer
        
        F = np.zeros((nlayer, nlayer))
        G = np.zeros(nlayer)
        for i in range(nlayer):
            F[i,i] = 1 - lam[i]/sy[i]
            G[i] = lam[i]/sy[i]**2
            if i>0:
                F[i, i-1] = lam[i-1]/sy[i]
                G[i] = -lam[i-1]/(sy[i-1]*sy[i]) + lam[i]/sy[i]**2
        
        self.F = F
        self.G = G
        self.r = r
        self.hmin = hmin
        
    def run_model(self, hini, t):
        """
        hini: initial groundwater level
        t: time
        """
        u = self.r*self.R-self.Dnet # net input
        
        h = np.empty((t+1, self.nlayer)) # create empty array
        h[0,:] = np.array(hini)  - self.hmin       # set the initial condition
                
        for k in range(t):
            h[k+1] = np.dot(self.F,h[k,:]) + self.G*u[k]
           
        self.h = h + self.hmin

    def ens(self, lam_lim, sy_lim, r_lim, hmin_lim, ens, hini, h_obs, t):
        """
        generate ensemble based on ensemble of parameters
        Input:
            F: min and max of F
            G: min and max of G
            r: min and max of r
            hmin: min and max of hmin
            ens: no. of ensembles
            hini: initial gw level
            t: final time
        """
        lam_lim = np.array(lam_lim)
        sy_lim = np.array(sy_lim)
        r_lim = np.array(r_lim)
        hmin_lim = np.array(hmin_lim)
        
        nlayer = lam_lim.shape[1]
        self.nlayer = nlayer
        
        R_v = np.random.rand(ens,nlayer)
        lam_ens = np.tile(lam_lim[0,:],(ens,1)) + \
            (np.tile(lam_lim[1,:],(ens,1)) - np.tile(lam_lim[0,:],(ens,1)))* R_v
        
        R_v = np.random.rand(ens,nlayer)
        sy_ens = np.tile(sy_lim[0,:],(ens,1)) + \
            (np.tile(sy_lim[1,:],(ens,1)) - np.tile(sy_lim[0,:],(ens,1)))* R_v
        
        r_ens = r_lim[0] + (r_lim[1]-r_lim[0]) * np.random.rand(ens)
        
        hmin_ens = hmin_lim[0] + (hmin_lim[1]-hmin_lim[0]) * np.random.rand(ens)
            
        self.lam_ens = lam_ens
        self.sy_ens = sy_ens
        self.r_ens = r_ens
        self.hmin_ens = hmin_ens
        
        eff = np.empty((ens, nlayer))
        for i in range(ens):
            self.set_parameters(lam_ens[i], sy_ens[i], r_ens[i], hmin_ens[i])
            self.run_model(hini, t)
            for j in range(nlayer):
                eff[i,j] = L(self.h[:,j], h_obs[:t+1,j])
        
        self.eff = eff.mean(axis=1)
        # select best ensembles        
        ind = self.eff.argmax()
                
        self.set_parameters(lam_ens[ind], sy_ens[ind], r_ens[ind], hmin_ens[ind])
        self.run_model(hini, t)
        self.best_h = self.h
        self.best_ind = ind
        
if __name__ == "__main__":
    # forcing
    R = np.random.rand(100)
    foo = GW_1D(R)
    
    # parameter
    F = 0.8
    G = 10
    r = 0.1
    #foo.set_parameters(F, G, r)
    
    # initial condition
    h_ini = 10
    
    # run the model    
    #foo.run_model(h_ini, 100)
    
    # get the simulated data
    #h_sim = foo.h
    
    # ensemble
    h_obs = np.random.rand(101)
    foo.ens([0.5, 1.0], [1, 20], [0, 0.2], [50,70], 2, 20, h_obs, 10)
    print(foo.L)
    
    ################### hill slope groundwater modelling ######################
    foo = GW_2D(R)
    lam = [0.00008, 0.00009, 0.0001, 0.0002]
    sy = [0.001, 0.001, 0.001, 0.001]
    r = 0.2
    foo.set_parameters(lam, sy, r)
    hini = [10,7,5,3]
    foo.run_model(hini, 50)
    
    lam_lim = [[0.2, 0.3, 0.4, 0.5], [0.3, 0.4, 0.5, 0.6]]
    sy_lim = [[0.2, 0.3, 0.4, 0.5], [0.3, 0.4, 0.5, 0.6]]
    r_lim = [0.2,0.3]
    hmin_lim = [2,5]
    ens = 10
    t = 10
    h_obs = np.random.rand(t+1,4)
    foo.ens(lam_lim, sy_lim, r_lim, hmin_lim, ens, hini, h_obs, t)
    
    
    
    