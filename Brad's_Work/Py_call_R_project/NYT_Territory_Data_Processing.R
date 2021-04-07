#--- Set working directory for this script from command line
# trailing argument.

a = commandArgs(trailingOnly = T)

setwd(a)


#--- Import States data from the NYT github repository into an R object
stage1=read.csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv')


#--- Create copy of imported data to be worked upon.
stage2=stage1

#--- Create new column to receive new calculations.
stage2$`daily_deaths`=1

#--- Alter death column from cumulative to daily

# Set upper bound for sifting counter which will be used
#  to serially target each territory in dataset by it's FIPS.
pp=max(stage2$fips)

# Create empty sifting counter.
xx=0

# Sift through each territory and alter it's cumulative death count 
#  to reflect daily death count instead.
while(xx<pp){
  xx=xx+1
  # check that a given territory has at least one data point and
  #  if not, check the next one.
  while(nrow(stage2[stage2$fips==xx,])==0){
    xx=xx+1
  }
  # create transitory data frame, which exists only in this loop,
  # consisting only of data relevant to the territory with the current FIPS.
  yy=data.frame(stage2[stage2$fips==xx,])
  # Alter currently relevant territory's cumulative death count to
  # a daily death count.
  yy$daily_deaths[2:nrow(yy)]=
    yy$deaths[2:nrow(yy)]-
    yy$deaths[1:(nrow(yy)-1)]
  # Replace the cumulative death count, of the currently relevant 
  # territory, in the global environment to reflect the daily 
  # death count in the loop environment.
  stage2[stage2$fips==xx,]=yy
}


#--- Copy working dataframe for futher alteration.
stage3=stage2

#--- Create new column to receive new calculations.
stage3$`daily_cases`=1

#--- Transform cases column from cumulative to daily.

# Set upper bound for sifting counter which will be used
#  to serially target each territory in dataset by it's FIPS.
pp=max(stage3$fips)

# Create empty sifting counter.
xx=0

# Sift through each territory and alter it's cumulative case count 
#  to reflect daily case count instead.
while(xx<pp){
  xx=xx+1
  # check that a given territory has at least one data point and
  #  if not, check the next fips ID.
  while(nrow(stage3[stage3$fips==xx,])==0){
    xx=xx+1
  }
  # create transitory data frame, which exists only in this loop,
  # consisting only of data relevant to the territory with the current FIPS.
  yy=data.frame(stage3[stage3$fips==xx,])
  # Alter currently relevant territory's cumulative death count to
  # a daily death count.
  yy$cases[2:nrow(yy)]=
    yy$cases[2:nrow(yy)]-
    yy$cases[1:(nrow(yy)-1)]
  # Replace the cumulative death count, of the currently relevant 
  # territory, in the global environment to reflect the daily 
  # death count in the loop environment.
  stage3[stage3$fips==xx,]=yy
}


#--- Add moving death averages in new columns.
stage4=stage3

stage4$`3_Day_MA_Ddeaths`=1
stage4$`7_Day_MA_Ddeaths`=1
stage4$`30_Day_MA_Ddeaths`=1


pp=max(stage4$fips)

# Create empty sifting counter.
xx=0

# Sift through each territory, calculate various MA and add results
# to a new column that is appropriately labeled.
while(xx<pp){
  xx=xx+1
  # check that a given territory has at least one data point and
  #  if not, check the next fips ID.
  while(nrow(stage4[stage4$fips==xx,])==0){
    xx=xx+1
  }
  # create transitory data frame, which exists only in this loop,
  # consisting only of data relevant to the territory with the current FIPS.
  yy=data.frame(stage4[stage4$fips==xx,],check.names = F)
  
  # Three day
  a=integer()
  b=0
  
  while (b <= (nrow(yy)-3)) {
    b=b+1
    a[length(a)+1]=round(mean(yy$daily_deaths[b:(b+2)]))
  }
  
  yy$`3_Day_MA_Ddeaths`=c(rep.int(0,2),a)
  
  # Seven day
  a=integer()
  b=0
  
  while (b <= (nrow(yy)-7)) {
    b=b+1
    a[length(a)+1]=round(mean(yy$daily_deaths[b:(b+6)]))
  }
  
  yy$`7_Day_MA_Ddeaths`=c(rep.int(0,6),a)
  
  #30 day
  a=integer()
  b=0
  
  while (b <= (nrow(yy)-30)) {
    b=b+1
    a[length(a)+1]=round(mean(yy$daily_deaths[b:(b+29)]))
  }
  
  yy$`30_Day_MA_Ddeaths`=c(rep.int(0,29),a)
  # Replace the cumulative death count, of the currently relevant 
  # territory, in the global environment to reflect the daily 
  # death count in the loop environment.
  stage4[stage4$fips==xx,]=yy
}


#--- Add moving case averages in new columns.
stage5=stage4

stage5$`3_Day_MA_Dcases`=1
stage5$`7_Day_MA_Dcases`=1
stage5$`30_Day_MA_Dcases`=1


pp=max(stage5$fips)

# Create empty sifting counter.
xx=0

# Sift through each territory, calculate various MA and add results
# to a new column that is appropriately labeled.
while(xx<pp){
  xx=xx+1
  # check that a given territory has at least one data point and
  #  if not, check the next fips ID.
  while(nrow(stage5[stage5$fips==xx,])==0){
    xx=xx+1
  }
  # create transitory data frame, which exists only in this loop,
  # consisting only of data relevant to the territory with the current FIPS.
  yy=data.frame(stage5[stage5$fips==xx,],check.names = F)
  
  # Three day
  a=integer()
  b=0
  
  while (b <= (nrow(yy)-3)) {
    b=b+1
    a[length(a)+1]=round(mean(yy$daily_cases[b:(b+2)]))
  }
  
  yy$`3_Day_MA_Dcases`=c(rep.int(0,2),a)
  
  # Seven day
  a=integer()
  b=0
  
  while (b <= (nrow(yy)-7)) {
    b=b+1
    a[length(a)+1]=round(mean(yy$daily_cases[b:(b+6)]))
  }
  
  yy$`7_Day_MA_Dcases`=c(rep.int(0,6),a)
  
  #30 day
  a=integer()
  b=0
  
  while (b <= (nrow(yy)-30)) {
    b=b+1
    a[length(a)+1]=round(mean(yy$daily_cases[b:(b+29)]))
  }
  
  yy$`30_Day_MA_Dcases`=c(rep.int(0,29),a)
  # Replace the cumulative death count, of the currently relevant 
  # territory, in the global environment to reflect the daily 
  # death count in the loop environment.
  stage5[stage5$fips==xx,]=yy
}

#--- Relable original columns to reflect their cumulative nature.
colnames(stage5)[colnames(stage5)=="deaths"]="cumu_deaths"
colnames(stage5)[colnames(stage5)=="cases"]="cumu_cases"

#--- Generate a CSV file of the working dataframe.
write.csv(stage5,file='NYT_States.csv',row.names = FALSE)
