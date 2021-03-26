from django.shortcuts import render, HttpResponse, redirect
from .forms import CsvFileForm
from .models import CsvFile, State, Entry
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

nyt_data = NewYorkTimesData()
print(nyt_data, " initailized.")

# """
 
#  8b    d8    db    88 88b 88     88b 88    db    Yb    dP 88  dP""b8    db    888888 88  dP"Yb  88b 88 
#  88b  d88   dPYb   88 88Yb88     88Yb88   dPYb    Yb  dP  88 dP   `"   dPYb     88   88 dP   Yb 88Yb88 
#  88YbdP88  dP__Yb  88 88 Y88     88 Y88  dP__Yb    YbdP   88 Yb  "88  dP__Yb    88   88 Yb   dP 88 Y88 
#  88 YY 88 dP""""Yb 88 88  Y8     88  Y8 dP""""Yb    YP    88  YboodP dP""""Yb   88   88  YbodP  88  Y8 
 
# """

def index(request):
    return render(request, "index.html")

def covid_info(request):
    return render(request, "covid_info.html")

def vaccines_main(request):
    return render(request, "vaccines/vaccines_main.html")

def dashboard_admin(request):
    return render(request, "admin/dashboard_admin.html")

def apiData(request):
    pass

# """
 
#     db    88""Yb 88     88b 88    db    Yb    dP 88  dP""b8    db    888888 88  dP"Yb  88b 88 
#    dPYb   88__dP 88     88Yb88   dPYb    Yb  dP  88 dP   `"   dPYb     88   88 dP   Yb 88Yb88 
#   dP__Yb  88"""  88     88 Y88  dP__Yb    YbdP   88 Yb  "88  dP__Yb    88   88 Yb   dP 88 Y88 
#  dP""""Yb 88     88     88  Y8 dP""""Yb    YP    88  YboodP dP""""Yb   88   88  YbodP  88  Y8 
 
# """

def nyt_svot(request):
    context = {
        "all_states" : State.objects.all().order_by("fips"),
    }
    return render(request, "NYT_single_variable_over_time.html", context)

def compare_daily_cases(request):
    caseData = []
    deathData = []
    labelData = []
    this_state = State.objects.get(fips=53)
    for item in Entry.objects.filter(state=this_state).order_by('date'):
        caseData.append(item.cases_d)
        deathData.append(item.deaths_d)
        labelData.append(str(item.date))
    context = {
        "all_states" : State.objects.all().order_by("fips"),
        "labels" : labelData,
        "caseData" : caseData,
        "deathData" : deathData,
    }
    return render(request, "compare_daily_cases.html", context)

def compare_single_variable(request):
    caseData = []
    deathData = []
    labelData = []
    this_state = State.objects.get(fips=53)
    for item in Entry.objects.filter(state=this_state).order_by('date'):
        caseData.append(item.cases_c)
        deathData.append(item.deaths_c)
        labelData.append(str(item.date))
    context = {
        "all_states" : State.objects.all().order_by("fips"),
        "labels" : labelData,
        "caseData" : caseData,
        "deathData" : deathData,
    }
    return render(request, "single_variable_over_time.html", context)

# """
 
#     db    8888b.  8b    d8 88 88b 88 
#    dPYb    8I  Yb 88b  d88 88 88Yb88 
#   dP__Yb   8I  dY 88YbdP88 88 88 Y88 
#  dP""""Yb 8888Y"  88 YY 88 88 88  Y8 
 
# """

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

def db_load_csv(request, id):
    if request.method == "POST":
        start = datetime.datetime.now()
        file_to_load = CsvFile.objects.filter(id=id)
        if len(file_to_load) > 0:
            file_to_load = file_to_load[0]
                # go through the file, check all the states and put them in the database if they are not there already.
            checked_states = check_and_create_states(file_to_load)
            print(checked_states)
                # go through the file again and create or update entries -no dailies yet
            processed_rows = replace_all_entries(file_to_load)
            print("Processed rows: ", processed_rows)
                # go through all the states and calculate daily values.
            processed_states = calculate_all_dailies()
            print("Processed States: ", processed_states)
                # print stats to terminal
            end = datetime.datetime.now()
            print("start: ", start)
            print("end: ", end)
            print("time to complete: ", (end - start))
            return redirect(f'dashboard_admin/db_load_success/{processed_rows}')
    return redirect('dashboard_admin/upload_success')

def db_load_sucess(request, row_count):
    context = {
        'row_count' : row_count,
    }
    return render(request, "admin/db_load_success.html", context)

# """
 
#   dP""b8 88  88    db    88""Yb 888888     Yb    dP 88 888888 Yb        dP .dP"Y8 
#  dP   `" 88  88   dPYb   88__dP   88        Yb  dP  88 88__    Yb  db  dP  `Ybo." 
#  Yb      888888  dP__Yb  88"Yb    88         YbdP   88 88""     YbdPYbdP   o.`Y8b 
#   YboodP 88  88 dP""""Yb 88  Yb   88          YP    88 888888    YP  YP    8bodP' 
 
# """


def oneStateDailyCases(request):
    if request.method == "POST":
        labels = []
        state_data = []
        this_state = State.objects.get(fips=request.POST['this_state'])
        
        this_state_qs = Entry.objects.filter(state=this_state).order_by('date')
        for entry in this_state_qs:
            labels.append(entry.date)
            state_data.append(entry.cases_d)
        
        return JsonResponse(data={ 'state_name': this_state.name, 'labels': labels, 'state_data': state_data })

def fourStatesDailyCases(request):
    if request.method == "POST":
        # labels = []
        state_1_data = []
        state_2_data = []
        state_3_data = []
        state_4_data = []
        state_1 = State.objects.get(fips=request.POST['state_1'])
        state_2 = State.objects.get(fips=request.POST['state_2'])
        state_3 = State.objects.get(fips=request.POST['state_3'])
        state_4 = State.objects.get(fips=request.POST['state_4'])

        state_1_qs = Entry.objects.filter(state=state_1).order_by('date')
        for entry in state_1_qs:
            s1date = datetime.datetime.strftime(entry.date, "%m/%d/%Y")
            state_1_data.append([s1date, entry.cases_d])

        state_2_qs = Entry.objects.filter(state=state_2).order_by('date')
        for entry in state_2_qs:
            s2date = datetime.datetime.strftime(entry.date, "%m/%d/%Y")
            state_2_data.append([s2date, entry.cases_d])

        state_3_qs = Entry.objects.filter(state=state_3).order_by('date')
        for entry in state_3_qs:
            s3date = datetime.datetime.strftime(entry.date, "%m/%d/%Y")
            state_3_data.append([s3date, entry.cases_d])

        state_4_qs = Entry.objects.filter(state=state_4).order_by('date')
        for entry in state_4_qs:
            s4date = datetime.datetime.strftime(entry.date, "%m/%d/%Y")
            state_4_data.append([s4date, entry.cases_d])
        
        return JsonResponse(data={  #'labels': labels,
            'state_1_name': state_1.name,
            'state_1_data': state_1_data,
            'state_2_name': state_2.name,
            'state_2_data': state_2_data,
            'state_3_name': state_3.name,
            'state_3_data': state_3_data,
            'state_4_name': state_4.name,
            'state_4_data': state_4_data})

def singleVariableOverTime(request):
    if request.method == "POST":
        # labels = []
        state_1_data = []
        state_2_data = []
        state_3_data = []
        state_4_data = []
        state_1 = State.objects.get(fips=request.POST['state_1'])
        state_2 = State.objects.get(fips=request.POST['state_2'])
        state_3 = State.objects.get(fips=request.POST['state_3'])
        state_4 = State.objects.get(fips=request.POST['state_4'])

        state_1_qs = Entry.objects.filter(state=state_1).order_by('date')
        for entry in state_1_qs:
            s1date = datetime.datetime.strftime(entry.date, "%m/%d/%Y")
            state_1_data.append([s1date, entry.cases_d])

        state_2_qs = Entry.objects.filter(state=state_2).order_by('date')
        for entry in state_2_qs:
            s2date = datetime.datetime.strftime(entry.date, "%m/%d/%Y")
            state_2_data.append([s2date, entry.cases_d])

        state_3_qs = Entry.objects.filter(state=state_3).order_by('date')
        for entry in state_3_qs:
            s3date = datetime.datetime.strftime(entry.date, "%m/%d/%Y")
            state_3_data.append([s3date, entry.cases_d])

        state_4_qs = Entry.objects.filter(state=state_4).order_by('date')
        for entry in state_4_qs:
            s4date = datetime.datetime.strftime(entry.date, "%m/%d/%Y")
            state_4_data.append([s4date, entry.cases_d])
        
        return JsonResponse(data={  #'labels': labels,
            'state_1_name': state_1.name,
            'state_1_data': state_1_data,
            'state_2_name': state_2.name,
            'state_2_data': state_2_data,
            'state_3_name': state_3.name,
            'state_3_data': state_3_data,
            'state_4_name': state_4.name,
            'state_4_data': state_4_data})

