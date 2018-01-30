#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 19:54:08 2010

@author: sat kumar tomer (http://civil.iisc.ernet.in/~satkumar/)

Functions:
    utm2deg: Calculate utm co-ordinates from Lat, Lon
    deg2utm : Calculate Lat, Lon from UTM
    kabini: 
    berambadi: 
"""

# load needed python modules 
from pyproj import Proj



def Geo2Pixel(Xgeo,Ygeo,GT):
    a1 = GT[1]
    b1 = GT[2]
    c1 = Xgeo - GT[0]
    a2 = GT[4]
    b2 = GT[5]
    c2 = Ygeo - GT[3]
    Xpixel = (b2*c1-b1*c2)/(a1*b2-a2*b1) 
    Yline = (a2*c1-a1*c2)/(a2*b1-a1*b2) 
    return Xpixel, Yline

def Pixel2Geo(Xpixel,Yline,GT):
    Xgeo = GT[0] + Xpixel*GT[1] + Yline*GT[2]
    Ygeo = GT[3] + Xpixel*GT[4] + Yline*GT[5]
    return Xgeo,Ygeo

def SetProjectionBerambadi():
	return 'PROJCS["WGS 84 / UTM zone 43N",GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433],AUTHORITY["EPSG","4326"]],PROJECTION["Transverse_Mercator"],PARAMETER["latitude_of_origin",0],PARAMETER["central_meridian",75],PARAMETER["scale_factor",0.9996],PARAMETER["false_easting",500000],PARAMETER["false_northing",0],UNIT["metre",1,AUTHORITY["EPSG","9001"]],AUTHORITY["EPSG","32643"]]'

def utm2deg(x,y,utmzone=43):
    p = Proj(proj='utm',zone=43,ellps='WGS84')
    Lon,Lat = p(x, y, inverse=True)
    return Lon,Lat
    
def deg2utm(Lon,Lat,utmzone=43):
    p = Proj(proj='utm',zone=utmzone,ellps='WGS84')
    x,y = p(Lon, Lat)
    return x,y
    
def kabini(Ifile,Ofile):
    # define the file names file
    Temp1 = '/home/tomer/MODISdata/temp/temp1.tif'
    Temp2 = '/home/tomer/MODISdata/temp/temp2.tif'
            
    # convert from geographical co-ordinates to UTM zone 43
    cmd= 'gdalwarp -r bilinear -t_srs  \'+proj=utm +zone=43 +datum=WGS84\' ' + Ifile + ' ' +Temp1
    try:
        returncode = call(cmd, shell=True)
        if returncode:
            print 'Failure with returncode', returncode; sys.exit(1)
    except OSError, message:
        print 'Execution failed!\n', message; sys.exit(1)

    # cut the area around Kabini Basin (output image will be of size 129 X 102)
    kab='582000 1372000 711000 1270000'
    cmd = 'gdal_translate -a_ullr ' + kab + ' -projwin ' + kab + ' ' + Temp1+ ' ' + Temp2
    try:
        returncode = call(cmd, shell=True)
        if returncode:
            print 'Failure with returncode', returncode; sys.exit(1)
    except OSError, message:
        print 'Execution failed!\n', message; sys.exit(1)
        
    # changing the resolution
    cmd = 'gdalwarp -r bilinear -tr 1000 1000 ' + Temp2 + ' ' +Ofile
    try:
        returncode = call(cmd, shell=True)
        if returncode:
            print 'Failure with returncode', returncode; sys.exit(1)
    except OSError, message:
        print 'Execution failed!\n', message; sys.exit(1)
        
    # remove the temporary file
    try:
        os.remove(Temp)
        os.remove(Temp2)
    except:
        print 'temp file not created'

def berambadi(Ifile,Ofile):
    # define the file names file
    Temp1 = '/home/tomer/MODISdata/temp/temp1.tif'
    Temp2 = '/home/tomer/MODISdata/temp/temp2.tif'
            
    # convert from geographical co-ordinates to UTM zone 43
    cmd= 'gdalwarp -r bilinear -t_srs  \'+proj=utm +zone=43 +datum=WGS84\' ' + Ifile + ' ' +Temp1
    try:
        returncode = call(cmd, shell=True)
        if returncode:
            print 'Failure with returncode', returncode; sys.exit(1)
    except OSError, message:
        print 'Execution failed!\n', message; sys.exit(1)

    # cut the area around Kabini Basin (output image will be of size 129 X 102)
    bmc='664000 1309000 685000 1294000'
    cmd = 'gdal_translate -a_ullr ' + bmd + ' -projwin ' + bmd + ' ' + Temp1+ ' ' + Temp2
    try:
        returncode = call(cmd, shell=True)
        if returncode:
            print 'Failure with returncode', returncode; sys.exit(1)
    except OSError, message:
        print 'Execution failed!\n', message; sys.exit(1)
        
    # changing the resolution
    cmd = 'gdalwarp -r bilinear -tr 1000 1000 ' + Temp2 + ' ' +Ofile
    try:
        returncode = call(cmd, shell=True)
        if returncode:
            print 'Failure with returncode', returncode; sys.exit(1)
    except OSError, message:
        print 'Execution failed!\n', message; sys.exit(1)
        
    # remove the temporary file
    try:
        os.remove(Temp1)
        os.remove(Temp2)
    except:
        print 'temp file not created'

