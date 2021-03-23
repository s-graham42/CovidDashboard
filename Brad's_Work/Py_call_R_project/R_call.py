import os

os.getcwd()
os.chdir('/Users/neo/Drive/Python/WuFlu Dashboard/WuFlu Sandbox/API Sandbox')
os.system('Rscript Get_us-states_githubrepo_NYT.R')
os.system('Rscript cumu_to_daily_deaths_NYT.R')
os.system('Rscript cumu_to_daily_cases_NYT.R')