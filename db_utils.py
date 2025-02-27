import mysql.connector
from contextlib import contextmanager
from dotenv import load_dotenv
import os
load_dotenv()

DATABASE_CONFIG = {
    "host": os.getenv("HOST"),
    "user": os.getenv("USER"),
    "password": os.getenv("PASSWORD"),
    "database": os.getenv("DATABASE"),
}


class Database:

    def __init__(self):

        self.connection = None
        self.cursor = None

    @contextmanager
    def get_db_connection(self):

        try:

            self.connection = mysql.connector.connect(**DATABASE_CONFIG)
            self.cursor = self.connection.cursor()
            yield self.cursor

        except Exception as error:

            print(f"Error connecting to database -> db_utils() -> get_db_connection(): {error}")


        finally:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()


    def execute_query(self,query,params=None):
        

        try:

            with self.get_db_connection() as cursor:

                cursor.execute(query,params)
                
                return cursor.fetchall()
            
        except Exception as error:

            print(f"Error connecting to database -> db_utils() -> execute_query(): {error}")

            return None
