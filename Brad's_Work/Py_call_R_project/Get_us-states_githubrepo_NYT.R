#--- Set working directory to a directory mutually understood with Python script
# setwd('C:/Users/toast/Documents/CodingDojo/python_stack/CovidDashboard/covid_project/media/current_api_data')

#--- Import States data from the NYT github repository into an R object
init=read.csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv')

#--- Export that R object as a CSV file
write.csv(init,file="C:/Users/toast/Documents/CodingDojo/python_stack/CovidDashboard/covid_project/media/current_api_data/us-states_githubrepo_NYT_1.csv",row.names = FALSE)
