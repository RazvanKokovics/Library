#import pymssql
import pyodbc
from exceptions import RepositoryError
import datetime

class SQLRepo():
    
    def __init__(self, Name, Table_Name, read_object, write_object):
        #self._conn = pymssql.connect('Trusted_Connection = yes', server = '(local)', user = 'admin', password = 'admin', database = 'Library')
        self._conn = pyodbc.connect(r'Driver={SQL Server};Server=DESKTOP-29D4507\SQLEXPRESS;Database=Library;Trusted_Connection = yes;')
        self._cursor = self._conn.cursor()
        self._name = Name
        self._table_name = Table_Name
        self._read_object = read_object
        self._write_object = write_object
        self._entities = []
    
    def read_data(self):
        #reads all the data from the sql table
        self._entities = []
        cmd = 'SELECT * FROM ' + self._table_name
        self._cursor.execute(cmd)
        line = self._cursor.fetchone()
        while line is not None:
            obj = self._read_object(line)
            self._entities.append(obj)
            line = self._cursor.fetchone()
        print(self._entities)
    
    def cmd(self):
        self._cursor.execute('SELECT * FROM dbo.Table_Books')
        line = self._cursor.fetchone()
        while line is not None:
            print(str(line[0]) + ' ' + line[1] + ' ' + line[2])
            line = self._cursor.fetchone()
        #for row in self._cursor:
            #print(row)
            
    def size(self):
        #the size of the sql table
        cmd = 'SELECT COUNT(*) FROM ' + self._table_name + ';'
        self._cursor.execute(cmd)
        line = self._cursor.fetchone()
        return int(line[0])
    
    def add(self, obj):
        #adds a new object in the sql table
        self.read_data()
        if obj in self._entities:
            raise RepositoryError(self._name + " Existing ID!\n")
        cmd = 'INSERT INTO ' + self._table_name + self._write_object(obj) + ';'
        self._cursor.execute(cmd)
        self._conn.commit()
        
    def search(self, keyobj):
        #returns an object with a specific key (keyobj) from the repo
        #raises a RepositoryError if the id is not in the repo
        self.read_data()
        if keyobj not in self._entities:
            raise RepositoryError(self._name + " Inexistent ID!\n")
        for obj in self._entities:
            if obj == keyobj:
                return obj
    
    def remove(self, obj):
        #removes an object from the repo
        #raises a RepositoryError if the obj does not exist
        self.read_data()
        i = 0
        y = self.size()
        #print(self.size())
        while i < self.size():
            if self._entities[i] == obj:
                
                del self._entities[i]
                return
            i = i + 1
        if y == self.size():
            raise RepositoryError(self._name + " Inexistend ID!\n")
    
    def update(self, obj):
        #updates an object from the repo
        #raises a RepositoryError if the object does not exist
        self.read_data()
        for i in range(len(self._entities)):
            if self._entities[i] == obj:
                self._entities[i] = obj
                return
        raise RepositoryError(self._name + " Inexistend ID!\n")
        
    def get_all(self):
        #returns all the list from the repo
        self.read_data()
        return self._entities
    
class RepositoryBooks(SQLRepo):
    
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
        self.read_data()
        alist = []
        for b in self._entities:
            found = False
            for i in range(len(alist)):
                if b.bookAuthor == alist[i]:
                    found = True
            if found == False:
                alist.append(b.bookAuthor)
        return alist
            
        
class RepositoryClients(SQLRepo):
    
    def searchClientId(self, clientId):
        self.read_data()
        c = []
        for client in self._entities:
            if str(client.clientID).find(str(clientId)) != -1:
                c.append(client)
        if len(c) > 0:
            return c
        else:
            raise RepositoryError(self._name + " No matching books were found!\n")
    
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
                del self._entities[i]
            i = i + 1
        return l

               
    def remove_book(self, bid):
        self.read_data()
        l = []
        i = 0
        while i < self.size():
            if self._entities[i].book.bookID == int(bid):
                l.append(self._entities[i])
                del self._entities[i]
            i = i + 1
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
    
    