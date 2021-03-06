# Running CovidDashboard

## Suggested steps to run this project:    

**1) Install Python 3.6 or later (current 3.8.5)**  

**2) Create a virtual environment:**  
It is suggested to always work on this django project with a virtual environment active.  This makes sure that dependencies are common for all contibutors.
- Create a directory near your django projects.
  - Make sure this directory is *not* within the git repository of the project - you don't want to push your environment to github.
- In your new *environments* directory run the following:

-  **Mac/Linux:**  
```
>python3 -m venv covidDashboard
```  
- **Windows:**    
```
>python -m venv covidDashboard
```


**3) Activate Virtual Environment:**
You must activate your virtual environment whenever you plan to work on the project so that only the dependencies that are needed for the project are active.
- Still in your *environments* directory run the following:
- **Mac/Linux:**  
```
>source covidDashboard/bin/activate
```
- **Windows (command prompt):**  
```
>call covidDashboard\Scripts\activate
```       
- **Windows (git bash):**  
```
>source covidDashboard/Scripts/activate
```  
-  **Windows (Powershell with PoshGit):**  
```
>covidDashboard\Scripts\activate.ps1
```  

you should now have an indicator on your command line that shows the name of your environment:
```
(covidDashboard) C:\Users\me\Documents\djangoProjects\CovidDashboard>
```  


**4) Install Django 2.2 and Pandas:**
With our virtual envoronment active, we can load packages associated with the project.  For no particular reason other than it's what I was used to, covidProject uses django version 2.2.
- **(covidDashboard) Windows/Mac:**  
```
>pip install Django==2.2
```
- (installs packages: sqlparse, pytz, django)  
```
>pip install pandas
```    
- (installs packages: six, python-dateutil, numpy, pandas)
<br/>

-  You can check to see that your dependencies are correct:  
```
>pip list

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
```

<br/>

**5) Navigate to where you want the project folder to go.**

**6) Clone the Git Repo**   
```
>git clone https://github.com/s-graham42/CovidDashboard.git
```

**7) cd into the covid_project folder.**  
(You know you are in the right place if it's the directory with manage.py in it)

**8)  Migrate the database models.**  
```
>python manage.py makemigrations
```

- (if you don't see a bunch of things being prepared, try adding the name of the app ('dashboard') at the end of the command):
    - (```>python manage.py makemigrations dashboard```)  
- if you see a bunch of models prepared, next step is to migrate:
```
>python manage.py migrate
```  

**9) Run the server:**  
```
>python manage.py runserver
```

**9) ctrl + click the local host url to open the project in your browser.**  
- **In terminal should be:**  
```
Starting development server at http://127.0.0.1:8000/
```

**10) To edit code or add files to the repo, _please make a branch_:**
-  It is suggested that you name the branch you will be making pull requests from your name, so we know where it came from.
-  To create and move to a branch in one command:
```
>git checkout -b myname
```
-  To create the branch but not move there:
```
>git branch myName
```
**11)  Workflow:**
When working on the project, the suggested git workflow is as follows:  
At the beginning if the day:
 - Change to main branch
 ```
 [myName]>git checkout main
 ```
 - pull the current main branch from github to get the current state.
 ```
 [main]>git pull origin main
 ```
 - Change back to your branch
 ```
 [main]>git checkout myName
 ```
 - Merge the newly updated main branch into your branch.
 ```
 [myName]>git merge main
 ```
 - When you've committed your changes and want to make a pull request, be sure to push to _your branch_.
 ```
 [myName]>git push origin myName
 ```

