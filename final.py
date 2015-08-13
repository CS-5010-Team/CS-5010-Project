# coding: utf-8

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#for regular expression string manipulation:
import re

sources = ['coal','nuclear','hydro','wind','ccgt','ocgt','pumped','oil','other']
connectors = ['french_ict','dutch_ict','irish_ict','ew_ict']
remove = ['id']
timestamp = 'timestamp'


def main():
    print("\n********************************************************")
    print("\n**     WELCOME TO THE ENERGY GRID DATA EXPLORER  !    **")
    print("\n********************************************************")
    print("\nINITIALIZING............")
    #Get a valid source filename
    input_file = get_filename()

    #Create a pandas dataframe and clean up column headers
    df = read_data(input_file)
    print("\nDONE!\n")
    #Print contents
    print("\nYou have imported " + str(len(df)) + " observations for the variables " + str(df.columns.values) + ".\n")

    #Convert date/time strings to pandas datetime object and use these as the data frame indices.
    #This allows for convenient subsetting and timeseries analysis.
    df = convert_time(df)

    for n in range(0,len(remove)):    
        try:
            df = df.drop(remove[n],1)
        except:
            continue
    
    #The next block of code reduces the imported data to a smaller data set of the user's choosing to speed up computations,
    #And then allows the user to select from a menu of analyses and plots to perform on the subsetted data


    while True:
        subset = get_subset(df)

        #Choose an (possibly more than 1) analysis to perform from a menu of options:
        while True:
            make_plot = input("\nWould you like to generate a new plot or analysis('y' or 'n')?\n")
            make_plot = (make_plot.strip()).lower()
            if make_plot == 'y':
                plot_menu(subset)
            else:
                break
     
        #Finally, output to a file:
        make_csv = input("\nWould you like to export the data subset to a csv file('y' or 'n')?\n")
        make_csv = (make_csv.strip()).lower()
        if make_csv == 'y':
            output_file = input("Please enter a filename for output (or press enter for 'extract.csv'):")
            if output_file == '':
                output_file = 'extract.csv'
            subset.to_csv(output_file, sep = ',')

        
        #Choose another subset or quit?
        subset_again = input("\nWould you like to select another subset for analysis('y' or 'n')?\n")
        subset_again = (subset_again.strip()).lower()
        if not(subset_again == 'y'):
            break


    
    #Import another file or quit?
    import_again = input("\nWould you like to import another data set('y' or 'n')?\n")
    import_again = (import_again.strip()).lower()
    if import_again == 'y':
        main()
    print("\n********************************************************")
    print("\n**       THANKS FOR USING THIS APPLICATION!           **")
    print("\n********************************************************")


# In[9]:

# This cell Contains all the functions for taking valid user input

def get_filename():
    #Try to get a valid filename 3 times
    num_tries = 0

    while (num_tries < 3):
        try:
            filename = input("Input the path to the csv file:\n")
            with open(filename,'r') as f:
                f.close()
            break
        except:
            print("The specified path does not exist.  Please try again.")
            num_tries += 1
            continue

    return filename



def get_date_range(min_date,max_date):
#Take user input for a valid date range (within bounds set by min_date, max_date).  Return a 2-tuple of datetime objects
    print("Input start date between " + str(min_date.year) + "-" + str(min_date.month) + "-" + str(min_date.day) +
           " and " + str(max_date.year) + "-" + str(max_date.month) + "-" + str(max_date.day) + ":")
    print("(empty input returns min or max available date.)")

    while True:
        start_date = get_date()
        if start_date == '':
            start_date = min_date
            break
        elif min_date <= start_date <= max_date:
            break
        print("Start date out of range.  Try again:")

    print("Input end date between " + str(start_date.year) + "-" + str(start_date.month) + "-" + str(start_date.day) +
           " and " + str(max_date.year) + "-" + str(max_date.month) + "-" + str(max_date.day) + ":")
    print("(empty input returns min or max available date.)")

    while True:
        end_date = get_date()
        if end_date == '':
            end_date = max_date
            break
        elif start_date <= end_date <=max_date:
            break
        print("End date out of range.  Try again:", end="")

    return (start_date,end_date)



def get_date():
#Input a date that parses correctly as a pandas datetime object
    while True:
        date = input();
        if date == '':
            return ''
        try:
            datetime = pd.to_datetime(date)
            #Was pandas able to convert to a datetime object?  If not, output may be a string.
            if type(datetime)==str:
                raise TypeError
            break
        except:
            print("Invalid date. Try again.")
            continue
        
    return datetime


def get_var_names(frame):
#Takes comma-separated strings and removes any that aren't variable names in frame
    var_names = []

    #Try until you get a valid variable name
    while len(var_names)==0:
        var_string = input()

        #clean up the input
        var_names = var_string.split(',')
        var_names = [x.strip() for x in var_names]
    
        # check for pre-defined input 
        if var_names[0] == 'all':
            var_names = frame.columns.values
        elif var_names[0] == 'sources':
            var_names = sources
        elif var_names[0] == 'connectors':
            var_names = connectors
            
        bad_names = [] # store bad variable names
        
        # check for bad variable names
        for name in var_names:
            if name not in frame.columns.values:
                print(name + " is not a valid variable.")
                bad_names.append(name)
            
        # remove any bad variable names we might have found
        for name in bad_names:
            print("removing " + name)
            var_names.remove(name)
        
        # if nothing left in var_names let the user know!
        if len(var_names)==0:
            print("No valid variables were entered. Try again", end="")
    
    return var_names


def get_frequency():
    while True:
        frequency = input()
        frequency = (frequency.lower()).strip()    
        frequency = re.findall(r'^[0-9]* *[mdh]',frequency)
        try:
            frequency = frequency[0]
            frequency = re.sub('m','min',frequency)
            timedelta = pd.to_timedelta(frequency)
            break
        except:
            print("Invalid frequency. Try again.",end="")
            continue
    
    return frequency


def plot_menu(frame):
    print("\nWhat kind of plot or analysis would you like to generate?")
    print("--- 1 --- Bar Chart with summary stats\n--- 2 --- Time series line graph\n" +
          "--- 3 --- Covariance matrix with heatmap\n--- 4 --- Autocorrelation with variable lag")
    
    while True:
        option = input("\nChoose an option:")
        option = option.strip()

        if option == "-1" :
            return
        elif option == "1":
            print("\nWhich variables would you like to include?")
            print("Please choose from " + str(frame.columns.values) + ".\n" +
                  "List individual variables or type 'all', 'sources' or 'connectors'.")
            var_names = get_var_names(frame)
            bar_chart(frame, var_names)
            return
        elif option == "2":
            print("\nWhich variables would you like to plot?")
            print("Please choose from " + str(frame.columns.values) + ".\n" +
                  "List individual variables or type 'all', 'sources' or 'connectors'.")
            var_names = get_var_names(frame)
            line_plot(frame, var_names)
            return
        elif option == "3":
            print("\nWhich variables would you like to compute covariances for?")
            print("Please choose from " + str(frame.columns.values) + ".\n" +
                  "List individual variables or type 'all', 'sources' or 'connectors'.")
            var_names = get_var_names(frame)
            corr_matrix = correlation_matrix(frame, var_names)
            return
        elif option == "4":
            print("This function plots autocorrelation for selected variables over a range of lags.\n" +
                  "Note: data should be resampled for this analysis to be valid")
            print("\nWhich variables would you like to compute autocorrelations for?")
            print("Please choose from " + str(frame.columns.values) + ".\n" +
                  "List individual variables or type 'all', 'sources' or 'connectors'.")
            var_names = get_var_names(frame)
            print("Minimum lag?")
            min_lag = get_frequency()
            print("Max multiple of lags(positive int)?")
            num_lags = int(input())
            auto_correlations = auto_correlation(frame, var_names, min_lag, num_lags)
            return
        else:
            print("Invalid input.  Try again.")


# In[14]:

# This cell has the plotting functions
def line_plot(frame, var_names):
    frame.plot(frame.index, var_names, label=var_names)
    plt.legend(loc='center left', bbox_to_anchor=(1,.5))
    plt.show()


def correlation_matrix(frame, var_names):
    corr_matrix = frame[var_names].corr()
    print("Correlation matrix:")
    print(corr_matrix)
    
    show_heatmap = input("Would you like to view the results as a heatmap?('y' or 'n')\n")
    show_heatmap = (show_heatmap.lower()).strip()
    if show_heatmap == 'y':
        column_labels = var_names
        row_labels = var_names

        #using matplotlib as plt        
        fig, ax = plt.subplots()
        heatmap = ax.pcolor(corr_matrix, cmap='RdBu', vmin=-1, vmax=1)
        
        # put the major ticks at the middle of each cell
        ax.set_xticks(np.arange(corr_matrix.shape[0])+0.5, minor=False)
        ax.set_yticks(np.arange(corr_matrix.shape[1])+0.5, minor=False)
        
        # legend.  tick labels -1 to 1 by .2
        colorbar = plt.colorbar(heatmap)
        colorbar.ax.set_yticklabels([(x-5)/5 for x in list(range(0,11))])
        colorbar.set_label('correlation coefficient', rotation=270)

        # labels
        ax.set_xticklabels(row_labels, minor=False)
        ax.set_yticklabels(column_labels, minor=False)
        
        plt.show()
        
    return corr_matrix
        

def bar_chart(frame, var_names):
    desc = frame.describe()
    print("Summary statistics:")
    print(desc)

    x_vals=np.arange(len(var_names))
    # means as bar heights
    heights = (desc[desc.index == 'mean'].get_values())[0]
    std_devs = (desc[desc.index == 'std'].get_values())[0]
    bar_width = 0.7
    plt.bar(x_vals, height=heights, width=bar_width, label=var_names, alpha=.5, yerr=std_devs)
    plt.xticks(x_vals+bar_width/2, var_names)
    plt.show()
    

def auto_correlation(frame, var_names, min_lag, num_lags):
    min_lag = pd.to_timedelta(min_lag)
    # Get avg period from frame.  If resampled, this will simply be the resampling period.
    frame_delta = (frame.index[len(frame.index)-1]-frame.index[0])/len(frame.index)
    # These timedelta objects will serve as labels in a plot if printed.
    labels = [pd.to_timedelta(n*min_lag) for n in range(1,num_lags+1)]
    # Compute expected number of rows for each lag.  This is necessary because pd.autocorr() takes only row# index lags.
    lags = [int(round(labels[n]/frame_delta)) for n in range(0,len(labels))]
    
    # Generate a dataframe with entries for each lag and each var (rows, cols respectively), and timedelta indices
    auto_correlations = pd.DataFrame(index=labels,columns=var_names)
    for var_name in auto_correlations.columns:
        auto_correlations[var_name] = [frame[var_name].autocorr(lag=lags[n]) for n in range(0,len(auto_correlations))]
    
    print(auto_correlations)

#    We tried to plot the autocorrelations on a line graph with lag on the x axis but kept getting MemoryError, 
#    coming out of the pandas code    
#    show_linegraph = input("Would you like to view the results on a linegraph?('y' or 'n')\n")
#    show_linegraph = (show_linegraph.lower()).strip()
#    if show_linegraph == 'y':
#        line_plot(auto_correlations,auto_correlations.columns)
        
    return auto_correlations


# In[11]:

# This cell has the data generation/manipulation functions

def read_data(filename):
    #read in the file
    frame = pd.read_csv(filename, header = 0)

    #strip the leading/trailing space in column names and be sure all letters are lower case
    frame.columns = (frame.columns.str.strip()).str.lower()

    return frame



def convert_time(frame):
    #convert timestamps to datetime objects to use as row indices
    frame[timestamp] = pd.to_datetime(frame[timestamp])
    
    #use datetime objects as row indices.  This will allow convenient subsetting and timeseries ops later.
    frame.index = frame[timestamp]
    
    #delete the old timestamps
    del frame[timestamp]

    return frame



def remove_outliers(frame, var_names, threshold):
    for var in var_names:
        SD = frame[var].std()
        mean = frame[var].mean()
        outlier_indices = (abs(frame[var]-mean)/SD > threshold)
        frame[var][outlier_indices] = None
        print(str(sum(outlier_indices)) + " observations were removed from " + var)
    
    return frame



def get_subset(df):
    # This function allows the user to select a subset of variables and a date range, then allows the user to
    # remove outliers from a chosen set of vars and resample the timeseries data at a chosen time interval.

    print("********************************************************")
    print("\nEXTRACT DATA FROM DATASET............ \n")

    #Get a valid date range for subsetting
    #First get upper and lower bounds
    min_date = df.index[0]
    max_date = df.index[len(df.index)-1]
    #convert these to datetime objects with all hour, minute, second data set to 0 (so that partial days at start/end may be selected)
    min_date = pd.to_datetime(pd.datetime(min_date.year,min_date.month,min_date.day))
    max_date = pd.to_datetime(pd.datetime(max_date.year,max_date.month,max_date.day))
    #make sure the datetime indices are monotonically increasing
    df.sort_index()
    #and take input
    date_range = get_date_range(min_date,max_date)
    
    #Now subset on the chosen date range. First, pull out date strings that can be used as indices:
    #Now subset on the chosen date range
    start_date = date_range[0]
    end_date = date_range[1]
    subset = df[str(start_date):str(end_date)]

    #Select vars for analysis and subset:
    print("\nWhich variables are you interested in?")
    print("Available variables are:\n " + str(subset.columns.values) + ".\n" +
          "List individual variables or type 'all', 'sources' or 'connectors'.")
    var_names = get_var_names(subset)
    print("You chose "+ str(var_names))
    #Then subset on these vars:
    subset = subset[var_names]

    #Remove outliers
    rm_outliers = input("\nWould you like to remove outliers('y' or 'n')?\n")
    rm_outliers = (rm_outliers.strip()).lower()
    n_obs = len(subset.index)
    if rm_outliers == 'y':
        print("\nFor which variables would you like to remove outliers?")
        print("Available variables are:\n " + str(subset.columns.values) + ".\n" +
              "List individual variables or type 'all', 'sources' or 'connectors'.")
        var_names = get_var_names(subset)
        threshold = input("Threshold for elimination (SD's from the mean)?")
        subset = remove_outliers(subset,var_names,float(threshold))

    #Resample
    resample = input("\nWould you like to resample the data('y' or 'n')?\n")
    resample = (resample.strip()).lower()
    if resample == 'y':
        #Avg frequency for display- (max time - min time)/(# samples)
        avg_freq = (subset.index[len(subset.index)-1]-subset.index[0])/len(subset.index)
        print("At what frequency would you like to resample the time series?" +
              "\n(input 'n t' where t = 'm', 'h', or 'd' for units and n is the number of units)\n" +
              "current average frequency is " + str(avg_freq) + '.')
        #Get a valid frequency, eg '1 d', '6 h', '30 m'
        frequency = get_frequency()
        #And finally, resample
        subset = subset.resample(frequency,closed='left',label='left',how='mean')

    print("\nDATA EXTRACTION SUCCESSFUL!\n")
    print("********************************************************")
    
    return subset


if __name__ == "__main__":
    main()



