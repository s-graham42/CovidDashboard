""" Module for methods to upload and process csv files into the sqlite database """

from .forms import CsvFileForm
from .models import CsvFile, State
import csv
import datetime
from covid_project.settings import BASE_DIR

def load_states_only():
    """ Creates State objects in sqlite database with info from /Brad's_Work/Py_call_R_project/States_Abb_FIPS.csv """

    with open(BASE_DIR + "/Transparency/Py_call_R_project/States_Abb_FIPS.csv") as csv_file:
        opened_file = csv.reader(csv_file, delimiter=',')
        # Name,Abbreviation,FIPS
        row_count = 0
        for row in opened_file:
            if row[0] == "Name":
                row_count += 1
            else:
                State.objects.update_or_create(defaults={'name': row[0], 'abbreviation': row[1]}, fips=row[2])
                row_count += 1

def check_and_create_states(file_to_load):
    """ Creates State objects in sqlite database from an uploaded .csv file """

    checked_states = []
    with open(BASE_DIR + file_to_load.file.url) as csv_file:
        opened_file = csv.reader(csv_file, delimiter=',')
        row_count = 0 # keep track of which row you're on
        this_fips = 0 # initialize so you're not creating it every time
        for row in opened_file:
            if row[0] == "date":
                row_count += 1
            else:
                this_fips = int(row[2])
                if this_fips not in checked_states:
                    # see if the state fips is already in the database
                    this_state = State.objects.filter(fips = int(row[2]))
                    # if it is, put the fips in checked_states
                    if len(this_state) > 0:
                        this_state = this_state[0]
                        checked_states.append(this_state.fips)
                    else:
                        # if not, create the state
                        new_state = State.objects.create(name = row[1], file = file_to_load, fips = int(row[2]))
                        # add fips int to checked_states
                        checked_states.append(new_state.fips)
                row_count += 1
    return checked_states
