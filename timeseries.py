# -*- coding: utf-8 -*-
"""
Created on Mon Aug 10 21:11:45 2015

@author: juan
"""
from numpy import *
import pandas as pd

df = pd.read_csv("gridwatch.csv", header = 0)
# strip column headers of trailing whitespace
df.columns = df.columns.str.strip()
# reindex the dataframe as a DatetimeIndex timeseries
df.index = pd.to_datetime(df.timestamp)