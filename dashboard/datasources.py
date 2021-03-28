# API Datasource Objects
import datetime
import pandas as pd
from .models import CsvFile, State


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
        self.df = self.get_new_from_api()   # generates a new dataframe from a fresh api pull.

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
        self.df = self.get_new_from_api()

        # basic pull and read - does no transformations on data.
    def get_new_from_api(self):
        api_df = pd.read_csv(self.source_url, parse_dates=True)

        return api_df


# """
 
#  88b 88 Yb  dP 888888     8888b.     db    888888    db    .dP"Y8  dP"Yb  88   88 88""Yb  dP""b8 888888 
#  88Yb88  YbdP    88        8I  Yb   dPYb     88     dPYb   `Ybo." dP   Yb 88   88 88__dP dP   `" 88__   
#  88 Y88   8P     88        8I  dY  dP__Yb    88    dP__Yb  o.`Y8b Yb   dP Y8   8P 88"Yb  Yb      88""   
#  88  Y8  dP      88       8888Y"  dP""""Yb   88   dP""""Yb 8bodP'  YbodP  `YbodP' 88  Yb  YboodP 888888 
 
# """

class NewYorkTimesData(DataSourceCSV):
    
    def __init__(self):
        self.source = "New York Times"  # string
        self.source_url = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv"
        self.date = datetime.date.today()
        self.df = self.get_new_from_api()

    def get_new_from_api(self):
                    # Get new csv file from NYTimes Github page
        api_file = pd.read_csv(self.source_url, parse_dates=True)
        
        max_fips = max(api_file['fips'])
        new_frame = pd.DataFrame()
                    # Calculate Daily Cases and Deaths
        for i in range(1, max_fips + 1):        
            this_state = api_file[api_file['fips'] == i].sort_values(by=['date'])
            if len(this_state) == 0:
                continue
            else:
                this_state['cases_d'] = this_state['cases'].diff()
                this_state['deaths_d'] = this_state['deaths'].diff()
                    # after .diif(), first item in new series is NaN.  Assign value from cumulative data to that item.
                this_state.loc[this_state.index[0], 'cases_d'] = this_state.loc[this_state.index[0], 'cases']
                this_state.loc[this_state.index[0], 'deaths_d'] = this_state.loc[this_state.index[0], 'deaths']

                    # append each state in turn to new Data Frame
                new_frame = new_frame.append(this_state, ignore_index = True)

                    # cast calculated columns from float64 to int32
        new_frame = new_frame.astype({'cases_d': 'int32', 'deaths_d': 'int32'})

        return new_frame

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
            return "cases"
        elif (interval == "cumulative" and datapoint == "deaths"):
            return "deaths"
        elif (interval == "daily" and datapoint == "cases"):
            return "cases_d"
        elif (interval == "daily" and datapoint == "deaths"):
            return "deaths_d"
        else:
            raise ValueError("Valid values are only 'cumulative' or 'daily', and 'cases' or 'deaths'.")


    #  FUTURE FUNCTIONALITY - STORE API-PULLED DATA AS A CSV FILE IN DATABASE / DOESN'T WORK YET
        # write dataframe to csv file
        # store as a CsvFile object
        # return CsvFile object

    # def store_dataframe_as_CSVFile(self, dataframe):
    #     today = datetime.date.today().strftime("%Y-%m-%d")
    #     new_name = (f"New_York_Times-{today}")
    #     new_desc = (f"Pulled from New York Times github on {today}")
    #     new_file = dataframe.to_csv(f"./NYT-{today}.csv")
    #     new_CsvFile = CsvFile.objects.create(name=new_name, description=new_desc, file=new_file)
    #     return new_CsvFile

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
        self.df = self.get_new_from_api()   # generates a new dataframe from a fresh api pull.
    
