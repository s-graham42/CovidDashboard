# API Datasource Objects
import datetime
import os
import pandas as pd
from .models import CsvFile, State
from covid_project.settings import BASE_DIR


# """
 
#  88""Yb    db    .dP"Y8 888888      dP""b8 88        db    .dP"Y8 .dP"Y8 
#  88__dP   dPYb   `Ybo." 88__       dP   `" 88       dPYb   `Ybo." `Ybo." 
#  88""Yb  dP__Yb  o.`Y8b 88""       Yb      88  .o  dP__Yb  o.`Y8b o.`Y8b 
#  88oodP dP""""Yb 8bodP' 888888      YboodP 88ood8 dP""""Yb 8bodP' 8bodP' 
 
# """

# Base class for holdng api data pulled as a csv file in a pandas dataframe.
class DataSourceCSV:

    def __init__(self, name, url):
        self.source = name
        self.source_url = url
        self.date = datetime.date.today()
        self.df = self.get_new_dataframe()   # generates a new dataframe from a fresh api pull.

    def __str__(self):
        return f"{self.source} api data ({self.date})"
    
    def get_source(self):
        return self.source
    
    def get_source_url(self):
        return self.source_url

    def get_date(self):
        return self.date

    def get_df(self):
        return self.df

    def update_df(self):
        self.df = self.get_new_dataframe()

        # basic pull and read - does no transformations on data.
    def get_new_dataframe(self):
        api_df = pd.read_csv(self.source_url, parse_dates=True)

        return api_df


# """
 
#  88b 88 Yb  dP 888888     8888b.     db    888888    db    .dP"Y8  dP"Yb  88   88 88""Yb  dP""b8 888888 
#  88Yb88  YbdP    88        8I  Yb   dPYb     88     dPYb   `Ybo." dP   Yb 88   88 88__dP dP   `" 88__   
#  88 Y88   8P     88        8I  dY  dP__Yb    88    dP__Yb  o.`Y8b Yb   dP Y8   8P 88"Yb  Yb      88""   
#  88  Y8  dP      88       8888Y"  dP""""Yb   88   dP""""Yb 8bodP'  YbodP  `YbodP' 88  Yb  YboodP 888888 
 
# """

class NewYorkTimesStateData(DataSourceCSV):
    
    def __init__(self):
        self.source = "New York Times"  # string
        self.source_url = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv"
        self.source_file = BASE_DIR + "/media/current_api_data/NYTStates.csv"
        self.date = datetime.date.today()
        self.df = self.get_new_dataframe()

        # Check if the source file of cleaned data is from today.
    def file_is_from_today(self):
        if os.path.exists(self.source_file):
            file_date = datetime.datetime.fromtimestamp(os.path.getmtime(self.source_file)).strftime("%Y-%m-%d")
            today = datetime.datetime.now().strftime('%Y-%m-%d')
            if today == file_date:
                return True
        return False

        # We always want the most recent data.  Checks if the file we have is from today.
        # If so, get dataframe from that.  If not, run R script to pull and process API
        # data into csv and then use that to get a dataframe.
    def get_new_dataframe(self):
        if self.file_is_from_today():
            return pd.read_csv(self.source_file, parse_dates=True)
        else:
            os.system("Rscript " + BASE_DIR + "/Brad's_Work/Py_call_R_project/Cumu_To_Daily_NYT.R")
            return pd.read_csv(self.source_file, parse_dates=True)

                    # get all 'column' entries for a particular state (by fips number)
    def get_all_by_state(self, fips, column):
        this_state = State.objects.get(fips=fips)
        this_data = self.df.loc[(self.df["fips"] == fips), ["date", "state", column]].sort_values(by=['date'])
        return {"state": this_state.name, "dates": this_data["date"].tolist(), "data": this_data[column].tolist()}

                    # get all 'column' entries for a paticular state in a date range (start and end are strings yyyy-mm-dd)
    def get_state_by_date_range(self, fips, start, end, column):
        this_state = State.objects.get(fips=fips)
                    # get the date and 'column' values by state and date range.
        this_data = self.df.loc[(self.df["date"] >= start) & (self.df["date"] <= end) & (self.df["fips"] == fips), ["date", column]].sort_values(by=['date'])
                    # chart generation needs a list of tuples in the format ('date', 'value')
        this_xy = list(this_data.itertuples(index=False, name=None))
                    # return dictionary {state: state name, data: list of date, value tuples
        return {"state": this_state.name, "data": list(this_xy)}

    def get_column(self, interval, datapoint):
        if (interval == "cumulative" and datapoint == "cases"):
            return "cumu_cases"
        elif (interval == "cumulative" and datapoint == "deaths"):
            return "cumu_deaths"
        elif (interval == "daily" and datapoint == "cases"):
            return "daily_cases"
        elif (interval == "daily" and datapoint == "deaths"):
            return "daily_deaths"
        else:
            raise ValueError("Valid values are only 'cumulative' or 'daily', and 'cases' or 'deaths'.")


# """
 
#   dP""b8 8888b.   dP""b8     8888b.     db    888888    db    .dP"Y8  dP"Yb  88   88 88""Yb  dP""b8 888888 
#  dP   `"  8I  Yb dP   `"      8I  Yb   dPYb     88     dPYb   `Ybo." dP   Yb 88   88 88__dP dP   `" 88__   
#  Yb       8I  dY Yb           8I  dY  dP__Yb    88    dP__Yb  o.`Y8b Yb   dP Y8   8P 88"Yb  Yb      88""   
#   YboodP 8888Y"   YboodP     8888Y"  dP""""Yb   88   dP""""Yb 8bodP'  YbodP  `YbodP' 88  Yb  YboodP 888888 
 
# """

class CDCData(DataSourceCSV):
    
    def __init__(self):
        self.source = "CDC"  # string
        self.source_url = "https://data.cdc.gov/resource/9mfq-cb36.csv"
        self.date = datetime.date.today()
        self.df = self.get_new_dataframe()   # generates a new dataframe from a fresh api pull.
    
