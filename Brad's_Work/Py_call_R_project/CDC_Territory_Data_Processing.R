#--- Set working directory for this script from command line
# trailing argument.

directory = commandArgs(trailingOnly = T)

deposit_directory = directory[1]

working_directory = directory[2]

setwd(working_directory)


#--- Set required libraries
library('dplyr')


#--- Import a FIPS list to be correlated with incomming data.  This
# will facilitate data processing.
FIPS=read.csv('States_Abb_FIPS.csv')


#--- Import territory data from the CDC github repository into an R object
stage1=read.csv('https://data.cdc.gov/api/views/9mfq-cb36/rows.csv?accessType=DOWNLOAD')


#--- Pair down CDC data to contain only vectors which correspond
# with NYT data.
stage2=data.frame(date=stage1$submission_date,
                  state=stage1$state,
                  cases=stage1$tot_cases,
                  deaths=stage1$tot_death)


#--- Eliminate municipalities from dataset.
a=1

stage3=stage2[stage2$state==FIPS$Abbreviation[a],]

while (a < nrow(FIPS)){
                            a=a+1
                            stage3[(nrow(stage3)+1):
                                       (nrow(stage3)+
                                          nrow(stage2[stage2[,'state']==
                                            FIPS$Abbreviation[a],])),]=
                                              stage2[stage2[,'state']==FIPS$Abbreviation[a],]
                            }


#--- Reformat dates to be understandable by dplyer arrange function.

stage3$date=as.Date(stage3$date,format='%m/%d/%Y')


#--- Adding FIPS to facilitate data processing.
stage4=stage3

# Prepare column to receive FIPS.
stage4$`fips`=1

a=0

while (a < nrow(FIPS)){
                            a=a+1
                            stage4[stage4['state']==FIPS$Abbreviation[a],'fips']=
                              FIPS$FIPS[a]
                            }


#--- Alter death column from cumulative to daily

# Create copy of previous stage to be worked upon.
stage5=stage4

#--- Create new column to receive new calculations.
stage5$`daily_deaths`=1

# Set upper bound for sifting counter which will be used
#  to serially target each territory in dataset by it's FIPS.
pp=max(stage5$fips)

# Create empty sifting counter.
xx=0

# Sift through each territory and alter it's cumulative death count 
#  to reflect daily death count instead.
while(xx<pp){
  xx=xx+1
  # Check that a given territory has at least one data point and
  #  if not, check the next one.
  while(nrow(stage5[stage5$fips==xx,])==0){
    xx=xx+1
  }
  # Create transitory data frame, which exists only in this loop,
  # consisting only of data relevant to the territory with the current FIPS.
  yy=data.frame(stage5[stage5$fips==xx,])
  
  # Arrange temporary dataframe by date to facilitate calculation.
  yy=arrange(yy,date)
  
  # Alter currently relevant territory's cumulative death count to
  # a daily death count.
  yy$daily_deaths[2:nrow(yy)]=
    yy$deaths[2:nrow(yy)]-
    yy$deaths[1:(nrow(yy)-1)]
  
  # Replace the cumulative death count, of the currently relevant 
  # territory, in the global environment to reflect the daily 
  # death count in the loop environment.
  stage5[stage5$fips==xx,]=yy
}


#--- Transform cases column from cumulative to daily.

# Create copy of previous stage to be worked upon.
stage6=stage5

# Create new column to receive new calculations.
stage6$`daily_cases`=1

# Set upper bound for sifting counter which will be used
#  to serially target each territory in dataset by it's FIPS.
pp=max(stage6$fips)

# Create empty sifting counter.
xx=0

# Sift through each territory and alter it's cumulative case count 
#  to reflect daily case count instead.
while(xx<pp){
  xx=xx+1
  
  # check that a given territory has at least one data point and
  #  if not, check the next fips ID.
  while(nrow(stage6[stage6$fips==xx,])==0){
    xx=xx+1
  }
  
  # create transitory data frame, which exists only in this loop,
  # consisting only of data relevant to the territory with the current FIPS.
  yy=data.frame(stage6[stage6$fips==xx,])
  
  # Arrange temporary dataframe by date to facilitate calculation.
  yy=arrange(yy,date)
  
  # Alter currently relevant territory's cumulative death count to
  # a daily death count.
  yy$daily_cases[2:nrow(yy)]=
    yy$cases[2:nrow(yy)]-
    yy$cases[1:(nrow(yy)-1)]
  
  # Replace the cumulative death count, of the currently relevant 
  # territory, in the global environment to reflect the daily 
  # death count in the loop environment.
  stage6[stage6$fips==xx,]=yy
}


#--- Add moving death averages in new columns.
stage7=stage6

stage7$`3_Day_MA_Ddeaths`=1
stage7$`7_Day_MA_Ddeaths`=1
stage7$`30_Day_MA_Ddeaths`=1


pp=max(stage7$fips)

# Create empty sifting counter.
xx=0

# Sift through each territory, calculate various MA and add results
# to a new column that is appropriately labeled.
while(xx<pp){
  xx=xx+1
  # check that a given territory has at least one data point and
  #  if not, check the next fips ID.
  while(nrow(stage7[stage7$fips==xx,])==0){
    xx=xx+1
  }
  # create transitory data frame, which exists only in this loop,
  # consisting only of data relevant to the territory with the current FIPS.
  yy=data.frame(stage7[stage7$fips==xx,],check.names = F)
  
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
  stage7[stage7$fips==xx,]=yy
}


#--- Add moving case averages in new columns.
stage8=stage7

stage8$`3_Day_MA_Dcases`=1
stage8$`7_Day_MA_Dcases`=1
stage8$`30_Day_MA_Dcases`=1


pp=max(stage8$fips)

# Create empty sifting counter.
xx=0

# Sift through each territory, calculate various MA and add results
# to a new column that is appropriately labeled.
while(xx<pp){
  xx=xx+1
  # check that a given territory has at least one data point and
  #  if not, check the next fips ID.
  while(nrow(stage8[stage8$fips==xx,])==0){
    xx=xx+1
  }
  # create transitory data frame, which exists only in this loop,
  # consisting only of data relevant to the territory with the current FIPS.
  yy=data.frame(stage8[stage8$fips==xx,],check.names = F)
  
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
  stage8[stage8$fips==xx,]=yy
}

#--- Relable original columns to reflect their cumulative nature.
colnames(stage8)[colnames(stage8)=="deaths"]="cumu_deaths"
colnames(stage8)[colnames(stage8)=="cases"]="cumu_cases"

#--- Generate a CSV file of the working dataframe.

write.csv(stage8,file=deposit_directory,row.names = FALSE)
