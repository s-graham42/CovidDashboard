# API Datasource Objects
import datetime
import pandas as pd
from .models import CsvFile, State

class NewYorkTimesData:
    source = "New York Times"  # string
    source_url = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv"

    def __init__(self):
        self.date = datetime.date.today()
        self.df = self.get_new_from_api()
    
    def __str__(self):
        return f"NYT api data {self.date}"
    
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
                this_state.loc[this_state.index[0], 'cases_d'] = this_state.loc[this_state.index[0], 'cases']
                this_state.loc[this_state.index[0], 'deaths_d'] = this_state.loc[this_state.index[0], 'deaths']

                    # appends each state in turn to new Data Frame
                new_frame = new_frame.append(this_state, ignore_index = True)

                    # cast calculated columns from float64 to int32
        new_frame = new_frame.astype({'cases_d': 'int32', 'deaths_d': 'int32'})

        return new_frame

    def get_all_by_state(self, fips, column):
        this_state = State.objects.get(fips=fips)
        this_data = self.df.loc[(self.df["fips"] == fips), ["date", "state", column]].sort_values(by=['date'])
        return {"state": this_state.name, "dates": this_data["date"].tolist(), "data": this_data[column].tolist()}

    def get_state_by_date_range(self, fips, start, end, column):
        this_state = State.objects.get(fips=fips)
        this_data = self.df.loc[(self.df["date"] >= start) & (self.df["date"] <= end) & (self.df["fips"] == fips), ["date", "state", column]].sort_values(by=['date'])
        # return dictionary state:state name, dates:list of dates, data:requested dataset 
        return {"state": this_state.name, "dates": this_data["date"].tolist(), "data": this_data[column].tolist()}

    #  FUTURE FUNCTIONALITY - STORE API-PULLED DATA AS A CSV FILE / DOESN'T WORK YET
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
