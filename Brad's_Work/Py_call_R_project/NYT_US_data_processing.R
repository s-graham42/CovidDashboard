#--- Set working directory for this script from command line
# trailing argument.

a = commandArgs(trailingOnly = T)

setwd(a)


#--- Import US data from the NYT github repository into an R object
stage1=read.csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv')

#--- Create copy of imported US data.
stage2=stage1


#--- Calculate daily deaths and cases from cumulative data
# and create new column with those calculations.

stage2$daily_deaths=c(stage2$deaths[1],
                    stage2$deaths[2:nrow(stage2)]-
                      stage2$deaths[1:(nrow(stage2)-1)]
                    )

stage2$daily_cases=c(stage2$cases[1],
                    stage2$cases[2:nrow(stage2)]-
                      stage2$cases[1:(nrow(stage2)-1)]
)


#--- Add moving death averages in new columns.
stage3=stage2

#--- Create new column to receive new calculations.
stage3$`3_Day_MA_Ddeaths`=1
stage3$`7_Day_MA_Ddeaths`=1
stage3$`30_Day_MA_Ddeaths`=1

# Three day
a=integer()
b=0

while (b <= (nrow(stage3)-3)) {
  b=b+1
  a[length(a)+1]=round(mean(stage3$daily_deaths[b:(b+2)]))
                                }

stage3$`3_Day_MA_Ddeaths`=c(rep.int(0,2),a)

# Seven day
a=integer()
b=0

while (b <= (nrow(stage3)-7)) {
  b=b+1
  a[length(a)+1]=round(mean(stage3$daily_deaths[b:(b+6)]))
}

stage3$`7_Day_MA_Ddeaths`=c(rep.int(0,6),a)

#30 day
a=integer()
b=0

while (b <= (nrow(stage3)-30)) {
  b=b+1
  a[length(a)+1]=round(mean(stage3$daily_deaths[b:(b+29)]))
}

stage3$`30_Day_MA_Ddeaths`=c(rep.int(0,29),a)


#--- Add moving case averages in new columns.
stage4=stage3

#--- Create new column to receive new calculations.
stage4$`3_Day_MA_Dcases`=1
stage4$`7_Day_MA_Dcases`=1
stage4$`30_Day_MA_Dcases`=1

# Three day
a=integer()
b=0

while (b <= (nrow(stage4)-3)) {
  b=b+1
  a[length(a)+1]=round(mean(stage4$daily_cases[b:(b+2)]))
}

stage4$`3_Day_MA_Dcases`=c(rep.int(0,2),a)

# Seven day
a=integer()
b=0

while (b <= (nrow(stage4)-7)) {
  b=b+1
  a[length(a)+1]=round(mean(stage4$daily_cases[b:(b+6)]))
}

stage4$`7_Day_MA_Dcases`=c(rep.int(0,6),a)

#30 day
a=integer()
b=0

while (b <= (nrow(stage4)-30)) {
  b=b+1
  a[length(a)+1]=round(mean(stage4$daily_cases[b:(b+29)]))
}

stage4$`30_Day_MA_Dcases`=c(rep.int(0,29),a)


#--- Specify names of original deaths and cases columns as
# cumulative.
colnames(stage4)[colnames(stage4)=="deaths"]="cumu_deaths"
colnames(stage4)[colnames(stage4)=="cases"]="cumu_cases"


#--- Write new dataframe as a CSV.
write.csv(stage4,file='NYT_US.csv',row.names = FALSE)

