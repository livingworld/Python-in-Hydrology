#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 15:49:45 2011

@ author:                  Sat Kumar Tomer 
@ author's webpage:        http://civil.iisc.ernet.in/~satkumar/
@ author's email id:       satkumartomer@gmail.com
@ author's website:        www.ambhas.com
"""

# import required library
import xlrd
import numpy as np

class time_data:
    def __init__(self, book_name):
        book = xlrd.open_workbook(book_name)
        sheet_daily = book.sheet_by_name('daily')
        sheet_monthly = book.sheet_by_name('monthly')
        
        # parse the daily data
        labels_daily = []
        for i in xrange(sheet_daily.ncols):
            labels_daily.append(str(sheet_daily.cell_value(0,i)))
        self.labels_daily = labels_daily
        
        data_daily = np.zeros((sheet_daily.nrows-1,sheet_daily.ncols))
        for i in xrange(sheet_daily.nrows-1):
            for j in xrange(sheet_daily.ncols):
                try:
                    data_daily[i,j] = sheet_daily.cell_value(i+1,j)
                except:
                    data_daily[i,j] = np.nan
        self.data_daily = data_daily
        
        # parse the monthly data
        labels_monthly = []
        for i in xrange(sheet_monthly.ncols):
            labels_monthly.append(str(sheet_monthly.cell_value(0,i)))
        self.labels_monthly = labels_monthly
        
        data_monthly = np.zeros((sheet_monthly.nrows-1,sheet_monthly.ncols))
        for i in xrange(sheet_monthly.nrows-1):
            for j in xrange(sheet_monthly.ncols):
                try:
                    data_monthly[i,j] = sheet_monthly.cell_value(i+1,j)
                except:
                    data_monthly[i,j] = np.nan
        self.data_monthly = data_monthly
        
    def get(self, var_name):
        if var_name in self.labels_daily:
            var_data = self.data_daily[:,self.labels_daily.index(var_name)]
        elif var_name in self.labels_monthly:
            var_data = self.data_monthly[:,self.labels_monthly.index(var_name)]
        else:
            raise ValueError, var_name + ' not found in the worksheet'
        return var_data
    
    def get_monthly(self, var_name, var_operation = 'mean'):
        if var_name in self.labels_daily:
            year = self.data_daily[:,self.labels_daily.index('year')]
            month = self.data_daily[:,self.labels_daily.index('month')]
            var_data = self.data_daily[:,self.labels_daily.index(var_name)]
            
            min_year = year[0]
            max_year = year[-1]
            
            var_monthly = np.zeros(((max_year - min_year +1)*12,1))
            i = 0
            for ind_year in xrange(min_year,max_year+1):
                for ind_month in xrange(1,13):
                    #var_monthly[i] = sum(var_data[(year == ind_year) & (month == ind_month)])
                    exec('var_monthly[i] = '+var_operation+'(var_data[(year == ind_year) & (month == ind_month)])')
                    i += 1          
                     
            return var_monthly
    
    def get_yearly(self, var_name, var_operation = 'mean'):
        if var_name in self.labels_daily:
            year = self.data_daily[:,self.labels_daily.index('year')]
            var_data = self.data_daily[:,self.labels_daily.index(var_name)]
            
            min_year = year[0]
            max_year = year[-1]
            
            var_yearly = np.zeros((max_year - min_year +1,1))
            i = 0
            for ind_year in xrange(min_year,max_year+1):
                exec('var_yearly[i] = '+var_operation+'(var_data[year == ind_year])')
                i += 1     
        
        elif var_name in self.labels_monthly:
            year = self.data_monthly[:,self.labels_monthly.index('year')]
            var_data = self.data_monthly[:,self.labels_monthly.index(var_name)]
            
            min_year = year[0]
            max_year = year[-1]
            
            var_yearly = np.zeros((max_year - min_year +1,1))
            i = 0
            for ind_year in xrange(min_year,max_year+1):
                #var_yearly[i] = sum(var_data[year == ind_year])
                exec('var_yearly[i] = '+var_operation+'(var_data[year == ind_year])')
                i += 1        
                     
        return var_yearly
    
    def nor(self, season = 'yearly', threshold = 10.0):
        year = self.data_daily[:,self.labels_daily.index('year')]
        month = self.data_daily[:,self.labels_daily.index('month')]
        rain_daily = self.get('rainfall')
        
        min_year = int(year[0])
        max_year = int(year[-1])
        
        if season == 'monthly':
            # monthly distribution of rainy days
            nor_monthly = np.zeros(((max_year - min_year +1)*12,1))
            i = 0
            for ind_year in xrange(min_year,max_year+1):
                    for ind_month in xrange(1,13):
                        nor_monthly[i] = sum(rain_daily[(year == ind_year) & (month == ind_month)]>threshold)
                        i += 1  
            return nor_monthly
        elif season == 'yearly':
            # yearly distribution of rainy days
            nor_yearly = np.zeros((max_year - min_year +1,1))
            i = 0
            for ind_year in xrange(min_year,max_year+1):
                nor_yearly[i] = sum(rain_daily[year == ind_year]>threshold)
                i += 1  
            return nor_yearly