## Installing Dependencies for covidDashboard

For this project, you just need to pip install *django* and *pandas*.
Here are my notes on the process:

current project dependencies:  
Package | Version
--------------- | -------
Django         | 2.2
numpy          | 1.19.4
pandas         | 1.1.5
pip            | 20.3.3
python-dateutil| 2.8.1
pytz           | 2020.4
setuptools     | 47.1.0
six            | 1.15.0
sqlparse       | 0.4.1

<br/>
commands to run (adjusted to be the mac commands):   

**create virtual environment:**

(I have a separate directory called myEnvironments that holds the directories for all my virtual environments.  Be in that directory.)

```>> python3 -m venv newEnvironmentName```  
(takes a moment to run.)
installs setuptools

activate virtual environment:
```>>source newEnvironmentName/bin/activate```  

```>>pip list:```  
Package         Version
--------------- -------
pip 20.1.1
setuptools 47.1.0

```>>pip install django==2.2```  
(installs packages: sqlparse, pytz, django)

```>>pip install pandas```  
(installs packages: six, python-dateutil, numpy, pandas)

```>>pip list```  
Package | Version
--------------- |-------
Django         | 2.2
numpy          | 1.20.0
pandas         | 1.2.1
pip            | 20.1.1
python-dateutil| 2.8.1
pytz           | 2021.1
setuptools     | 47.1.0
six            | 1.15.0
sqlparse       | 0.4.1

<br/>
(leave your venv active and cd to your project directory and do your thing)

**To exit the virtual environment** is just:

```>>deactivate```  


Data used for this project comes from: https://github.com/nytimes/covid-19-data/blob/master/us-states.csv