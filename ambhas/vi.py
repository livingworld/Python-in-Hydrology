#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  9 11:51:10 2011
@ author:                  Sat Kumar Tomer 
@ author's webpage:        http://civil.iisc.ernet.in/~satkumar/
@ author's email id:       satkumartomer@gmail.com
@ author's website:        www.ambhas.com
"""

# import required modules
import numpy as np




class vi:
    def __init__(self, g, r, nir, swir):
        self.g = g
        self.r = r
        self.nir = nir
        self.swir = swir

    def get_vi(self, vi_name):
        exec("veg_ind=fun_"+vi_name+"(g,r,nir,swir)")
        return veg_ind
    
    def fun_rvi(g,r,nir,swir):
        rvi = nir/r
        return rvi
    
    def fun_ndvi(g,r,nir,swir):
        ndvi = (nir - r)/(nir + r)
        return ndvi    

    def fun_ipvi(g,r,nir,swir):
        ipvi = (nir)/(nir + r)
        return ipvi        
    
    def fun_dvi(g,r,nir,swir):
        dvi = nir-r
        return dvi    
    
    
    def fun_rndvi(g,r,nir,swir):
        rndvi = (nir**2 - r)/(nir + r**2)
        return rndvi
    
    def fun_mrvi(g,r,nir,swir):
        mrvi = swir/r
        return mrvi
         
    def fun_mpri(g,r,nir,swir):
        mpri = (g - r)/(g + r)
        return mpri
        
    def fun_savi(g,r,nir,swir):
        savi = 1.5*(nir - r)/(nir + r + 0.5)
        return savi  

    def fun_evi2(g,r,nir,swir):
        evi2 = 2.5*(nir - r)/(nir + r + 1)
        return evi2
        
    def fun_mgndvi(g,r,nir,swir):
        mgndvi = (swir - g)/(swir + g)
        return mgndvi   
        
    def fun_mndvi(g,r,nir,swir):
        mndvi = (swir - r)/(swir + r)
        return mndvi
        
    def fun_bi(g,r,nir,swir):
        bi = (g + r + nir + swir)/500
        return bi   
     
    def fun_rgri(g,r,nir,swir):
        rgri = r/g
        return rgri  
     
    def fun_gndvi(g,r,nir,swir):
        gndvi = (nir-g)/(nir + g)
        return gndvi
    
    def fun_ndrgi(g,r,nir,swir):
        ndrgi = (r - g)/(r + g)
        return ndrgi  
    
    def fun_ndvsi(g,r,nir,swir):
        ndvsi = (nir -0.5*(r + g))/(nir + 0.5*(r+g))
        return ndvsi   
        
    def fun_rdi(g,r,nir,swir):
        rdi = swir/nir
        return rdi  
     
    def fun_tndvi(g,r,nir,swir):
        tndvi = np.sqrt((nir - r)/(nir + r) + 1)
        return tndvi
        
    def fun_grvi(g,r,nir,swir):
        grvi = nir/g
        return grvi  
     
    def fun_osavi(g,r,nir,swir):
        osavi = (nir - r)/(nir + r + 0.16)
        return osavi  
       
    def fun_mgrvi(g,r,nir,swir):
        mgrvi = swir/g
        return mgrvi
       
    def fun_slavi(g,r,nir,swir):
        slavi = nir/(r + swir)
        return slavi
       
    def fun_ndmi(g,r,nir,swir):
        ndmi = (nir - swir)/(nir + swir)
        return ndmi   
    
