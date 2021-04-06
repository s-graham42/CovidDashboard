# CovidDashboard
A Web App Dashboard for visualizing covid-19 data.

![April_2021_dashboard](https://user-images.githubusercontent.com/68925652/113661850-bce13c00-965b-11eb-97a1-7cef2bc99955.gif)

This project was born out of a desire to be able to visualize and explore the data surounding the covid-19 pandemic.  We would build a sandbox where covid-19 data could be selected, compared and manipulated in order to gain new insights and better understanding of the impact of this deadly time.
<hr><br>

# Watch a Demo Video:

[![Demo Video](http://img.youtube.com/vi/z-TTvH_B9Vw/0.jpg)](http://www.youtube.com/watch?v=z-TTvH_B9Vw "CovidDashboard Demo Video")

## Datasets
Admins of the app can upload csv files to load information into the onboard SQLite Database.  To begin with, we used the [.csv file on the NY Times github](https://github.com/nytimes/covid-19-data/blob/master/us-states.csv)

You can also view and manipulate live API datasets from the following sources:
- CDC
- The New York Times
- Johns Hopkins University
<hr><br>

## Tech Stack:
- The app is built in **Python** 3.8 using **Django 2.2**
- The Database used (when used) is the Django-provided **SQLite** Database 
- Charts are displayed using **Charts.js**
- Data cleaning and processing is done in **R**
- .csv file processing is done using the **Pandas** library
- Page Styling uses the **Bootstrap** CSS framework.
<hr><br>

If you would like to fork and run this project, we've provided some [step-by-step instructions to get you going in covid_project\ToRunThisProject.md](ToRunThisProject.md)

A list of necessary packages to install with some instructions is in [covid_project\dependencies.md](dependencies.md)
