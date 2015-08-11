# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 04:06:07 2015

@author: matt
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#for regular expression string manipulation:
import re




def line_plot(frame):

    print("\nWhich variables would you like to plot?")
    var_names = get_var_names(frame)

    print("At what frequency would you like to resample the time series?" +
          "\n('n t' where t = 'm', 'h', or 'd' for units and n is the number of units)")
    frequency = get_frequency()
 
    resampled = frame.resample(frequency,closed='left',label='left',how='mean')

    frame.plot(frame.index, var_names, label=var_names)
    plt.legend()
    plt.show()

    return




def covariance_matrix(s):
    return




def auto_correlation(s):
    return




def plot_menu(frame):
    print("\nWhat kind of plot would you like to generate?")
    print("--- 1 --- Time series line graph \n--- 2 --- Covariance matrix\n--- 3 --- Autocorrelation plot")

    while True:
        option = input("\nChoose an option:")
        option = option.strip()

        if option == "-1" :
            return
        elif option == "1":
            line_plot(frame)
            return
        elif option == "2":
            covariance_matrix(frame)
            return
        elif option == '3':
            auto_correlation(frame)
            return
        else:
           print("Invalid input.  Try again.")




def get_frequency():
    while True:
        frequency = input()
        frequency = (frequency.upper()).strip()    
        frequency = re.findall(r'^[0-9]* *[MDH]',frequency)
        try:
            frequency = frequency[0]
            frequency = re.sub('M','min',frequency)
            break
        except:
            print("Invalid frequency. Try again.")
            continue
    
    return frequency



def get_var_names(frame):
#Takes comma-separated strings and removes any that aren't variable names in frame
    var_names = []

    #Try until you get a valid variable name
    while len(var_names)==0:
        var_string = input()

        #clean up the input
        var_names = var_string.split(',')
        var_names = [x.strip() for x in var_names]
    
        #Take out bad variable names
        for name in var_names:
            if not(name in frame.columns):
                print(name + " is not a valid variable.")
                var_names.remove(name)

        if len(var_names)==0:
            print("No valid variables were entered.")
 
    return var_names




def get_date():
#Input a date that parses correctly as a pandas datetime object
    while True:
        date = input();
        #Regular expression for the requested date format
        date = re.findall(r'^ *[0-9]{4}-[0-9]{1,2}-[0-9]{1,2} *$', date)
        try:
            datetime = pd.to_datetime(date[0])
            #Was pandas able to convert?  If not, output may be a string.
            if type(datetime)==str:
                raise TypeError
            break
        except:
            print("Invalid date. Try again.")
            continue
        
    return datetime




def get_date_range(min_date,max_date):
#Take user input for a valid date range (within bounds set by min_date, max_date).  Return a 2-tuple of datetime objects
    print("Input start date between " + str(min_date.year) + "-" + str(min_date.month) + "-" + str(min_date.day) +
           " and " + str(max_date.year) + "-" + str(max_date.month) + "-" + str(max_date.day) + ":",end='')
    while True:
        start_date = get_date()
        if min_date <= start_date <= max_date:
            break
        print("Start date out of range.  Try again:")

    print("Input end date between " + str(start_date.year) + "-" + str(start_date.month) + "-" + str(start_date.day) +
           " and " + str(max_date.year) + "-" + str(max_date.month) + "-" + str(max_date.day) + ":",end='')
    while True:
        end_date = get_date()
        if start_date <= end_date <=max_date:
            break
        print("End date out of range.  Try again:")

    return (start_date,end_date)




def convert_time(frame):
    #get timestamp column
    print("Which column name corresponds to the timestamp?", end="")
    timestamp = get_var_names(frame)
    timestamp = timestamp[0]

    #convert timestamps to datetime objects and use as row indices
    frame[timestamp] = pd.to_datetime(frame[timestamp])
    
    #use datetime objects as row indices.  This will allow convenient subsetting and timeseries ops later.
    frame.index = frame[timestamp]
    
    #delete the old timestamps
    del frame[timestamp]

    return frame
    



def read_data(filename):
    #read in the file
    frame = pd.read_csv(filename, header = 0)

    #strip the leading/trailing space in column names and be sure all letters are lower case
    frame.columns = (frame.columns.str.strip()).str.lower()

    return frame




def get_filename():
    #Try to get a valid filename 3 times
    num_tries = 0

    while (num_tries < 3):
        try:
            filename = input("Input the path to the csv file:")
            with open(filename,'r') as f:
                f.close()
            break
        except:
            print("The specified path does not exist.  Please try again.")
            num_tries += 1
            continue

    return filename



def main():
    #Get a valid source filename
    input_file = get_filename()

    #Create a pandas dataframe and clean up column headers
    df = read_data(input_file)

    #Print contents
    print("\nYou have imported " + str(len(df)) + " observations for the variables " + str(df.columns.values) + ".\n")

    #Convert date/time strings to pandas datetime object and use these as the data frame indices.
    #This allows for convenient subsetting and timeseries analysis.
    df = convert_time(df)

    #Get a valid date range for subsetting
    #First get upper and lower bounds
    min_date = df.index[0]
    max_date = df.index[len(df.index)-1]
    #convert these to datetime objects with all hour, minute, second data set to 0 (so that partial days and start and end may be selected)
    min_date = pd.to_datetime(pd.datetime(min_date.year,min_date.month,min_date.day))
    max_date = pd.to_datetime(pd.datetime(max_date.year,max_date.month,max_date.day))
    #and take input
    date_range = get_date_range(min_date,max_date)

    #Now subset on the chosen date range. First, pull out date strings that can be used as indices:
    #Now subset on the chosen date range
    start_date = date_range[0]
    end_date = date_range[1]
    start_str = str(start_date.year) + '-' + str(start_date.month) + '-' + str(start_date.day)
    end_str = str(end_date.year) + '-' + str(end_date.month) + '-' + str(end_date.day)
    #Then take the subset
    subset = df[start_str:end_str]

    #Now select vars for analysis:
    print("\nInput variables to select for analysis.")
    print("Available variables are:\n " + str(subset.columns.values) + ".")
    var_names = get_var_names(subset)
    #Then subset on these vars:
    subset = subset[var_names]

    #Choose an (possibly more than 1) analysis to perform from a menu of options:
    while True:
        make_plot = input("Would you like to generate a new plot('y' or 'n')?")
        make_plot = (make_plot.strip()).lower()
        if make_plot == 'y':
            plot_menu(subset)
        else:
            break

    #Finally, output to a file:
    make_csv = input("Would you like to export the data subset to a csv file('y' or 'n')?")
    make_csv = (make_csv.strip()).lower()
    if make_csv == 'y':
        subset.to_csv("extract.csv", sep = ',')

    #Start another import or quit?
    import_again = input("Would you like to import another file('y' or 'n')?")
    import_again = (import_again.strip()).lower()
    if import_again == 'y':
        main()
    
    return


   
#Execute
main()

