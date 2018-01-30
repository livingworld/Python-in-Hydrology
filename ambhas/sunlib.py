#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 11:53:29 2011
@author: sat kumar tomer (http://civil.iisc.ernet.in/~satkumar/)

"""

import numpy as np

class sun():
    """
    This class estimate extral-terrestial solar radiation,
    sunset time, sunrise time, daylight hours
    
    Based on the article:
        Empirical Model for Estimating Global Solar Radiation
        on Horizontal Surfaces for Selected Cities in 
        the Six Geopolitical Zones in Nigeria
    By:
        M.S. Okundamiya and A.N. Nzeako

        
    Example:
        lat_deg = 11
        lon_deg = 76
        doy = 180
        foo = sun(doy, lat_deg, lon_deg)
        hourly_etr = foo.hourly_ETR(11.0)
        daily_etr = foo.daily_ETR()
        risetime, settime = foo.set_rise()
    """
    

    def __init__(self, doy, lat_deg, lon_deg, ze=5.5):
        """ initialise the class
        Input:
            doy:            day of year
            lat_deg:        latitude in degree ( south is negative)
            lon_deg:        longitude in degree (west is negative)
            ze :            time zone in hour
        """
        self.doy = doy
        self._lat_rad = lat_deg*np.pi/180
        
        self.lon_deg = lon_deg
        self.ze = ze

        
        
        self._Isc = 1367 # solar constant (W/m^2)

        B_deg = (doy-1)*360/365
        B_rad = B_deg*np.pi/180
        
        E = 3.82*(0.000075 + 0.001868*np.cos(B_rad) - 0.032077*np.sin(B_rad) \
                    - 0.0141615*np.cos(2*B_rad) -0.04089*np.sin(2*B_rad) )
        
        self._E = E        
        
        # declination
        delta = 0.4093*np.sin(2*np.pi*(284+doy)/365)
        self._delta = delta
    
        # relative distance of the earth from sun
        dr = 1 + 0.0033*np.cos(2*np.pi*doy/365)
        self.dr = dr
        
    def hourly_ETR(self,tc):
        """
        Input:
            tc:     local time in hours
        """
        ze = self.ze
        lat_rad = self._lat_rad
        E = self._E 
        delta = self._delta
        dr = self.dr
        
        ts = tc + E + self.lon_deg/15 - ze
        # hour angle
        w = ((ts-12)*15)/180.0*np.pi
        # hourly ETR
        I0 = self._Isc*dr*(np.sin(lat_rad)*np.sin(delta) + 
                np.cos(lat_rad)*np.cos(delta)*np.cos(w))
        
        return I0
        
    def daily_ETR(self):
        """ 
        Returns the daily Extra Terrestial Radiation (ETR)
        Input:
            
        Output:
            
        """
        lat_rad = self._lat_rad
        delta = self._delta
        
        # sunset hour angle
        ws = np.arccos(-np.tan(lat_rad)*np.tan(delta))
        # maximum sunshine hour lenght
        self.N = ws*24/np.pi

        H0 = (1/np.pi)*self._Isc*self.dr*(ws*np.sin(delta)*np.sin(lat_rad) +
                np.cos(delta)*np.cos(lat_rad))
                
        return H0
    
    def set_rise(self):
        """
        Returns the sun set and rise time
        """
        lon_deg = self.lon_deg
        lat_rad = self._lat_rad
        delta = self._delta
        E = self._E
        ze = self.ze
        
        w1 = np.arccos(- np.tan(delta)*np.tan(lat_rad))
        ts1 = 12 - w1*180/np.pi/15 
        ts2 = 12 + w1*180/np.pi/15 
        
        tc1 = ts1 - E - lon_deg/15 + ze
        tc2 = ts2 - E - lon_deg/15 + ze
        
        return tc1, tc2
