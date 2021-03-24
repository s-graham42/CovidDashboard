#--------- Transform cumulative deaths to daily deaths.


#--- Set working directory to a directory mutually understood with Python script.
setwd('C:\Users\toast\Documents\CodingDojo\python_stack\CovidDashboard\covid_project\csv_files')


#--- Import current working NYT states csv file.
init=read.csv('us-states_githubrepo_NYT_2.csv')

#--- Transform cases column from cumulative to daily.

# Set upper bound for sifting counter which will be used
#  to serially target each territory in dataset by it's FIPS.
pp=max(init$fips)

# Create empty sifting counter.
xx=0

# Sift through each territory and alter it's cumulative case count 
#  to reflect daily case count instead.
while(xx<pp){
  xx=xx+1
  # check that a given territory has at least one data point and
  #  if not, check the next fips ID.
  while(nrow(init[init$fips==xx,])==0){
    xx=xx+1
  }
  # create transitory data frame, which exists only in this loop,
  # consisting only of data relevant to the territory with the current FIPS.
  yy=data.frame(init[init$fips==xx,])
  # Alter currently relevant territory's cumulative death count to
  # a daily death count.
  yy$cases[2:nrow(yy)]=
    yy$cases[2:nrow(yy)]-
    yy$cases[1:(nrow(yy)-1)]
  # Replace the cumulative death count, of the currently relevant 
  # territory, in the global environment to reflect the daily 
  # death count in the loop environment.
  init[init$fips==xx,]=yy
}



write.csv(init,file='us-states_githubrepo_NYT_3.csv',row.names = FALSE)

init2=init[,colnames(init)=="date" |
             colnames(init)=="state"|
             colnames(init)=="fips"|
             colnames(init)=="cases"]
write.csv(init2,file='NYT_dly_case.csv',row.names = FALSE)
