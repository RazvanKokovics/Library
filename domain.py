from datetime import datetime
from dates import get_date
#-------------------------------BOOOK-----------------------
class Book(object):
    
    def __init__(self, bookID, title, author):
        #initializes the book object
        self._bookID = int(bookID)
        self._bookTitle = title
        self._bookAuthor = author

#----------GETTERS AND SETTERS-----------   
    @property
    def bookID(self):
        #returns the ID of a book
        return self._bookID
    
    @property
    def bookTitle(self):
        #returns the Title of a book
        return self._bookTitle
    
    @bookTitle.setter
    def bookTitle(self, newTitle):
        #changes the Title of a book with a new one
        #newTitle = the new Title of the book
        self._bookTitle = newTitle
    
    @property
    def bookAuthor(self):
        #returns the Author of a book
        return self._bookAuthor
    
    @bookAuthor.setter
    def bookAuthor(self, newAuthor):
        self._bookAuthor = newAuthor
    
    def __eq__(self, other):
        #checks if two books have the same id
        return self._bookID == other.bookID
    
    def __str__(self):
        #returns the str format of the book
        return '|{:^5s}|{:<42s}|{:<42s}|'.format(str(self._bookID), self._bookTitle, self._bookAuthor)
    
    @staticmethod
    def read_book(line):
        parts = line.split(",")
        return Book(int(parts[0].strip()),parts[1].strip(),parts[2].strip())
    
    @staticmethod
    def write_book(book):
        return str(book._bookID) + ',' + book._bookTitle + ',' + book._bookAuthor     

#-------------------------------CLIENT-----------------------


class Client(object):
    
    def __init__(self, clientID, clientName):
        #initializes the client object
        self._clientID = int(clientID)
        self._clientName = clientName
    
#----------GETTERS AND SETTERS-----------
    
    @property
    def clientID(self):
        #returns the ID of a client
        return self._clientID
    
    @property
    def clientName(self):
        #returns the name of a client
        return self._clientName
    
    @clientName.setter
    def clientName(self, newName):
        #changes the Name of a client with a new one
        #newName = the new Name of the client
        self._clientName = newName

    def __eq__(self, other):
        #checks if two clients have the same id
        return self._clientID == other.clientID
    
    def __str__(self):
        #returns the str format of the book
        return '|{:^5s}|{:<42s}|'.format(str(self._clientID), self._clientName)

    @staticmethod
    def read_client(line):
        parts = line.split(",")
        return Client(int(parts[0].strip()),parts[1].strip())
    
    @staticmethod
    def write_client(client):
        return str(client._clientID) + ',' + client._clientName 
    
#-------------------------------RENTAL-------------------
class Rental(object):
    #initializes the rent object
    def __init__(self, rentalID, book, client, rentedDate, returnedDate):
        self._rentalID = int(rentalID)
        self._book = book
        self._client = client
        self._rentedDate = rentedDate
        self._returnedDate = returnedDate
    
#----------GETTERS AND SETTERS-----------
    
    @property
    def rentalID(self):
        return self._rentalID
    
    @property
    def book(self):
        return self._book
    
    @property
    def client(self):
        return self._client
    
    @property
    def rentedDate(self):
        return self._rentedDate
    
    @property
    def returnedDate(self):
        return self._returnedDate
    
    def __eq__(self, other):
        return self._rentalID == other.rentalID

    @staticmethod
    def read_rental(line):
        parts = line.split(",")
        if parts[7].strip() != '-':
            return Rental(int(parts[0].strip()),Book(int(parts[1].strip()),parts[2].strip(),parts[3].strip()),Client(int(parts[4].strip()),parts[5].strip()),get_date(parts[6].strip()),get_date(parts[7].strip()))
        else:
            return Rental(int(parts[0].strip()),Book(int(parts[1].strip()),parts[2].strip(),parts[3].strip()),Client(int(parts[4].strip()),parts[5].strip()),get_date(parts[6].strip()),None)
    
    @staticmethod
    def write_rental(rent):
        if rent._returnedDate is not None:
            return str(rent._rentalID) + ',' + str(rent.book.bookID) + ',' + rent.book.bookTitle + ',' + rent.book.bookAuthor + ',' + str(rent.client.clientID) + ',' + rent.client.clientName + ',' + str(rent.rentedDate) + ',' + str(rent.returnedDate)
        else:
            return str(rent._rentalID) + ',' + str(rent.book.bookID) + ',' + rent.book.bookTitle + ',' + rent.book.bookAuthor + ',' + str(rent.client.clientID) + ',' + rent.client.clientName + ',' + str(rent.rentedDate) + ',-'
        
                
class RentalDTO(object):
    
    def __init__(self, rentalID, bookTitle, clientName, rentedDate, returnedDate):
        self._bookTitle = bookTitle
        self._clientName = clientName
        self._rentedDate = rentedDate
        self._rentalID = rentalID
        if str(returnedDate) == "None":
            self._returnedDate = "-"
        else:
            self._returnedDate = returnedDate
        
    def __str__(self):
        return '|{:^5s}|{:<32s}|{:<32s}|{:^20s}|{:^20s}|'.format(str(self._rentalID), self._bookTitle, self._clientName, str(self._rentedDate), str(self._returnedDate))