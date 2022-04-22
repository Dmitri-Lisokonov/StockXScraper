import pyodbc
import logging

# Class for initialising database connection.
class ConnectionManager:
    conn = None
    cursor = None

    # add variables for connection.
    def __init__(self):
        try:
            self.conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server}; '
                                    'Server=stockxscraper.database.windows.net;'
                                    'Database=XXXXXXX'
                                    'UID=XXXXXXXX'
                                    'PWD=XXXXXXXX;'
                                    )
            self.cursor = self.conn.cursor()
        except Exception as e:
            logging.critical(f"Could not initialze connectionmanager => {e}")
            raise e
