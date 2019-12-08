#import pymssql
import pyodbc

class SQLRepo():
    
    def __init__(self, Name):
        #self._conn = pymssql.connect('Trusted_Connection = yes', server = '(local)', user = 'admin', password = 'admin', database = 'Library')
        self._conn = pyodbc.connect(r'Driver={SQL Server};Server=DESKTOP-29D4507\SQLEXPRESS;Database=Library;Trusted_Connection = yes;')
        self._cursor = self._conn.cursor()
        self._name = Name
        self._entities = []
        
    def cmd(self):
        self._cursor.execute('SELECT * FROM dbo.Table_Books')
        line = self._cursor.fetchone()
        while line is not None:
            print(str(line[0]) + ' ' + line[1] + ' ' + line[2])
            line = self._cursor.fetchone()
        #for row in self._cursor:
            #print(row)