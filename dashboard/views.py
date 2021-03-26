from django.shortcuts import render, HttpResponse, redirect
from .forms import CsvFileForm
from .models import CsvFile, State, Entry
from django.http import JsonResponse
import csv
import json
import datetime
from covid_project.settings import BASE_DIR
from .db_processing import *


"""
 
 .##.....##....###....####.##....##....##....##....###....##.....##
 .###...###...##.##....##..###...##....###...##...##.##...##.....##
 .####.####..##...##...##..####..##....####..##..##...##..##.....##
 .##.###.##.##.....##..##..##.##.##....##.##.##.##.....##.##.....##
 .##.....##.#########..##..##..####....##..####.#########..##...##.
 .##.....##.##.....##..##..##...###....##...###.##.....##...##.##..
 .##.....##.##.....##.####.##....##....##....##.##.....##....###...
 
"""

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

def nyt_svot(request):
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

"""
 
 ....###....########..##.....##.####.##....##
 ...##.##...##.....##.###...###..##..###...##
 ..##...##..##.....##.####.####..##..####..##
 .##.....##.##.....##.##.###.##..##..##.##.##
 .#########.##.....##.##.....##..##..##..####
 .##.....##.##.....##.##.....##..##..##...###
 .##.....##.########..##.....##.####.##....##
 
"""

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

"""
 
 ..######..##.....##....###....########..########....##.....##.####.########.##......##..######.
 .##....##.##.....##...##.##...##.....##....##.......##.....##..##..##.......##..##..##.##....##
 .##.......##.....##..##...##..##.....##....##.......##.....##..##..##.......##..##..##.##......
 .##.......#########.##.....##.########.....##.......##.....##..##..######...##..##..##..######.
 .##.......##.....##.#########.##...##......##........##...##...##..##.......##..##..##.......##
 .##....##.##.....##.##.....##.##....##.....##.........##.##....##..##.......##..##..##.##....##
 ..######..##.....##.##.....##.##.....##....##..........###....####.########..###..###...######.
 
"""

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

