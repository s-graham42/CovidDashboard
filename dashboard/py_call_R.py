""" A class for calling custom R scripts that process various API calls and produce csv files. """

import os
import pandas as pd
from covid_project.settings import BASE_DIR

class PyCallR:
    """ Our main python/R interface class.

    This class holds all the R script calls for the processing and writing of
    csv files for use in the display of information in the dashboard charts.
    
    Attributes:
    - script_directory: File Path to R Scripts this class can call. (String)
    - csv_directory: File Path to destination folder for processed .csv files. (String)
    """

    script_directory = BASE_DIR + "/Transparency/Py_call_R_project"
    csv_directory = BASE_DIR + "/media/current_api_data"


    @classmethod
    def get_new_nyt_states(self):
        """ Get a new set of New York Times Cocid-19 data for all U.S. Territories.
        
        Runs the R script 'NYT_Territory_Data_Processing.R', which:
        Pulls API data from New york Times, and processes it.
        Overwrites NYT_States.csv with current processed data.

        Returns:
            A Pandas DataFrame read from the resultant csv file.
        """

        script_to_run = self.script_directory + "/NYT_Territory_Data_Processing.R"
        file_to_save = self.csv_directory + "/NYT_States.csv"
        os.system("Rscript " + script_to_run + " " + file_to_save + " " + self.script_directory)

        return pd.read_csv(file_to_save, parse_dates=True).sort_values(by=['date'])


    @classmethod
    def get_new_nyt_us(self):
        """ Get a new set of New York Times data of US Covid-19 Totals.
        
        Runs the R script 'NYT_US_Data_Processing.R', which:
        Pulls API data from New york Times, and processes it.
        Overwrites NYT_States.csv with current processed data.

        Returns:
            A Pandas DataFrame read from the resultant csv file.
        """

        script_to_run = self.script_directory + "/NYT_US_data_processing.R"
        file_to_save = self.csv_directory + "/NYT_US.csv"
        os.system("Rscript " + script_to_run + " " + file_to_save + " " + self.script_directory)

        return pd.read_csv(file_to_save, parse_dates=True).sort_values(by=['date'])


    @classmethod
    def get_new_cdc_states(self):
        """ Get a new set of CDC data for all U.S. Territories.
        
        Runs the R script 'CDC_Territory_Data_Processing.R', which: 
        Pulls API data from New york Times, and processes it.
        Overwrites CDC_States.csv with current processed data.

        Returns:
            A Pandas DataFrame read from the resultant csv file.
        """

        script_to_run = self.script_directory + "/CDC_Territory_Data_Processing.R"
        file_to_save = self.csv_directory + "/CDC_States.csv"
        os.system("Rscript " + script_to_run + " " + file_to_save + " " + self.script_directory)

        return pd.read_csv(file_to_save, parse_dates=True).sort_values(by=['date'])

