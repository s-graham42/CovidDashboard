
import os
import pandas as pd

# Path to R script.
a = "/Users/neo/Drive/Python/WuFlu_Dashboard/WuFlu_Sandbox/WD_Sandbox/NYT_Territory_Data_Processing.R"

# Path to directory in which the produced CSV should be placed.
b = "/Users/neo/Drive/Python/WuFlu_Dashboard/WuFlu_Sandbox/WD_Sandbox/Test_Folder"

# Path for CSV imporation into a dataframe.
c = "/Users/neo/Drive/Python/WuFlu_Dashboard/WuFlu_Sandbox/WD_Sandbox/Test_Folder/NYT_States.csv"

os.system("Rscript " + a + " " + b)
NYT_States = pd.read_csv(c)

# Path to R script
a = "/Users/neo/Drive/Python/WuFlu_Dashboard/WuFlu_Sandbox/WD_Sandbox/NYT_US_Data_Processing.R"

# Path to directory in which the produced CSV should be placed.
b = "/Users/neo/Drive/Python/WuFlu_Dashboard/WuFlu_Sandbox/WD_Sandbox/Test_Folder"

# Path for CSV imporation into a dataframe.
c = "/Users/neo/Drive/Python/WuFlu_Dashboard/WuFlu_Sandbox/WD_Sandbox/Test_Folder/NYT_US.csv"

os.system("Rscript " + a + " " + b)
NYT_US = pd.read_csv(c)

