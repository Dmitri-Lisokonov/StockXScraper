import pyodbc

# Class for initialising database connection.
class ConnectionManager:
    conn = None
    cursor = None
    #add variables for connection.
    def __init__(self):
        self.conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                                   'Server=stockxscraper.database.windows.net;'
                                   'Database=stockxscraper;'
                                   'UID=stockx-database-username;'
                                   'PWD=Lodewijkhasib12!;'
                                   )
        self.cursor = self.conn.cursor()
