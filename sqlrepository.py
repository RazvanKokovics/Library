#import pymssql
#import pyodbc
from exceptions import RepositoryError
import datetime
from domain import Book, Client, Rental

class SQLRepo():
    
    def __init__(self, Name, Table_Name):
        #self._conn = pymssql.connect('Trusted_Connection = yes', server = '(local)', user = 'admin', password = 'admin', database = 'Library')
        self._conn = pyodbc.connect(r'Driver={SQL Server};Server=DESKTOP-29D4507\SQLEXPRESS;Database=Library;Trusted_Connection = yes;')
        self._cursor = self._conn.cursor()
        self._name = Name
        self._table_name = Table_Name
        self._entities = []
            
    def size(self):
        #the size of the sql table
        cmd = 'SELECT COUNT(*) FROM ' + self._table_name + ';'
        self._cursor.execute(cmd)
        line = self._cursor.fetchone()
        return int(line[0])
    
class RepositoryBooks(SQLRepo):
    
    def read_data(self):
        #reads all the data from the sql table
        self._entities = []
        cmd = 'SELECT * FROM ' + self._table_name
        self._cursor.execute(cmd)
        line = self._cursor.fetchone()
        while line is not None:
            obj = Book(int(line[0]), line[1], line[2])
            self._entities.append(obj)
            line = self._cursor.fetchone()
    
    def get_all(self):
        #returns all the list from the repo
        self.read_data()
        return self._entities
    
    def add(self, obj):
        #adds a new object in the sql table
        cmd = "SELECT * FROM " + self._table_name + " WHERE Id=" + str(obj.bookID) + ";" 
        #self.read_data()
        #if obj in self._entities:
        self._cursor.execute(cmd)
        line = self._cursor.fetchone()
        if line is not None:
            raise RepositoryError(self._name + " Existing ID!\n")
        cmd = 'INSERT INTO ' + self._table_name + " VALUES ("+ str(obj.bookID) + ",'" + obj.bookTitle + "'," + obj.bookAuthor  + "');"
        self._cursor.execute(cmd)
        self._conn.commit()
        
    def search(self, keyobj):
        #returns an object with a specific key (keyobj) from the repo
        #raises a RepositoryError if the id is not in the repo
        #print(str(keyobj.bookID))
        cmd = "SELECT * FROM " + self._table_name + " WHERE Id=" + str(keyobj.bookID) + ";" 
        self._cursor.execute(cmd)
        line = self._cursor.fetchone()
        if line is None:
            raise RepositoryError(self._name + " Inexistent ID!\n")
        return Book(int(line[0]), line[1], line[2])
    
    def remove(self, obj):
        #removes an object from the repo
        #raises a RepositoryError if the obj does not exist
        b = self.search(obj)
        cmd = "DELETE FROM " + self._table_name + " WHERE Id=" + str(obj.bookID) + ";"
        self._cursor.execute(cmd)
        self._conn.commit()
    
    def update(self, obj):
        #updates an object from the repo
        #raises a RepositoryError if the object does not exist
        b = self.search(obj)
        cmd = "UPDATE " + self._table_name + " SET Title = '" + obj.bookTitle + "', Author = '" + obj.bookAuthor + "' WHERE Id=" + str(obj.bookID) + ";"
        self._cursor.execute(cmd)
        self._conn.commit()
    
    def searchBookId(self, bookId):
        self.read_data()
        l = []
        for book in self._entities:
            if str(book.bookID).find(str(bookId)) != -1:
                l.append(book)
        if len(l) > 0:
            return l
        else:
            raise RepositoryError(self._name + " No matching books were found!\n")

    def searchBookAuthor(self, bookAuthor):
        self.read_data()
        l = []
        for book in self._entities:
            if book.bookAuthor.lower().find(bookAuthor.lower()) != -1:
                l.append(book)
        if len(l) > 0:
            return l
        else:
            raise RepositoryError(self._name + " No matching books were found!\n")

    def searchBookTitle(self, bookTitle):
        self.read_data()
        l = []
        for book in self._entities:
            if book.bookTitle.lower().find(bookTitle.lower()) != -1:
                l.append(book)
        if len(l) > 0:
            return l
        else:
            raise RepositoryError(self._name + " No matching books were found!\n")
    
    def get_all_authors(self):
        alist = []
        cmd = "SELECT DISTINCT Author FROM " + self._table_name + ";"
        self._cursor.execute(cmd)
        line = self._cursor.fetchone()
        while line is not None:
            alist.append(line[0])
            line = self._cursor.fetchone()
        return alist
            
        
class RepositoryClients(SQLRepo):
    
    def read_data(self):
        #reads all the data from the sql table
        self._entities = []
        cmd = 'SELECT * FROM ' + self._table_name
        self._cursor.execute(cmd)
        line = self._cursor.fetchone()
        while line is not None:
            obj = Client(int(line[0]), line[1])
            self._entities.append(obj)
            line = self._cursor.fetchone()
    
    def get_all(self):
        #returns all the list from the repo
        self.read_data()
        return self._entities
    
    def add(self, obj):
        #adds a new object in the sql table
        cmd = "SELECT * FROM " + self._table_name + " WHERE Id=" + str(obj.clientID) + ";" 
        self._cursor.execute(cmd)
        line = self._cursor.fetchone()
        if line is not None:
            raise RepositoryError(self._name + " Existing ID!\n")
        cmd = 'INSERT INTO ' + self._table_name + " VALUES ("+ str(obj.clientID) + ",'" + obj.clientName + "');"
        self._cursor.execute(cmd)
        self._conn.commit()
        
    def search(self, keyobj):
        #returns an object with a specific key (keyobj) from the repo
        #raises a RepositoryError if the id is not in the repo
        #print(str(keyobj.bookID))
        cmd = "SELECT * FROM " + self._table_name + " WHERE Id=" + str(keyobj.clientID) + ";" 
        self._cursor.execute(cmd)
        line = self._cursor.fetchone()
        if line is None:
            raise RepositoryError(self._name + " Inexistent ID!\n")
        return Client(int(line[0]), line[1])
    
    def remove(self, obj):
        #removes an object from the repo
        #raises a RepositoryError if the obj does not exist
        b = self.search(obj)
        cmd = "DELETE FROM " + self._table_name + " WHERE Id=" + str(obj.clientID) + ";"
        self._cursor.execute(cmd)
        self._conn.commit()
    
    def update(self, obj):
        #updates an object from the repo
        #raises a RepositoryError if the object does not exist
        b = self.search(obj)
        cmd = "UPDATE " + self._table_name + " SET Name = '" + obj.clientName + "' WHERE Id=" + str(obj.clientID) + ";"
        self._cursor.execute(cmd)
        self._conn.commit()
        
    def searchClientId(self, clientId):
        self.read_data()
        c = []
        for client in self._entities:
            if str(client.clientID).find(str(clientId)) != -1:
                c.append(client)
        if len(c) > 0:
            return c
        else:
            raise RepositoryError(self._name + " No matching clients were found!\n")
    
    def searchClientName(self, clientName):
        self.read_data()
        c = []
        for client in self._entities:
            if client.clientName.lower().find(clientName.lower()) != -1:
                c.append(client)
        if len(c) > 0:
            return c
        else:
            raise RepositoryError(self._name + " No matching clients were found!\n")


class RepositoryRentals(SQLRepo):
    
    def read_data(self):
        #reads all the data from the sql table
        self._entities = []
        cmd = 'SELECT * FROM ' + self._table_name
        self._cursor.execute(cmd)
        line = self._cursor.fetchone()
        while line is not None:
            if line[4] is not None:
                obj = Rental(int(line[0]), Book(int(line[1]), None, None), Client(int(line[2]), None), datetime.datetime.strptime(line[3], '%Y-%m-%d').date(), datetime.datetime.strptime(line[4], '%Y-%m-%d').date())
            else:
                obj = Rental(int(line[0]), Book(int(line[1]), None, None), Client(int(line[2]), None), datetime.datetime.strptime(line[3], '%Y-%m-%d').date(), None)
            self._entities.append(obj)
            line = self._cursor.fetchone()
    
    def get_all(self):
        #returns all the list from the repo
        self.read_data()
        return self._entities
    
    def add(self, obj):
        #adds a new object in the sql table
        cmd = "SELECT * FROM " + self._table_name + " WHERE Id=" + str(obj.rentalID) + ";" 
        #self.read_data()
        #if obj in self._entities:
        self._cursor.execute(cmd)
        line = self._cursor.fetchone()
        if line is not None:
            raise RepositoryError(self._name + " Existing ID!\n")
        if obj.returnedDate is not None:
            cmd = 'INSERT INTO ' + self._table_name + " VALUES ("+ str(obj.rentalID) + "," + str(obj.book.bookID) + "," + str(obj.client.clientID) + ",'" + str(obj.rentedDate) + "','" + str(obj.returnedDate) + "');"
        else:
            cmd = 'INSERT INTO ' + self._table_name + " VALUES ("+ str(obj.rentalID) + "," + str(obj.book.bookID) + "," + str(obj.client.clientID) + ",'" + str(obj.rentedDate) + "', NULL " + ");"
        self._cursor.execute(cmd)
        self._conn.commit()
        
    def search(self, keyobj):
        #returns an object with a specific key (keyobj) from the repo
        #raises a RepositoryError if the id is not in the repo
        #print(str(keyobj.bookID))
        cmd = "SELECT * FROM " + self._table_name + " WHERE Id=" + str(keyobj.rentalID) + ";" 
        self._cursor.execute(cmd)
        line = self._cursor.fetchone()
        if line is None:
            raise RepositoryError(self._name + " Inexistent ID!\n")
        if line[4] is not None:
            obj = Rental(int(line[0]), Book(int(line[1]), None, None), Client(int(line[2]), None), datetime.datetime.strptime(line[3], '%Y-%m-%d').date(), datetime.datetime.strptime(line[4], '%Y-%m-%d').date())
        else:
            obj = Rental(int(line[0]), Book(int(line[1]), None, None), Client(int(line[2]), None), datetime.datetime.strptime(line[3], '%Y-%m-%d').date(), None)
        return obj
        
    def remove(self, obj):
        #removes an object from the repo
        #raises a RepositoryError if the obj does not exist
        b = self.search(obj)
        cmd = "DELETE FROM " + self._table_name + " WHERE Id=" + str(obj.rentalID) + ";"
        self._cursor.execute(cmd)
        self._conn.commit()
    
    def update(self, obj):
        #updates an object from the repo
        #raises a RepositoryError if the object does not exist
        b = self.search(obj)
        if obj.returnedDate is not None:
            cmd = "UPDATE " + self._table_name + " SET Returned = '" + str(obj.returnedDate) + "' WHERE Id=" + str(obj.rentalID) + ";"
        else:
            cmd = "UPDATE " + self._table_name + " SET Returned = NULL WHERE Id=" + str(obj.rentalID) + ";"
        self._cursor.execute(cmd)
        self._conn.commit()
        
    def search_unique(self, keyobj):
        self.read_data()
        for obj in self._entities:
            #if keyobj == obj:
            if keyobj.rentalID == obj.rentalID:
                raise RepositoryError(self._name + " Invalid ID!\n")
            elif keyobj.book.bookID == obj.book.bookID and obj.returnedDate is None:
                raise RepositoryError(self._name + " Book is already taken!\n")
    
    def remove_client(self, cid):
        self.read_data()
        l = []
        i = 0
        while i < self.size():
            if self._entities[i].client.clientID == int(cid):
                l.append(self._entities[i])
                cmd = "DELETE FROM " + self._table_name + " WHERE Id=" + str(self._entities[i].rentalID) + ";"
                self._cursor.execute(cmd)
            i = i + 1
        self._conn.commit()
        return l

               
    def remove_book(self, bid):
        self.read_data()
        l = []
        i = 0
        while i < self.size():
            if self._entities[i].book.bookID == int(bid):
                l.append(self._entities[i])
                cmd = "DELETE FROM " + self._table_name + " WHERE Id=" + str(self._entities[i].rentalID) + ";"
                self._cursor.execute(cmd)
            i = i + 1
        self._conn.commit()
        return l
        
           
    def most_books(self, blist_all):
        self.read_data()
        blist = []
        for b in blist_all:
            blist.append([b , 0])
        for obj in self._entities:
            for i in range(len(blist)):
                if obj.book == blist[i][0]:
                    blist[i][1] = blist[i][1] + 1
        blist = sorted(blist, key = lambda x : (-x[1] , x[0].bookID), reverse = False)           
        return blist
    
    def most_clients(self, clist_all):
        self.read_data()
        clist = []
        for c in clist_all:
            clist.append([c, 0])
        for obj in self._entities:
            for i in range(len(clist)):
                if obj.client == clist[i][0]:
                    if obj.returnedDate is not None:
                        clist[i][1] = clist[i][1] + int((obj.returnedDate - obj.rentedDate).days)
                    else:
                        clist[i][1] = clist[i][1] + int((datetime.date.today() - obj.rentedDate).days)
        clist = sorted(clist, key = lambda x : (-x[1] , x[0].clientID), reverse = False)           
        return clist
    
    def most_authors(self, alist_all):
        self.read_data()
        alist = []
        for a in alist_all:
            alist.append([a, 0])
        for j in range(len(self._entities)):
            for i in range(len(alist)):
                if self._entities[j].book.bookAuthor == alist[i][0]:
                    alist[i][1] = alist[i][1] + 1
        alist = sorted(alist, key = lambda x : (-x[1] , x[0]), reverse = False)           
        return alist
    
    