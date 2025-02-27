import pandas as pd
from pathlib import Path
import logging


logging.basicConfig()



class CreateCsv:

    def __init__(self,sponsor_occurence_list):

        self.sponsor_occurence = sponsor_occurence_list
        self.csv = Path("CSV")
        self.csv.mkdir(exist_ok=True)


    def create_csv(self):
        
        try:
            self.data = {}

            self.data["audio_id"] = [val[1] for val in self.sponsor_occurence]
            self.data["chunk_id"] = [val[2] for val in self.sponsor_occurence]
            self.data["sponsor_id"] = [val[3] for val in self.sponsor_occurence]
            self.data["sponsor_frequency"] = [val[4] for val in self.sponsor_occurence]

            df = pd.DataFrame(self.data)
            csv_path = self.csv / "sponsor_occurence.csv"
            df.to_csv(csv_path)

            return csv_path

        except Exception as error:
            print("Error in creating csv file: save_csv script -> create_csv()  ",error)





