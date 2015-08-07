from numpy import *
import pandas as pd
import datetime

#read in the file
df = pd.read_csv("gridwatch-small.csv", header = 0)

#strip the space in names of column
#aka: clean the data
df.columns = df.columns.str.strip()
 
#input a date and return all the rows for that day
time_lookingfors = input("Input the time in the format YYYY-MM-DD(seperate by ','):")
time_lookingfor = [y.strip() for y in time_lookingfors.split(',')]
s = df[df['timestamp'].str.contains('|'.join(time_lookingfor))]

#input the columns you need
titles = input("Input the title you are looking for(seperate by ',') or type 'all': ")
if (titles == 'all'):
	s = s[s.columns.values]
else:
	title_lookingfor = [x.strip() for x in titles.split(',')]
	s = s[title_lookingfor]
print(s)
