import os
import pandas as pd

os.getcwd()

os.chdir('/Users/neo/Drive/Python/WuFlu Dashboard/CovidDashboard')
#os.chdir('CovidDashboard')

init = pd.read_csv('us-states.csv')


#--------- Transform cumulative deaths to daily deaths
init2 = init.copy()

max_fips = max(init2['fips'])   # gets the largest fips numer in the 'fips' column

counter = 0                     # set a counter to 0

while counter < max_fips:
    counter = counter + 1
    while len(init2[init2['fips'] == counter]) == 0: # could be an if statement? if the length of the selection of the current fips number == 0:
        counter = counter + 1
    current_territory = init2.loc[init2['fips'] == counter] # might not need this one?  a second selection of the current fips' entries.
    indexes_without_first = list(range(1,len(current_territory)))      #  list from 1 to current territory's entries
    column_index = current_territory.columns.get_loc('deaths')  #  index number of 'deaths' column
    indexes_without_last = list(range(0,(len(current_territory)-1)))  # list from 0 to 1 less than last entry

    a = [x1-x2 for (x1,x2) in zip(current_territory.iloc[indexes_without_first,column_index],current_territory.iloc[indexes_without_last,column_index])]
    current_territory.iloc[indexes_without_first,column_index] = a
    dd = list(init2.index[init2['fips'] == counter])
    ee = init2.columns.get_loc('deaths')
    while list(current_territory['deaths']) != list(init2.iloc[dd,ee]):
        init2.iloc[dd,ee] = current_territory['deaths']


#--------- Transform cumulative cases to daily cases
init3=init2.copy()

max_fips=max(init3['fips'])

counter=0

while counter<max_fips:
    counter=counter+1
    while len(init2[init2['fips']==counter])==0:
        counter=counter+1
    current_territory=init2.loc[init2['fips']==counter]
    indexes_without_first=list(range(1,len(current_territory)))
    column_index=current_territory.columns.get_loc('cases')
    indexes_without_last=list(range(0,(len(current_territory)-1)))
    a=[x1-x2 for (x1,x2) in zip(current_territory.iloc[indexes_without_first,column_index],current_territory.iloc[indexes_without_last,column_index])]
    current_territory.iloc[indexes_without_first,column_index]=a
    dd=list(init2.index[init2['fips']==counter])
    ee=init2.columns.get_loc('cases')
    while list(current_territory['cases'])!= list(init2.iloc[dd,ee]):
        init2.iloc[dd,ee]=current_territory['cases']
  
#init3[init3['fips']==33]


#--- Check for illogical data points; aka negative daily case number
init3[init3['cases']<0]

init3[init3['deaths']<0]


