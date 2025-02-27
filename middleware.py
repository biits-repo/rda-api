from fastapi import FastAPI, Depends, HTTPException
import pandas as pd
from db_utils import Database
from save_csv import CreateCsv
import os

db_obj = Database()


current_directory = os.getcwd()



def get_middleware_sponsor():

    query = "SELECT * FROM sponsor"
    result = db_obj.execute_query(query)
    
    sponsor_list = []
    
    for i in result:

        sponsor = {}
        sponsor['sponsor_id'] = i[0]
        sponsor['sponsor_name'] = i[1]

        sponsor_list.append(sponsor)
    
    return {"data":sponsor_list}

    


def get_middleware_sponsor_occurence():

    try:
        query = "SELECT * FROM sponsor_occurence"
        result = db_obj.execute_query(query)
        
        csv_obj = CreateCsv(result)
        csv_path = csv_obj.create_csv()
        csv_abs_path = os.path.join(current_directory / csv_path)
        if csv_path:
            return {"csv_path": csv_abs_path}
        else:
            return {"message": "csv creation failed"}

    except Exception as e:

        print(f"miidleware script -> get_middleware_sponsor_occurence() -> error {e}")


