# API Datasource Objects
import datetime
import pandas as pd
from .models import CsvFile

class NewYorkTimesData:
    def __init__(self):
        self.source = "New York Times"
        self.csv_file = None
        self.df = None
    
    def get_new_from_api(self):
                    # Get new csv file from NYTimes Github page
        api_file = pd.read_csv("https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv", parse_dates=True)
        
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

        print(new_frame)
        return new_frame
        # write dataframe to csv file
        # store as a CSV_File object
        # return CSV_File object

    def store_dataframe_as_CSVFile(self, dataframe):
        today = datetime.date.today().strftime("%Y-%m-%d")
        new_name = (f"New_York_Times-{today}")
        new_desc = (f"Pulled from New York Times github on {today}")
        new_file = dataframe.to_csv(f"./NYT-{today}.csv")
        new_CsvFile = CsvFile.objects.create(name=new_name, description=new_desc, file=new_file)
        return new_CsvFile
