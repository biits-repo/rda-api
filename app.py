from fastapi import FastAPI, Depends, HTTPException
import mysql.connector
from mysql.connector import Error
from middleware import *
import pandas as pd
from dotenv import load_dotenv 
import os
load_dotenv()

# FastAPI app
app = FastAPI(
    title="Sponsors API",
    description="Here is the complete description of all the API'S",
    version="1.0.0"
    )

# DATABASE_CONFIG = {
#     "host": os.getenv("HOST"),
#     "user": os.getenv("USER"),
#     "password": os.getenv("PASSWORD"),
#     "database": os.getenv("DATABASE"),
# }



@app.get("/sponsors")
def get_sponsors():
    
    """
        This endpoint returns a list of all sponsors in the database.
    """

    sponsor_data = get_middleware_sponsor()

    return sponsor_data


@app.get("/occurences")
def get_sponsor_occurence():

    """
        This endpoint returns a list of all sponsors occurence in the database.
    """

    csv_path = get_middleware_sponsor_occurence()

    return {"csv_path": csv_path}







# Run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
