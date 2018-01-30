# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 17:55:54 2011

@author: Sat Kumar Tomer
@website: www.ambhas.com
@email: satkumartomer@gmail.com
"""

# import required modules
import numpy as np
import matplotlib.pylab as plt


class OK:
    """
    This performs the ordinary kriging
    Input:
        x: x vector of location
        Y: y vector of location
        z: data vector at location (x,y)
    
    Output:
        None
        
    Methods:
        variogram: estimate the variogram
        
    """
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
    
    def variogram(self, var_type='averaged', min_lag=None):
        x = self.x
        y = self.y
        z = self.z
        # make the meshgrid
        X1,X2 = np.meshgrid(x,x) 
        Y1,Y2 = np.meshgrid(y,y)
        Z1,Z2 = np.meshgrid(z,z)
        
        D = np.sqrt((X1 - X2)**2 + (Y1 - Y2)**2)
        self.D = D
        G = 0.5*(Z1 - Z2)**2
        indx = range(len(z))
        C,R = np.meshgrid(indx,indx)
        I = R > C

        D2 = D*(np.diag(x*np.nan)+1)
        lag = 10*np.mean(np.nanmin(D2))
	if min_lag is not None:
	    lag = min_lag

        hmd = D.max()/2
        max_lags = np.floor(hmd/lag)
        LAGS = np.ceil(D/lag)
        
        DE = np.empty(max_lags)
        PN = np.empty(max_lags)
        GE = np.empty(max_lags)
        for i in range(int(max_lags)):
            SEL = (LAGS == i+1)
            DE[i] = D[SEL].mean()
            PN[i] = np.sum(SEL == 1)/2
            GE[i] = G[SEL].mean()
            
        if var_type == 'scattered':
            return D[I],G[I]      
        elif var_type == 'averaged':
            return DE,GE
        else:
            raise ValueError('var_type should be either averaged or scatter')
        
    def vario_model(self, lags, model_par, model_type='linear'):
        """
        Input:
            model_type : the type of variogram model 
                             spherical
                             linear
                             exponential
        """
        
        if model_type == 'spherical':
            n = model_par['nugget']
            r = model_par['range']
            s = model_par['sill']
            l = lags
            G = n + (s*(1.5*l/r - 0.5*(l/r)**3)*(l<=r) + s*(l>r))
        
        elif model_type == 'linear':
            n = model_par['nugget']
            s = model_par['slope']
            l = lags
            G = n + s*l
        
        elif model_type == 'exponential':
            n = model_par['nugget']
            r = model_par['range']
            s = model_par['sill']
            l = lags
            G = n + s*(1 - np.exp(-3*l/r))
        
        else:
            raise ValueError('model_type should be spherical or linear or exponential')
            
        return G
            
    def krige(self, Xg, Yg, model_par, model_type):
        
        # set up the Gmod matrix 
        n = len(self.x)
        Gmod = np.empty((n+1,n+1))
        Gmod[:n, :n] = self.vario_model(self.D, model_par, model_type)
                
        Gmod[:,n] = 1
        Gmod[n,:] = 1
        Gmod[n,n] = 0

        Gmod = np.matrix(Gmod)      
        
        # inverse of Gmod
        Ginv = Gmod.I

        Xg = Xg.flatten()
        Yg = Yg.flatten()        
        Zg = np.empty(Xg.shape)
        s2_k = np.empty(Xg.shape)
        
        for k in range(len(Xg)):
            
            DOR = ((self.x - Xg[k])**2 + (self.y - Yg[k])**2)**0.5
            GR = np.empty((n+1,1))
            GR[:n,0] = self.vario_model(DOR, model_par, model_type)
            GR[n,0] = 1
            E = np.array(Ginv * GR )
            Zg[k] = np.sum(E[:n,0]*self.z)
            s2_k[k] = np.sum(E[:n,0]*GR[:n,0])+ E[n, 0]
        
        self.Zg = Zg
        self.s2_k = s2_k
            
if __name__ == "__main__":          
    # generate some sythetic data
    x = np.random.normal(size=100)
    y = np.random.normal(size=100)
    z = 0.0*np.random.normal(size=100)+x+y
    
    foo = OK(x,y,z)
    ax,ay = foo.variogram()
    
    #plt.plot(ax,ay,'ro')
    
    lags = np.linspace(0,5)
    model_par = {}
    model_par['nugget'] = 0
    model_par['range'] = 1
    model_par['sill'] = 2.0
    
    G = foo.vario_model(lags, model_par, model_type = 'exponential')
    #plt.plot(lags, G, 'k')
    #plt.show()
    
    Rx = np.linspace(-1,1)
    Ry = np.linspace(0,1)
    foo.krige(Rx, Ry, model_par, 'exponential')
    
    plt.plot(x,z,'ro')
    plt.plot(Rx,foo.Zg)
    plt.show()
