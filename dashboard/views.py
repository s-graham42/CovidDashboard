from django.shortcuts import render, HttpResponse, redirect
from .forms import CsvFileForm
from .models import CsvFile, State, Entry
from django.http import JsonResponse
import csv
import json
import datetime
from covid_project.settings import BASE_DIR

# Create your views here.
def index(request):
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
    return render(request, "index.html", context)

def demo_charts(request):
    return render(request, "demo_charts.html")

def upload_csv(request):
    if request.method == "POST":
        form = CsvFileForm(request.POST, request.FILES)
        if form.is_valid():
            new_name = form.cleaned_data['name']
            new_desc = form.cleaned_data['description']
            new_file = form.cleaned_data['file']
            CsvFile.objects.create(name=new_name, description=new_desc, file=new_file)
            return redirect("/upload_success")
    else:
        form = CsvFileForm()
    return render(request, "upload_csv.html", {'form' : form})

def upload_success(request):
    context = {
        'all_files' : CsvFile.objects.all(),
    }
    return render(request, "upload_success.html", context)

def db_load_csv(request, id):
    if request.method == "POST":
        file_to_load = CsvFile.objects.filter(id=id)
        if len(file_to_load) > 0:
            file_to_load = file_to_load[0]
            with open(BASE_DIR + file_to_load.file.url) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                row_count = 0
                for row in csv_reader:
                    if row[0] == "date":
                        row_count += 1
                    else:
                        # "date","state","fips","cases","deaths"
                        print(f"processing row {row_count}")
                        this_state = State.objects.update_or_create(defaults={'name': row[1], 'file': file_to_load}, fips=int(row[2]))
                        this_state = this_state[0]
                        entry_date = datetime.datetime.strptime(row[0], "%Y-%m-%d").date()
                        previous_entries = Entry.objects.filter(state=this_state, date__lt=entry_date)
                        # print(previous_entries)
                        if len(previous_entries) == 0:
                            Entry.objects.update_or_create(defaults={'cases_c': int(row[3]),'cases_d': int(row[3]), 'deaths_c': int(row[4]), 'deaths_d': int(row[4])}, date=entry_date, state=this_state)
                            row_count += 1
                        else:
                            # "date","state","fips","cases","deaths"
                            previous_entry = previous_entries.latest('date')
                            print("prev entry: " + str(previous_entry))
                            daily_cases = (int(row[3]) - previous_entry.cases_c)
                            daily_deaths = (int(row[4]) - previous_entry.deaths_c)
                            Entry.objects.update_or_create(defaults={'cases_c': int(row[3]),'cases_d': daily_cases, 'deaths_c': int(row[4]), 'deaths_d': daily_deaths}, date=entry_date, state=this_state)
                            row_count += 1
                return redirect(f'/db_load_success/{row_count}')
    return redirect('/upload_success')

def db_load_sucess(request, row_count):
    context = {
        'row_count' : row_count,
    }
    return render(request, "db_load_success.html", context)

# ----------  Chart Views ----------

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

def fourStatesDailyCases(request):  # doesn't work yet
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



