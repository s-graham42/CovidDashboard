setwd('C:/Users/toast/Documents/CodingDojo/python_stack/CovidDashboard/covid_project/media/current_api_data')

#--- Import US data from the NYT github repository into an R object
init1=read.csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv')

#--- Create copy of imported US data.
init2=init1


#--- Calculate daily deaths and cases from cumulative data
# and create new column with those calculations.

init2$daily_deaths=c(init2$deaths[1],
                    init2$deaths[2:nrow(init2)]-
                      init2$deaths[1:(nrow(init2)-1)]
                    )

init2$daily_cases=c(init2$cases[1],
                    init2$cases[2:nrow(init2)]-
                      init2$cases[1:(nrow(init2)-1)]
)


#--- Specify names of original deaths and cases columns as
# cumulative.
colnames(init2)[colnames(init2)=="deaths"]="cumu_deaths"
colnames(init2)[colnames(init2)=="cases"]="cumu_cases"


#--- Write new dataframe as a CSV.
write.csv(init2,file='NYT_US.csv',row.names = FALSE)