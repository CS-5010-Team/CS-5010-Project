import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def line_plot(s):
	var_names = input("The trend for what variable you want to see?(seperate by ',') ")
	var_name = [x.strip() for x in var_names.split(',')]

	s.plot("timestamp", var_name, label=var_name)
	plt.legend()
	plt.show()

	menu(s)
	return

def pie_chart(s):
	ans = s.sum(axis=0)
	plt.pie(ans.get_values(), labels=ans.keys(), autopct='%1.1f%%')
	plt.axis('equal')
	plt.show()
	
	menu(s)
	return


def menu(s):
	print("\nThis is the menu for analysis: ")
	print("     1 --- Line chart with timestamp ")
	print("     2 --- Pie chart the consumption in that date ")

	option = input("\nType in the number or -1 to quit: ")

	if option == "-1" : 
		return
	elif option == "1":
		line_plot(s)
	elif option == "2":
		pie_chart(s)
	else:
		return

	return


def beginning():
	#read in the file
	print("\nWELCOME TO THE UK ENERGY COMSUMPTION!")
	print("\n********************************************************")
	print("\nINITIALING............")
	df = pd.read_csv("gridwatch-small.csv", header = 0)

	#strip the space in names of column
	#aka: clean the data
	df.columns = df.columns.str.strip()
	print("\nDONE!\n")
 
	#input a date and return all the rows for that day
	print("********************************************************")
	print("\nEXTRACT DATA FROM DATASET............ \n")
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
	

	#save the dataframe to a new .csv file
	#print(s)
	s.to_csv("extract.csv", sep = ',')
	print("\nEXTRACT SUCCEFULLY!!\n")
	print("********************************************************")
	menu(s);

	return

#The entire program starts here.
beginning()

