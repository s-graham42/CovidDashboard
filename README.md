# CovidDashboard
A Dashboard to upload and visualize covid-19 data.

Suggested steps to run this project:

1) Install Python 3.6 or later (current 3.8.5)

2) create a virtual environment:  
- **Mac/Linux:**  
```python3 -m venv covidDashboard```  
- **Windows:**    
```python -m venv covidDashboard```


3) Activate Virtual Environment:
- **Mac/Linux:**  
```source covidDashboard/bin/activate```
- **Windows (command prompt):**  
```call covidDashboard\Scripts\activate```       
- **Windows (git bash):**  
```source covidDashboard/Scripts/activate```           
**Windows (Powershell with PoshGit):**  
```covidDashboard\Scripts\activate.ps1```  

4) Install Django 2.2:
- **(covidDashboard) Windows/Mac:**  
```pip install Django==2.2``` 

5) Navigate to where you want the project folder to go.

6) Clone the Git Repo:  
```git clone https://github.com/s-graham42/CovidDashboard.git```

7) cd into the covid_project folder.  (Should be in the directory with manage.py)

8) run the server:  
```python manage.py runserver```

9) ctrl + click the local host url to open the project in your browser.  
- **In terminal should be:**  
```Starting development server at http://127.0.0.1:8000/```

10) To edit code or add files to the repo, please make a branch _I'll put instructions here in a bit_




Data used: https://github.com/nytimes/covid-19-data/blob/master/us-states.csv