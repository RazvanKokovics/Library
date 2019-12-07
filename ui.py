#---------------IMPORT SECTION-------------------
import datetime
from exceptions import CommandError, NumericalError
from redomanager import RedoManager
from undomanager import UndoManager
from undohandler import UndoHandler
#------------------------------------------------


class Console:
    
    def __init__(self, Service, ValidateInteger, ValidateDate):
        self._srv = Service
        self._validateinteger = ValidateInteger
        self._validatedate = ValidateDate
        
    @staticmethod
    def printTitle():
        #prints the title
        dash = "-" * 50
        print("{:^50s}".format("LIBRARY MANAGEMENT SYSTEM"))
        print(dash)     
        
    @staticmethod
    def printMenu():
        #prints the whole Menu
        dash = "-" * 50
        
        #-------THE MENU
        #manage
        print()
        print("MANAGE:")
        print("  1. Manage the list of books.")
        print("  2. Manage the list of clients.")
        print(dash)
        
        #rent or return
        print("RENT OR RETURN:")
        print("  3. Rent a book.")
        print("  4. Return a book.")
        print(dash)
        
        #search
        print("SEARCH:")
        print("  5. Search a specific book.") 
        print("  6. Search a specific client.")
        print(dash)
        
        #statistics
        print("STATISTICS:")
        print("  7. List the most rented books.")
        print("  8. List the most active clients.")
        print("  9. List the most rented authors.")    
        print(dash)
        
        #undo / redo
        print("  10. List rentals.")
        print("  11. Undo.")
        print("  12. Redo.")
        print("  13. Exit.")
        print(dash)
        print()
    
    def getCommand(self):
        #gets the command from the user and calls the validation functions
        cmd = input("Please choose an option from above: ")
        print()
        if cmd == "":
            raise CommandError("Enter is not an option.")
        self._validateinteger.validate_integer(cmd)
        return str(cmd)
    
    #########################################################
    #                                                       #
    #                                                       #
    #_______________________BOOKS MENU______________________#
    #                                                       #
    #                                                       #
    #########################################################
    @staticmethod
    def printManageBooks():
        print()
        print("BOOKS MENU:")
        print("1. Add a new book.")
        print("2. Remove a book.")
        print("3. Update a book.")
        print("4. List books.")
        print("5. Back.")
        print()
    
    def addBook(self):
        #asks the user for data regarding the book and calls the add function from services
        bookId = input("Book ID: ")
        bookTitle = input("Book Title: ")
        bookAuthor = input("Book Author: ")
        self._validateinteger.validate_integer(bookId)
        bookId = int(bookId)
        self._srv.add_book(bookId, bookTitle, bookAuthor, True)
        RedoManager.delete()
        
    def removeBook(self):
        #asks the user for the id of the book he wants to delete and calls the remove function from services
        bookId = input("Book ID: ")
        self._validateinteger.validate_integer(bookId)
        self._srv.remove_book(bookId, True)
        RedoManager.delete()
    
    def updateBook(self):
        #updates a given book by its ID 
        #asks the user for the id of the book he wants to modify and for the new data 
        bookId = input("Book ID: ")
        self._validateinteger.validate_integer(bookId)
        bookTitle = input("New book Title: ")
        bookAuthor = input("New book Author: ")
        self._srv.update_book(bookId, bookTitle, bookAuthor, True)
        RedoManager.delete()
        
    def listBooks(self):
        #prints the list of books in a tabel
        blist = self._srv.list_books()
        dash = '-' * 100
        print(dash)
        print('|{:^6s}|{:^5s}|{:^42s}|{:^42s}|'.format("NUMBER", "ID", "NAME", "AUTHOR"))        
        print(dash)
        for i in range(len(blist)):
            print('|{:^6s}'.format(str(i+1)) + str(blist[i]))
        print(dash)
              
    def manageBooks(self):
        commands = {
            "1" : self.addBook,
            "2" : self.removeBook,
            "3" : self.updateBook,
            "4" : self.listBooks
        }
        while True:
            self.printManageBooks()
            try:
                command = self.getCommand()
                if command == "5":
                    break
                self.callCommand(commands,command)
            except Exception as ex:
                print(str(ex))
    
    #########################################################
    #                                                       #
    #                                                       #
    #______________________CLIENTS MENU_____________________#
    #                                                       #
    #                                                       #
    #########################################################
    @staticmethod
    def printManageClients():
        print()
        print("CLIENTS MENU:")
        print("1. Add a new client.")
        print("2. Remove a client.")
        print("3. Update a client.")
        print("4. List clients.")
        print("5. Back.")
        print()
    
    def addClient(self):
        #asks the user for data regarding the client and calls the add function from services
        clientId = input("Client ID: ")
        clientName = input("Client Name: ")
        self._validateinteger.validate_integer(clientId)
        self._srv.add_client(clientId, clientName, True)
        RedoManager.delete()
    
    def removeClient(self):
        #asks the user for the id of the client he wants to delete and calls the remove function from services
        clientId = input("Client ID: ")
        self._validateinteger.validate_integer(clientId)
        self._srv.remove_client(clientId, True)
        RedoManager.delete()

    
    def updateClient(self):
        #updates a given client by its ID 
        #asks the user for the id of the client he wants to modify and for the new data 
        clientId = input("Client ID: ")
        self._validateinteger.validate_integer(clientId)
        clientName = input("New client Name: ")
        self._srv.update_client(clientId, clientName, True)
        RedoManager.delete()
    
    def listClients(self):
        #prints the list of clients in a tabel
        dash = '-' * 57
        print(dash)
        print('|{:^6s}|{:^5s}|{:^42s}|'.format('Number', 'ID', 'Name'))
        print(dash)
        clist = self._srv.list_clients()
        for i in range(len(clist)):
            print('|{:^6s}'.format(str(i+1)) + str(clist[i]))
        print(dash)
    
    def manageClients(self):
        commands = {
            "1" : self.addClient,
            "2" : self.removeClient,
            "3" : self.updateClient,
            "4" : self.listClients
        }
        while True:
            self.printManageClients()
            try:
                command = self.getCommand()
                if command == "5":
                    break
                self.callCommand(commands,command)
            except Exception as ex:
                print(str(ex))
 
    def rentBook(self):
        rentalId = input("Enter rental ID: ")
        bookId = input("Enter book ID: ")
        clientId = input("Enter client ID: ")
        self._validateinteger.validate_integer(bookId)
        self._validateinteger.validate_integer(clientId)
        self._validateinteger.validate_integer(rentalId)
        rentedDate = datetime.date.today()
        self._srv.add_rental(rentalId, bookId, clientId, rentedDate, None, True)
        RedoManager.delete()  
        
    def returnBook(self):
        rentalId = input("Enter rental ID: ")
        self._validateinteger.validate_integer(rentalId)
        print("Enter returned date... ")
        returned_day = input("Enter returned day: ")
        returned_month = input("Enter returned month: ")
        returned_year = input("Enter returned year: ")
        self._validateinteger.validate_integer(returned_day)
        self._validateinteger.validate_integer(returned_month)
        self._validateinteger.validate_integer(returned_year)
        self._validatedate.validate_date(int(returned_day), int(returned_month), int(returned_year))
        self._srv.update_rental(int(rentalId), datetime.date(int(returned_year), int(returned_month), int(returned_day)), True)
        RedoManager.delete()
        
    def printRental(self):
        dash = '-' * 115
        print(dash)
        print('|{:^5s}|{:<32s}|{:<32s}|{:^20s}|{:^20s}|'.format('ID', 'Book Title', 'Client Name', 'Rented Date', 'Returned Date'))
        print(dash)
        rlist = self._srv.list_rental()
        for rent in rlist:
            print(rent)
        print(dash)
    
    @staticmethod
    def printSearchBook():
        print()
        print("Search Books:")
        print("1. Search by ID.")
        print("2. Search by Title.")
        print("3. Search by Author.")
        print("4. Back.")
        print()
    
    def searchBookByID(self):
        bookId = input("Book ID: ")
        self._validateinteger.validate_integer(bookId)
        blist = self._srv.searchBookId(int(bookId))
        dash = '-' * 100 
        print(dash)
        print('|{:^6s}|{:^5s}|{:^42s}|{:^42s}|'.format("NUMBER", "ID", "NAME", "AUTHOR"))        
        print(dash)
        for i in range(len(blist)):
            print('|{:^6s}'.format(str(i+1)) + str(blist[i]))
        print(dash)
    
    def searchBookByAuthor(self):
        bookAuthor = input("Book Author: ")
        blist = self._srv.searchBookAuthor(bookAuthor)
        dash = '-' * 100 
        print(dash)
        print('|{:^6s}|{:^5s}|{:^42s}|{:^42s}|'.format("NUMBER", "ID", "NAME", "AUTHOR"))        
        print(dash)
        for i in range(len(blist)):
            print('|{:^6s}'.format(str(i+1)) + str(blist[i]))
        print(dash)
    
    def searchBookByTitle(self):
        bookTitle = input("Book Title: ")
        blist = self._srv.searchBookTitle(bookTitle)
        dash = '-' * 100 
        print(dash)
        print('|{:^6s}|{:^5s}|{:^42s}|{:^42s}|'.format("NUMBER", "ID", "NAME", "AUTHOR"))        
        print(dash)
        for i in range(len(blist)):
            print('|{:^6s}'.format(str(i+1)) + str(blist[i]))
        print(dash) 
       
    def searchBook(self):
        commands = {
            "1" : self.searchBookByID,
            "2" : self.searchBookByTitle,
            "3" : self.searchBookByAuthor
        }
        while True:
            self.printSearchBook()
            try:
                command = self.getCommand()
                if command == "4":
                    break
                self.callCommand(commands,command)
            except Exception as ex:
                print(str(ex))
    
    @staticmethod
    def printSearchClient():
        print()
        print("Search Clients:")
        print("1. Search by ID.")
        print("2. Search by Name.")
        print("3. Back.")
        print()
    
    def searchClientByID(self):
        clientId = input("Client ID: ")
        self._validateinteger.validate_integer(clientId)
        clist = self._srv.searchClientId(int(clientId))
        dash = '-' * 57
        print(dash)
        print('|{:^6s}|{:^5s}|{:^42s}|'.format('Number', 'ID', 'Name'))
        print(dash)
        for i in range(len(clist)):
            print('|{:^6s}'.format(str(i+1)) + str(clist[i]))
        print(dash)
    
    def searchClientByName(self):
        clientName = input("Client Name: ")
        clist = self._srv.searchClientName(clientName)
        dash = '-' * 57
        print(dash)
        print('|{:^6s}|{:^5s}|{:^42s}|'.format('Number', 'ID', 'Name'))
        print(dash)
        for i in range(len(clist)):
            print('|{:^6s}'.format(str(i+1)) + str(clist[i]))
        print(dash)
    
    def searchClient(self):
        commands = {
            "1" : self.searchClientByID,
            "2" : self.searchClientByName
        }
        while True:
            self.printSearchClient()
            try:
                command = self.getCommand()
                if command == "3":
                    break
                self.callCommand(commands,command)
            except Exception as ex:
                print(str(ex))
    
    def mostrentedbooks(self):
        #prints the list of books in a tabel
        blist = self._srv.list_most_rented_books()
        dash = '-' * 100
        print(dash)
        print('|{:^6s}|{:^5s}|{:^42s}|{:^42s}|'.format("NUMBER", "ID", "NAME", "AUTHOR"))        
        print(dash)
        for i in range(len(blist)):
            print('|{:^6s}'.format(str(blist[i][1])) + str(blist[i][0]))
        print(dash)
        
    def mostactiveclients(self):
        dash = '-' * 57
        print(dash)
        print('|{:^6s}|{:^5s}|{:^42s}|'.format('Act', 'ID', 'Name'))
        print(dash)
        clist = self._srv.list_most_active_clients()
        for i in range(len(clist)):
            print('|{:^6s}'.format(str(clist[i][1])) + str(clist[i][0]))
        print(dash)
    
    def mostauthor(self):
        dash = '-' * 51
        print(dash)
        print('|{:^6s}|{:^42s}|'.format('Points', 'Name'))
        print(dash)
        alist = self._srv.list_most_authors()
        for i in range(len(alist)):
            print('|{:^6s}|{:<42s}|'.format(str(alist[i][1]), str(alist[i][0])))
        print(dash)
    
    def undo(self):
        UndoManager.undo()

    def redo(self):
        RedoManager.redo()
    
    def callCommand(self, commands, command):
        #calls the specific function in a given dict
        if command not in commands:
            raise CommandError(str(command) + " is not an option.")
        commands[command]()
            
    def run(self):
        #the run function
        self.printTitle()
        commands = {
            "1" : self.manageBooks,
            "2" : self.manageClients,
            "3" : self.rentBook,
            "4" : self.returnBook,
            "5" : self.searchBook,
            "6" : self.searchClient,
            "7" : self.mostrentedbooks,
            "8" : self.mostactiveclients,
            "9" : self.mostauthor,
            "10" : self.printRental,
            "11" : self.undo,
            "12" :self.redo
        }
        while True:
            self.printMenu()
            try:
                command = self.getCommand()
                if command == "13":
                    break
                self.callCommand(commands,command)
            except Exception as ex:
                print(str(ex))
                
        