""" A class for calling custom R scripts that process various API calls and produce csv files. """

import os
import pandas as pd
from covid_project.settings import BASE_DIR

class PyCallR:
    """ The main python/R interface class.

    This class holds all the R script calls for the processing and writing of
    csv files for use in the display of information in the dashboard charts.
    
    """

    def __init__(self):
        """ Initializes the class with the location of the scripts and the 
        location to save the resultant csv files. """
        
        self.script_location = BASE_DIR + "/Brad's_Work/Py_call_R_project"
        self.csv_location = BASE_DIR + "/media/current_api_data"

    def get_new_nyt_states(self):
        """ Get a new set of New York Times data for all U.S. Territories.
        
        Runs the R script 'NYT_Territory_Data_Processing.R', which:
        Pulls API data from New york Times, and processes it.
        Overwrites NYT_States.csv with current processed data.

        Returns:
            A Pandas DataFrame read from the resultant csv file.
        """

        script_to_run = self.script_location + "/NYT_Territory_Data_Processing.R"
        file_to_save = self.csv_location + "/NYT_States.csv"
        os.system("Rscript " + script_to_run + " " + file_to_save)

        return pd.read_csv(file_to_save, parse_dates=True).sort_values(by=['date'])
    
# # Path to R script.
# a = BASE_DIR + "/Brad's_Work/Py_call_R_project/NYT_Territory_Data_Processing.R"

# # Path to directory in which the produced CSV should be placed and where it can be retrieved.
# b = "/Users/neo/Drive/Python/WuFlu_Dashboard/WuFlu_Sandbox/WD_Sandbox/Test_Folder/NYT_States.csv"

# os.system("Rscript " + a + " " + b)
# NYT_States = pd.read_csv(b)

    def get_new_nyt_states(self):
        """ Get a new set of New York Times data of US Totals.
        
        Runs the R script 'NYT_US_Data_Processing.R', which:
        Pulls API data from New york Times, and processes it.
        Overwrites NYT_States.csv with current processed data.

        Returns:
            A Pandas DataFrame read from the resultant csv file.
        """

        script_to_run = self.script_location + "/NYT_US_Data_Processing.R"
        file_to_save = self.csv_location + "/NYT_US.csv"
        os.system("Rscript " + script_to_run + " " + file_to_save)

        return pd.read_csv(file_to_save, parse_dates=True).sort_values(by=['date'])

# # Path to R script
# a = "/Users/neo/Drive/Python/WuFlu_Dashboard/WuFlu_Sandbox/WD_Sandbox/NYT_US_Data_Processing.R"

# # Path to directory in which the produced CSV should be placed and where it can be retrieved.
# b = "/Users/neo/Drive/Python/WuFlu_Dashboard/WuFlu_Sandbox/WD_Sandbox/Test_Folder/NYT_US.csv"

# os.system("Rscript " + a + " " + b)
# NYT_US = pd.read_csv(b)

    def get_new_cdc_states(self):
        """ Get a new set of CDC data for all U.S. Territories.
        
        Runs the R script 'CDC_Territory_Data_Processing.R', which: 
        Pulls API data from New york Times, and processes it.
        Overwrites CDC_States.csv with current processed data.

        Returns:
            A Pandas DataFrame read from the resultant csv file.
        """

        script_to_run = self.script_location + "/CDC_Territory_Data_Processing.R"
        file_to_save = self.csv_location + "/CDC_States.csv"
        os.system("Rscript " + script_to_run + " " + file_to_save + " " + self.script_location)

        return pd.read_csv(file_to_save, parse_dates=True).sort_values(by=['date'])


# # Path to R script
# a = "/Users/neo/Drive/Python/WuFlu_Dashboard/WuFlu_Sandbox/WD_Sandbox/CDC_Territory_Data_Processing.R"

# # Path to directory in which the produced CSV should be placed and where it can be retrieved.
# b = "/Users/neo/Drive/Python/WuFlu_Dashboard/WuFlu_Sandbox/WD_Sandbox/Test_Folder/CDC_States.csv"

# # Working directory for current R script.
# c = "/Users/neo/Drive/Python/WuFlu_Dashboard/WuFlu_Sandbox/WD_Sandbox"

# os.system("Rscript " + a + " " + b + " " + c)
# NYT_US = pd.read_csv(b)