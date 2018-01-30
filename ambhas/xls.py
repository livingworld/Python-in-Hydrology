# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 16:49:46 2011

@author: Sat Kumar Tomer
@website: www.ambhas.com
@email: satkumartomer@gmail.com
"""

import xlrd, xlwt
import numpy as np

class xlsread():
    """
    A class to read data from xls file
    based on the 'xlrd'
    """
    
    def __init__(self, fname):
        self.fname = fname
                
    def get_cells(self, cell_range, sheet):
        """
        cell_range: a single cell i.e. 'a2'
                    range of cells i.e. 'a2:f5'
        sheet:  name of the sheet, must be string
        """
        
        book = xlrd.open_workbook(self.fname)
        sheet = book.sheet_by_name(sheet)
        
        if ':' not in cell_range:
            foo1 = cell_range
            row,col = self.__cell2ind__(foo1)
            data = sheet.cell_value(row,col)
        else:
            foo1, foo2 = cell_range.split(':')
            row1,col1 = self.__cell2ind__(foo1)
            row2,col2 = self.__cell2ind__(foo2)
            
            if row2<row1:
                raise Exception('row_start should be <= row_end')
            if col2<col1:
                raise Exception('col_start should be <= col_end')
            
            data = []
            for i in range(row1,row2+1):
                data_row = []
                for j in range(col1,col2+1):
                    data_row.append(sheet.cell_value(i,j))
                    
                data.append(data_row)
            
        return np.array(data)

    def __cell2ind__(self,foo):
        """
        given the cell number i.e. (AA100)
        returns the row and column of cell in indices format i.e. 0,10
        """
        
        # if the column is less than Z
        foo_str = foo[0].lower()
        col = ord(foo_str)-ord('a')
        
        # if the column is more than Z, i.e. AA
        try:
            row = int(foo[1:])-1
        except:
            row = int(foo[2:])-1
            foo_str = foo[1].lower()
            col = (col+1)*26+ ord(foo_str)-ord('a')
        
        return row, col


class xlswrite():
    
    def __init__(self, data, cell_start, sheet):
        self.data = data
        self.cell_start = cell_start
        
        # initialize the xlrt     
        book = xlwt.Workbook()
        sheet = book.add_sheet(sheet)
        
        # convert into row and col        
        row, col = self.__cell2ind__(cell_start)
        
        if isinstance(data, str)  or isinstance(data, float) or isinstance(data,int):
            sheet.write(row,col,data)
                
        if data.ndim == 1:
            for i in range(data.shape[0]):
                sheet.write(row+i,col, data[i])
                
        else:
            for i in range(data.shape[0]):
                for j in range(data.shape[1]):
                    sheet.write(row+i, col+j, data[i,j])
        
        self.book = book
    
    def save(self, fname):
        self.book.save(fname)
    
    
    def __cell2ind__(self, foo):
        """
        given the cell number i.e. (AA100)
        returns the row and column of cell in indices format i.e. 0,10
        """
        
        # if the column is less than Z
        foo_str = foo[0].lower()
        col = ord(foo_str)-ord('a')
        
        # if the column is more than Z, i.e. AA
        try:
            row = int(foo[1:])-1
        except:
            row = int(foo[2:])-1
            foo_str = foo[1].lower()
            col = (col+1)*26+ ord(foo_str)-ord('a')
        
        return row,col
        
if __name__ == "__main__":
    
    # read the data
    fname = '/home/tomer/rain_projection/raw_data/a2_0.5.xls'
        
    foo = xlsread(fname)
    var = foo.get_cells('a3:a5', 'Sheet1')
    
    book = xlrd.open_workbook(fname)
    sheet = book.sheet_by_name('Sheet1')
    sheet.cell_value(0,0)    
    
    print var
    
    # write the data
    var = np.array([[5,10,12],[2,5,6]])
    foo1 = xlswrite(var, 'f10', 'Sheet1')
    fname = '/home/tomer/data.xls'
    foo1.save(fname)
    
    

