#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 20 15:36:37 2011
@ author:                  Sat Kumar Tomer 
@ author's webpage:        http://civil.iisc.ernet.in/~satkumar/
@ author's email id:       satkumartomer@gmail.com
@ author's website:        www.ambhas.com

A libray with Python functions for calculations of 
micrometeorological parameters and some miscellaneous
utilities.

functions:
    pc_bias : percentage bias
    apb :     absolute percent bias
    rmse :    root mean square error
    mae :     mean absolute error
    bias :    bias
    NS :      Nash-Sutcliffe Coefficient
    
"""

# import required modules
import numpy as np

def filter_nan(s,o):
    data = np.array([s,o])
    data = np.transpose(data)
    data = data[~np.isnan(data).any(1)]
    return data[:,0],data[:,1]

def pc_bias(s,o):
    s,o = filter_nan(s,o)
    return 100.0*sum(s-o)/sum(o)

def apb(s,o):
    s,o = filter_nan(s,o)
    return 100.0*sum(abs(s-o))/sum(o)

def rmse(s,o):
    s,o = filter_nan(s,o)
    return np.sqrt(np.mean((s-o)**2))

def mae(s,o):
    s,o = filter_nan(s,o)
    return np.mean(abs(s-o))

def bias(s,o):
    s,o = filter_nan(s,o)
    return np.mean(s-o)

def NS(s,o):
    s,o = filter_nan(s,o)
    return 1 - sum((s-o)**2)/sum((o-np.mean(o))**2)

def L(s,o, N=5):
    s,o = filter_nan(s,o)
    return np.exp(-N*sum((s-o)**2)/sum((o-np.mean(o))**2))

def correlation(s,o):
    s,o = filter_nan(s,o)
    return np.corrcoef(o, s)[0,1]

