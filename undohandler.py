from enum import Enum

from redohandler import RedoHandler
from redomanager import RedoManager
from domain import Book, Client, Rental

def add_book_undo_handler(srv, bookId, bookTitle, bookAuthor):
    #print(bookId)
    #print(bookTitle)
    #print(bookAuthor)
    RedoManager.register_operation(srv, RedoHandler.REMOVE_BOOK, bookId, bookTitle, bookAuthor)
    #srv._booksList.remove
    srv.remove_book(bookId, False)
    
def add_client_undo_handler(srv, clientId, clientName):
    RedoManager.register_operation(srv, RedoHandler.REMOVE_CLIENT, clientId, clientName)
    srv.remove_client(clientId, False)

def add_rental_undo_handler(srv, rentalId, bookId, clientId, rentedDate, returnedDate):
    
    RedoManager.register_operation(srv, RedoHandler.REMOVE_RENTAL, rentalId, bookId, clientId, rentedDate, returnedDate)
    srv.remove_rental(rentalId, False)

def remove_book_undo_handler(srv, bookId, bookTitle, bookAuthor, rlist):
    RedoManager.register_operation(srv, RedoHandler.ADD_BOOK, bookId, bookTitle, bookAuthor, rlist)
    srv.add_book(int(bookId), bookTitle, bookAuthor, False)
    for rent in rlist:
        srv.add_rental(rent.rentalID, rent.book.bookID, rent.client.clientID, rent.rentedDate, rent.returnedDate, False)
      
def remove_client_undo_handler(srv, clientId, name, rlist):
    RedoManager.register_operation(srv, RedoHandler.ADD_CLIENT, clientId, name, rlist)
    #print(len(rlist))
    #srv._clientsList.add(Client(clientId, name))
    srv.add_client(int(clientId), name, False)
    for rent in rlist:
        srv.add_rental(rent.rentalID, rent.book.bookID, rent.client.clientID, rent.rentedDate, rent.returnedDate, False)
        #srv._repoRental.add(rental)

def remove_rental_undo_handler(srv, rentalId, bookId, clientId, rentedDate, returnedDate):
    RedoManager.register_operation(srv, RedoHandler.ADD_RENTAL, rentalId, bookId, clientId, rentedDate, returnedDate)
    srv.add_rental(rentalId, bookId, clientId, rentedDate, returnedDate, False)

def update_book_undo_handler(srv, bookId, bookTitle, bookAuthor):
    #print(int(bookId))
    #print(bookTitle)
    #print(bookAuthor)     
    blist = srv.list_books()
    for book in blist:
        if book.bookID == int(bookId):
            RedoManager.register_operation(srv, RedoHandler.UPDATE_BOOK, book.bookID, book.bookTitle, book.bookAuthor)
            break
    srv.update_book(bookId, bookTitle, bookAuthor, False)


def update_client_undo_handler(srv, clientId, name):
    clients = srv.list_clients()
    for client in clients:
        if client.clientID == int(clientId):
            RedoManager.register_operation(srv, RedoHandler.UPDATE_CLIENT, client.clientID, client.clientName)
            break
    srv.update_client(clientId, name, False)

def update_rental_undo_handler(srv, rentalId, bookId, clientId, rentedDate, returnedDate):
    rentals = srv._repoRental.get_all()
    for rent in rentals:
        if rent.rentalID == rentalId:
            RedoManager.register_operation(srv, RedoHandler.UPDATE_RENTAL, rentalId, bookId, clientId, rentedDate, rent.returnedDate)
            break
    srv.update_rental(rentalId, returnedDate, False)

class UndoHandler (Enum):
    ADD_BOOK = add_book_undo_handler 
    REMOVE_BOOK = remove_book_undo_handler
    UPDATE_BOOK = update_book_undo_handler
    ADD_CLIENT = add_client_undo_handler
    REMOVE_CLIENT = remove_client_undo_handler
    UPDATE_CLIENT = update_client_undo_handler
    ADD_RENTAL = add_rental_undo_handler
    REMOVE_RENTAL = remove_rental_undo_handler
    UPDATE_RENTAL = update_rental_undo_handler

