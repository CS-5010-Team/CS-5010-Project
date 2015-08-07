# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 10:10:57 2015

@author: juan
"""
from numpy import *
import pandas as pd

MONTH = {"january":'01', "febuary":'02',"march":'03',"april":'04',"may":'05',
         "june":'06', "july":'07', 'august':'08', 'september':'09', 
         "october":'10', 'november':'11', 'december':'12'}

grid = pd.read_csv('gridwatch.csv',header=0)
grid.columns = grid.columns.str.strip()

def extract_year(year):
    return grid[grid["timestamp"].str.contains(str(year))]
    
def month_day_year_variable(month, day, year, variable):
    """
        
    
    """
    month = month.lower()
    day = str(day)
    if day[0] != '0' and len(day) == 1:
        day = '0'+str(day)
     
    date_string = "" + str(year)+'-'+MONTH[month]+'-'+day
    print(date_string)
    return grid[grid["timestamp"].str.contains(date_string)][variable]
    
print("hello, nerds")
    
        
                                                   
   
    
