#--- Set working directory to a directory mutually understood with Python script
setwd('C:\Users\toast\Documents\CodingDojo\python_stack\CovidDashboard\covid_project\csv_files')

#--- Import States data from the NYT github repository into an R object
init1=read.csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv')


#--- Create copy of imported data to be worked upon.
init2=init1


#--- Alter death column from cumulative to daily

# Set upper bound for sifting counter which will be used
#  to serially target each territory in dataset by it's FIPS.
pp=max(init2$fips)

# Create empty sifting counter.
xx=0

# Sift through each territory and alter it's cumulative death count 
#  to reflect daily death count instead.
while(xx<pp){
  xx=xx+1
  # check that a given territory has at least one data point and
  #  if not, check the next one.
  while(nrow(init2[init2$fips==xx,])==0){
    xx=xx+1
  }
  # create transitory data frame, which exists only in this loop,
  # consisting only of data relevant to the territory with the current FIPS.
  yy=data.frame(init2[init2$fips==xx,])
  # Alter currently relevant territory's cumulative death count to
  # a daily death count.
  yy$deaths[2:nrow(yy)]=
    yy$deaths[2:nrow(yy)]-
    yy$deaths[1:(nrow(yy)-1)]
  # Replace the cumulative death count, of the currently relevant 
  # territory, in the global environment to reflect the daily 
  # death count in the loop environment.
  init2[init2$fips==xx,]=yy
}


#--- Copy working dataframe for futher alteration.
init3=init2

#--- Transform cases column from cumulative to daily.

# Set upper bound for sifting counter which will be used
#  to serially target each territory in dataset by it's FIPS.
pp=max(init3$fips)

# Create empty sifting counter.
xx=0

# Sift through each territory and alter it's cumulative case count 
#  to reflect daily case count instead.
while(xx<pp){
  xx=xx+1
  # check that a given territory has at least one data point and
  #  if not, check the next fips ID.
  while(nrow(init3[init3$fips==xx,])==0){
    xx=xx+1
  }
  # create transitory data frame, which exists only in this loop,
  # consisting only of data relevant to the territory with the current FIPS.
  yy=data.frame(init3[init3$fips==xx,])
  # Alter currently relevant territory's cumulative death count to
  # a daily death count.
  yy$cases[2:nrow(yy)]=
    yy$cases[2:nrow(yy)]-
    yy$cases[1:(nrow(yy)-1)]
  # Replace the cumulative death count, of the currently relevant 
  # territory, in the global environment to reflect the daily 
  # death count in the loop environment.
  init3[init3$fips==xx,]=yy
}

init1$daily_deaths=init3$deaths
init1$daily_cases=init3$cases

colnames(init1)[colnames(init1)=="deaths"]="cumu_deaths"
colnames(init1)[colnames(init1)=="cases"]="cumu_cases"

write.csv(init1,file='NYT.csv',row.names = FALSE)