from enum import Enum
from domain import Book, Client, Rental

def remove_book_redo_handler(srv, bookId, bookTitle, bookAuthor):
    srv.add_book(bookId, bookTitle, bookAuthor, True)

def remove_client_redo_handler(srv, clientId, name):
    srv.add_client(clientId, name, True)

def remove_rental_redo_handler(srv, rentalId, bookId, clientId, rentedDate, returnedDate):
    srv.add_rental(rentalId, bookId, clientId, rentedDate, returnedDate, True)

def add_book_redo_handler(srv, bookId, booktitle, bookAuthor, rlist):
    srv.remove_book(bookId, True)
    #for rental in rlist:
        #srv.remove_rental(rental.rentalID)

def add_client_redo_handler(srv, clientId, name, rlist):
    srv.remove_client(int(clientId), True)
    #srv._clientsList.remove(Client(clientId, name))
    #print(len(rlist))
    #for rent in rlist:
        #print(rent.rentalID)
    #srv._repoRental.remove_client(int(clientId))
        #srv._repoRental.remove(rent)

def add_rental_redo_handler(srv, rentalId, bookId, clientId, rentedDate, returnedDate):
    srv.remove_rental(rentalId, True)

def update_book_redo_handler(srv, bookId, bookTitle, bookAuthor):
    srv.update_book(bookId, bookTitle, bookAuthor, True)

def update_client_redo_handler(srv, clientId, name):
    srv.update_client(clientId, name, True)

def update_rental_redo_handler(srv, rentalId, bookId, clientId, rentedDate, returnedDate):
    srv.update_rental(rentalId, returnedDate, True)

class RedoHandler(Enum):
    REMOVE_BOOK = remove_book_redo_handler
    REMOVE_CLIENT = remove_client_redo_handler
    REMOVE_RENTAL = remove_rental_redo_handler
    ADD_BOOK = add_book_redo_handler
    ADD_CLIENT = add_client_redo_handler
    ADD_RENTAL = add_rental_redo_handler
    UPDATE_BOOK = update_book_redo_handler
    UPDATE_CLIENT = update_client_redo_handler
    UPDATE_RENTAL = update_rental_redo_handler
