# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 18:35:39 2015

@author: Mason
"""

import pandas as pd
import numpy as np
import statsmodels.formula.api as sm

df = pd.read_csv("gridwatch.csv")

result = sm.ols(formula="df.demand ~ Month + Hour + Weekday", data=df).fit()
print(result.params)
print(result.summary())

df["Monthc"] = df["Month"].astype('str')
df["Hourc"] = df["Hour"].astype('str')
df["Weekdayc"] = df["Weekday"].astype('str')

result2 = sm.ols(formula="df.demand ~ Monthc + Hourc + Weekdayc", data=df).fit()
print(result2.params)
print(result2.summary())

df.Month

#not needed anymore, I don't think
def regress(data, yvar, xvars):
    Y = data[yvar]
    X = data[xvars]
    X['intercept']=1.
    result = sm.OLS(Y, X).fit()
    return result.params
    
result = sm.OLS('demand', 'Month').fit()
print (result.params)