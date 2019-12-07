from exceptions import RepositoryError
import datetime

class Repo(object):
    
    def __init__(self, Name):
        self._name = Name
        self._entities = []
        
    def size(self):
        #returns the size of the repo
        return len(self._entities)
    
    def add(self, obj):
        #adds a new object (obj) to the repo
        #raises a RepositoryError if the id of the obj is invalid
        if obj in self._entities:
            raise RepositoryError(self._name + " Existing ID!\n")
        self._entities.append(obj)
        
    def search(self, keyobj):
        #returns an object with a specific key (keyobj) from the repo
        #raises a RepositoryError if the id is not in the repo
        if keyobj not in self._entities:
            raise RepositoryError(self._name + " Inexistent ID!\n")
        for obj in self._entities:
            if obj == keyobj:
                return obj
    
    def remove(self, obj):
        #removes an object from the repo
        #raises a RepositoryError if the obj does not exist
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
        for i in range(len(self._entities)):
            if self._entities[i] == obj:
                self._entities[i] = obj
                return
        raise RepositoryError(self._name + " Inexistend ID!\n")
    
    def get_all(self):
        #returns all the list from the repo
        return self._entities

class RepositoryBooks(Repo):
    
    def searchBookId(self, bookId):
        l = []
        for book in self._entities:
            if str(book.bookID).find(str(bookId)) != -1:
                l.append(book)
        if len(l) > 0:
            return l
        else:
            raise RepositoryError(self._name + " No matching books were found!\n")

    def searchBookAuthor(self, bookAuthor):
        l = []
        for book in self._entities:
            if book.bookAuthor.lower().find(bookAuthor.lower()) != -1:
                l.append(book)
        if len(l) > 0:
            return l
        else:
            raise RepositoryError(self._name + " No matching books were found!\n")

    def searchBookTitle(self, bookTitle):
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
        for b in self._entities:
            found = False
            for i in range(len(alist)):
                if b.bookAuthor == alist[i]:
                    found = True
            if found == False:
                alist.append(b.bookAuthor)
        return alist
            
        
class RepositoryClients(Repo):
    
    def searchClientId(self, clientId):
        c = []
        for client in self._entities:
            if str(client.clientID).find(str(clientId)) != -1:
                c.append(client)
        if len(c) > 0:
            return c
        else:
            raise RepositoryError(self._name + " No matching books were found!\n")
    
    def searchClientName(self, clientName):
        c = []
        for client in self._entities:
            if client.clientName.lower().find(clientName.lower()) != -1:
                c.append(client)
        if len(c) > 0:
            return c
        else:
            raise RepositoryError(self._name + " No matching clients were found!\n")


class RepositoryRentals(Repo):
    def search_unique(self, keyobj):
        for obj in self._entities:
            #if keyobj == obj:
            if keyobj.rentalID == obj.rentalID:
                raise RepositoryError(self._name + " Invalid ID!\n")
            elif keyobj.book.bookID == obj.book.bookID and obj.returnedDate is None:
                raise RepositoryError(self._name + " Book is already taken!\n")
    
    def remove_client(self, cid):
        l = []
        i = 0
        while i < self.size():
            if self._entities[i].client.clientID == int(cid):
                l.append(self._entities[i])
                del self._entities[i]
            i = i + 1
        return l
               
    def remove_book(self, bid):
        l = []
        i = 0
        while i < self.size():
            if self._entities[i].book.bookID == int(bid):
                l.append(self._entities[i])
                del self._entities[i]
            i = i + 1
        return l
           
    def most_books(self, blist_all):
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
        alist = []
        for a in alist_all:
            alist.append([a, 0])
        for j in range(len(self._entities)):
            for i in range(len(alist)):
                if self._entities[j].book.bookAuthor == alist[i][0]:
                    alist[i][1] = alist[i][1] + 1
        alist = sorted(alist, key = lambda x : (-x[1] , x[0]), reverse = False)           
        return alist