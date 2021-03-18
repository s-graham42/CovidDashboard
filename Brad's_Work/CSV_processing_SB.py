import os
import pandas as pd

os.getcwd()

os.chdir('/Users/neo/Drive/Python/WuFlu Dashboard/CovidDashboard')
#os.chdir('CovidDashboard')

init = pd.read_csv('us-states.csv')


#--------- Transform cumulative deaths to daily deaths
init2=init.copy()

pp=max(init2['fips'])

xx=0

while xx<pp:
    xx=xx+1
    while len(init2[init2['fips']==xx])==0:
        xx=xx+1
    yy=init2.loc[init2['fips']==xx]
    aa=list(range(1,len(yy)))
    bb=yy.columns.get_loc('deaths')
    cc=list(range(0,(len(yy)-1)))
    a=[x1-x2 for (x1,x2) in zip(yy.iloc[aa,bb],yy.iloc[cc,bb])]
    yy.iloc[aa,bb]=a
    dd=list(init2.index[init2['fips']==xx])
    ee=init2.columns.get_loc('deaths')
    while list(yy['deaths'])!= list(init2.iloc[dd,ee]):
        init2.iloc[dd,ee]=yy['deaths']


#--------- Transform cumulative cases to daily cases
init3=init2.copy()

pp=max(init3['fips'])

xx=0

while xx<pp:
    xx=xx+1
    while len(init2[init2['fips']==xx])==0:
        xx=xx+1
    yy=init2.loc[init2['fips']==xx]
    aa=list(range(1,len(yy)))
    bb=yy.columns.get_loc('cases')
    cc=list(range(0,(len(yy)-1)))
    a=[x1-x2 for (x1,x2) in zip(yy.iloc[aa,bb],yy.iloc[cc,bb])]
    yy.iloc[aa,bb]=a
    dd=list(init2.index[init2['fips']==xx])
    ee=init2.columns.get_loc('cases')
    while list(yy['cases'])!= list(init2.iloc[dd,ee]):
        init2.iloc[dd,ee]=yy['cases']
  
#init3[init3['fips']==33]


#--- Check for illogical data points; aka negative daily case number
init3[init3['cases']<0]

init3[init3['deaths']<0]


