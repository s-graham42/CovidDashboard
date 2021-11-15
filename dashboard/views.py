from django.shortcuts import render, HttpResponse, redirect
from .forms import CsvFileForm
from .models import CsvFile, State
from django.http import JsonResponse
import csv
import json
import datetime
from covid_project.settings import BASE_DIR
from .db_processing import *
from .datasources import *

# """
 
#  88 88b 88 88 888888     8888b.     db    888888    db    .dP"Y8  dP"Yb  88   88 88""Yb  dP""b8 888888 .dP"Y8 
#  88 88Yb88 88   88        8I  Yb   dPYb     88     dPYb   `Ybo." dP   Yb 88   88 88__dP dP   `" 88__   `Ybo." 
#  88 88 Y88 88   88        8I  dY  dP__Yb    88    dP__Yb  o.`Y8b Yb   dP Y8   8P 88"Yb  Yb      88""   o.`Y8b 
#  88 88  Y8 88   88       8888Y"  dP""""Yb   88   dP""""Yb 8bodP'  YbodP  `YbodP' 88  Yb  YboodP 888888 8bodP' 
 
# """
# TODO: [CD-31] comment out the datasource initialization during migrations
nyt_us_data = NewYorkTimesUSData()
print(nyt_us_data, "initialized.")
nyt_state_data = NewYorkTimesStateData()
print(nyt_state_data, "initialized.")
cdc_state_data = CDCStateData()
print(cdc_state_data, "initialized.")

def get_datasource(name):
    if name == "NewYorkTimes":
        return nyt_state_data
    elif name == "CDC":
        return cdc_state_data
    else:
        return ValueError("Invalid Name.")

# """
 
#  8b    d8    db    88 88b 88     88b 88    db    Yb    dP 88  dP""b8    db    888888 88  dP"Yb  88b 88 
#  88b  d88   dPYb   88 88Yb88     88Yb88   dPYb    Yb  dP  88 dP   `"   dPYb     88   88 dP   Yb 88Yb88 
#  88YbdP88  dP__Yb  88 88 Y88     88 Y88  dP__Yb    YbdP   88 Yb  "88  dP__Yb    88   88 Yb   dP 88 Y88 
#  88 YY 88 dP""""Yb 88 88  Y8     88  Y8 dP""""Yb    YP    88  YboodP dP""""Yb   88   88  YbodP  88  Y8 
 
# """

def index(request):
    return render(request, "index.html")

def covid_info(request):
    current_cases = nyt_us_data.get_current_cases()
    current_deaths = nyt_us_data.get_current_deaths()
    current_date = nyt_us_data.get_date().strftime('%Y-%m-%d')
    context = {
        'current_cases': f"{current_cases:,}",
        'current_deaths': f"{current_deaths:,}",
        'current_date': current_date,
    }
    return render(request, "covid_info.html", context)

def vaccines_main(request):
    return render(request, "vaccines/vaccines_main.html")

def dashboard_admin(request):
    return render(request, "admin/dashboard_admin.html")

# """
 
#     db    88""Yb 88     88b 88    db    Yb    dP 88  dP""b8    db    888888 88  dP"Yb  88b 88 
#    dPYb   88__dP 88     88Yb88   dPYb    Yb  dP  88 dP   `"   dPYb     88   88 dP   Yb 88Yb88 
#   dP__Yb  88"""  88     88 Y88  dP__Yb    YbdP   88 Yb  "88  dP__Yb    88   88 Yb   dP 88 Y88 
#  dP""""Yb 88     88     88  Y8 dP""""Yb    YP    88  YboodP dP""""Yb   88   88  YbodP  88  Y8 
 
# """

def singleVariable(request, source):
    data_source = get_datasource(source)
    current_date = data_source.get_date().strftime('%Y-%m-%d')
    context = {
        "data_source": data_source.get_source(),
        "all_states" : State.objects.all().order_by("fips"),
        "current_date": current_date,
    }
    return render(request, "single_variable_over_time.html", context)

# """
 
#     db    8888b.  8b    d8 88 88b 88 
#    dPYb    8I  Yb 88b  d88 88 88Yb88 
#   dP__Yb   8I  dY 88YbdP88 88 88 Y88 
#  dP""""Yb 8888Y"  88 YY 88 88 88  Y8 
 
# """

def db_load_states(request):
    if request.method == "POST":
        load_states_only()

    return redirect("/dashboard_admin/view_states")

def view_states(request):
    context = {
        "all_states": State.objects.all().order_by("fips")
    }
    return render(request, "admin/view_states.html", context)

def demo_charts(request):
    return render(request, "admin/demo_charts.html")

def upload_csv(request):
    if request.method == "POST":
        form = CsvFileForm(request.POST, request.FILES)
        if form.is_valid():
            new_name = form.cleaned_data['name']
            new_desc = form.cleaned_data['description']
            new_file = form.cleaned_data['file']
            CsvFile.objects.create(name=new_name, description=new_desc, file=new_file)
            return redirect("dashboard_admin/upload_success")
    else:
        form = CsvFileForm()
    return render(request, "admin/upload_csv.html", {'form' : form})

def upload_success(request):
    context = {
        'all_files' : CsvFile.objects.all(),
    }
    return render(request, "admin/upload_success.html", context)

# """
 
#   dP""b8 88  88    db    88""Yb 888888     Yb    dP 88 888888 Yb        dP .dP"Y8 
#  dP   `" 88  88   dPYb   88__dP   88        Yb  dP  88 88__    Yb  db  dP  `Ybo." 
#  Yb      888888  dP__Yb  88"Yb    88         YbdP   88 88""     YbdPYbdP   o.`Y8b 
#   YboodP 88  88 dP""""Yb 88  Yb   88          YP    88 888888    YP  YP    8bodP' 
 
# """

def usTotalsChart(request):
    if request.method == "POST":
        start = request.POST['start_date']
        end = request.POST['end_date']
        column = nyt_us_data.get_column(request.POST['cumulative_daily'], request.POST['cases_deaths'], request.POST['moving_average'])

        title = (f"U.S. {request.POST['cumulative_daily'].capitalize()} Covid-19 {request.POST['cases_deaths'].capitalize()} from {start} to {end}.")
        this_data_name = (f"U.S. {request.POST['cumulative_daily'].capitalize()} {request.POST['cases_deaths'].capitalize()}")
        this_dataset = nyt_us_data.get_by_date_range(start, end, column)
        # returns list of tuples [(date, datapoint), (...] }
        
        return JsonResponse(data={
            'title': title,
            'data_name': this_data_name,
            'dataset': this_dataset})


def singleVariableOverTime(request, source):
    if request.method == "POST":
        data_source = get_datasource(source)
        column = data_source.get_column(request.POST['cumulative_daily'], request.POST['cases_deaths'], request.POST['moving_average'])
        start = request.POST['start_date']
        end = request.POST['end_date']
        title = (f"{request.POST['cumulative_daily'].capitalize()} Covid-19 {request.POST['cases_deaths'].capitalize()} from {start} to {end}.")

        state_1 = data_source.get_state_by_date_range(int(request.POST['state_1']), start, end, column)
        state_2 = data_source.get_state_by_date_range(int(request.POST['state_2']), start, end, column)
        state_3 = data_source.get_state_by_date_range(int(request.POST['state_3']), start, end, column)
        state_4 = data_source.get_state_by_date_range(int(request.POST['state_4']), start, end, column)
        # returns dictionary {'state': state name, 'data': list of tuples [(date, datapoint), (...] }
        
        return JsonResponse(data={
            'title': title,
            'state_1_name': state_1['state'],
            'state_1_data': state_1['data'],
            'state_2_name': state_2['state'],
            'state_2_data': state_2['data'],
            'state_3_name': state_3['state'],
            'state_3_data': state_3['data'],
            'state_4_name': state_4['state'],
            'state_4_data': state_4['data']})


