import pyodbc

class SQLRepo():
    
    def __init__(self, Name):
        self._conn = pyodbc('Driver = {SQL Server};'
                            'Server = server_name;'
                            'Database = db_name;'
                            'Trusted_Connection = yes;')
        self._cursor = self._conn.cursor()
        self._name = Name
        self._entities = []
        
    def cmd(self):
        self._cursor.execute('SELECT * FROM Library.dbo.Books')
        for row in self._cursor:
            print(row)