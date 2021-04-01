from covid_project.settings import BASE_DIR # may need this wherever we use these calls
import os
import pandas as pd

os.getcwd()
os.chdir('C:\Users\toast\Documents\CodingDojo\python_stack\CovidDashboard\covid_project\csv_files')
os.system('Rscript Cumu_To_Daily_NYT.R')
os.system('Rscript NYT_US_data_processing.R')

NYT_US_states = pd.read_csv('NYT.csv')

NYT_US = pd.read_csv('NYT_US.csv')