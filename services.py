from domain import Book, Client, Rental, RentalDTO
from undohandler import UndoHandler
from undomanager import UndoManager

class Service():
    
    def __init__(self, repoBooks, repoClients, repoRental, validatorRental, validatorBook, validatorClients):
        #self._repoBooks = repoBooks
        #self._repoClients = repoClients
        self._repoRental = repoRental
        self._validatorRental = validatorRental
        
        self._booksList = repoBooks
        self._validator = validatorBook
        
        self._clientsList = repoClients
        self._validatorClient = validatorClients
    
    def add_client(self, clientId, clientName, u):
        #adds a new client to the list of clients
        #clientID = (int) the client ID, clientName = (str) the name of the client
        client = Client(clientId, clientName)
        self._validatorClient.validate_client(client)
        self._clientsList.add(client)
        if u == True:
            UndoManager.register_operation(self, UndoHandler.ADD_CLIENT, int(clientId), clientName)
        
        
    def remove_client(self, clientId, u):
        #removes a client from the list of clients
        #clientId = (str) the client ID which has to be removed
        client = Client(clientId, None)
        client = self._clientsList.search(client)
        #print(client.clientName)
        self._clientsList.remove(client)
        if u == True:
            rlist = self._repoRental.remove_client(int(clientId))
            UndoManager.register_operation(self, UndoHandler.REMOVE_CLIENT, clientId, client.clientName, rlist)
            
    def update_client(self, clientId, clientName, u):
        #updates a client with a new Title and a new Author
        #clientId = (str) the client ID which has to be updated
        #clientName = (str) the new client Name
        client = Client(clientId, clientName)
        self._validatorClient.validate_client(client)
        client2 = self._clientsList.search(client)
        self._clientsList.update(client)
        if u == True:
            UndoManager.register_operation(self, UndoHandler.UPDATE_CLIENT, client2.clientID, client2.clientName)
        
        
    def list_clients(self):
        #returns a list with all the clients  
        return self._clientsList.get_all()
    
    def add_book(self, bookId, bookName, bookAuthor, u):
        #adds a new book to the list of books
        #bookId = (str) the book ID, bookName = (str) the name of the book, bookAuthor = (str) the Author of the book
        book = Book(bookId, bookName, bookAuthor)
        self._validator.validate_book(book)
        self._booksList.add(book)
        if u == True:
            UndoManager.register_operation(self, UndoHandler.ADD_BOOK, int(bookId), bookName, bookAuthor)
    
    def remove_book(self, bookId, u):
        #removes a book from the list of books
        #bookId = (str) the book ID which has to be removed
        book = Book(int(bookId), None, None)
        book = self._booksList.search(book)
        self._booksList.remove(book)
        #self._repoRental.remove_book(int(bookId))
        blist = self._repoRental.remove_book(int(bookId))
        if u == True:
            UndoManager.register_operation(self, UndoHandler.REMOVE_BOOK, int(bookId), book.bookTitle, book.bookAuthor, blist)
        
    
    def update_book(self, bookId, bookTitle, bookAuthor, u):
        #updates a book with a new Title and a new Author
        #bookId = (str) the book ID which has to be updated
        #bookTitle = (str) the new book Title
        #bookAuthor = (str) the new book Author
        book = Book(bookId, bookTitle, bookAuthor)
        self._validator.validate_book(book)
        
        book2 = self._booksList.search(book)
        self._booksList.update(book)
        if u == True:
            UndoManager.register_operation(self, UndoHandler.UPDATE_BOOK, book2.bookID, book2.bookTitle, book2.bookAuthor)
    """
    def update_book_redo(self, bookId, bookTitle, bookAuthor):
        #updates a book with a new Title and a new Author
        #bookId = (str) the book ID which has to be updated
        #bookTitle = (str) the new book Title
        #bookAuthor = (str) the new book Author
        book = Book(bookId, bookTitle, bookAuthor)
        self._validator.validate_book(book)
        
        book2 = self._booksList.search(book)
        self._booksList.update(book)
        UndoManager.register_operation(self, UndoHandler.UPDATE_BOOK, book2.bookID, book2.bookTitle, book2.bookAuthor)
     """   
        
    def list_books(self):  
        #returns a list with all the books
        return self._booksList.get_all()
    
    def get_no_books(self):
        #returns the number of books
        return self._booksList.size()
        
    def get_book_by_id(self, b_id):
        key = Book(b_id, None, None)
        return self._booksList.search(key)
    
    def add_rental(self, rentalId, bookId, clientId, rentedDate, returnedDate, u):
        #adds a new rental to the list of rentals
        #rentalID = (int) the rental ID
        #bookID = (int) the book ID
        #clientID = (int) the client ID
        #rentedDate = (date) the rentedDate
        #returnedDate = (date) the returnedDate
        rent = Rental(rentalId, Book(bookId, None, None), Client(clientId, None), rentedDate, returnedDate)
        book = self._booksList.search(rent.book)
        client = self._clientsList.search(rent.client)
        rent = Rental(rentalId, book, client, rentedDate, returnedDate)
        self._validatorRental.validate_rental(rent)
        self._repoRental.search_unique(rent)
        self._repoRental.add(rent)
        if u == True:
            UndoManager.register_operation(self, UndoHandler.ADD_RENTAL, int(rentalId), int(bookId), int(clientId), rentedDate, returnedDate)
        
    
    def update_rental(self, rentalId, returnedDate, u):
        #updates a rental by adding its returnedDate
        #rentalID = (int) the rental ID
        #returnedDate = (date) the returnedDate
        rent = Rental(rentalId, None, None, None, returnedDate)
        book = self._repoRental.search(rent).book
        client = self._repoRental.search(rent).client
        rentedDate = self._repoRental.search(rent).rentedDate
        rent = Rental(rentalId, book, client, rentedDate, returnedDate)
        self._validatorRental.validate_rental(rent)
        rent2 = self._repoRental.search(rent)
        self._repoRental.update(rent)
        if u == True:
            UndoManager.register_operation(self, UndoHandler.UPDATE_RENTAL, int(rentalId), book.bookID, client.clientID, rentedDate, rent2.returnedDate)
    
    def remove_rental(self, rentalId, u):
        rent = Rental(int(rentalId), None, None, None, None)
        rent = self._repoRental.search(rent)
        #print(self._repoRental.size())
        self._repoRental.remove(rent)
        if u == True:
            UndoManager.register_operation(self, UndoHandler.REMOVE_RENTAL, rent.rentalID, rent.book.bookID, rent.client.clientID, rent.rentedDate, rent.returnedDate)
    
    def list_rental(self):
        #returns a list with all the rentals
        rlist = self._repoRental.get_all()
        rez = []
        for rent in rlist:
            bookTitle = self._booksList.search(rent.book).bookTitle
            clientName = self._clientsList.search(rent.client).clientName
            rentDTO = RentalDTO(rent.rentalID, bookTitle, clientName, rent.rentedDate, rent.returnedDate)
            rez.append(rentDTO)
        return rez
    
    def searchBookId(self, bookId):
        return self._booksList.searchBookId(bookId)
    
    def searchBookAuthor(self, bookAuthor):
        return self._booksList.searchBookAuthor(bookAuthor)
   
    def searchBookTitle(self, bookTitle):
        return self._booksList.searchBookTitle(bookTitle)
    
    def searchClientId(self, clientId):
        return self._clientsList.searchClientId(clientId)
    
    def searchClientName(self, clientName):
        return self._clientsList.searchClientName(clientName)
    
    def list_most_rented_books(self):
        blist_all = self._booksList.get_all()
        return self._repoRental.most_books(blist_all)
        
    def list_most_active_clients(self):
        clist_all = self._clientsList.get_all()
        return self._repoRental.most_clients(clist_all)
    
    def list_most_authors(self):
        alist_all = self._booksList.get_all_authors()
        return self._repoRental.most_authors(alist_all)