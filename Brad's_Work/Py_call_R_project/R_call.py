import os
import pandas as pd

os.getcwd()
os.chdir('C:\Users\toast\Documents\CodingDojo\python_stack\CovidDashboard\covid_project\csv_files')
os.system('Rscript Cumu_To_Daily_NYT.R')

NYT_data = pd.read_csv('NYT.csv')