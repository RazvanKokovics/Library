import unittest
from domain import Book, Client, Rental, RentalDTO
from repository import Repo, RepositoryBooks, RepositoryClients, RepositoryRentals
from validators import ValidateBook, ValidateClient, ValidateInteger, ValidateRental, ValidateDate
from exceptions import NumericalError, RepositoryError, ValidationError, CommandError
import datetime
from services import Service
from undohandler import UndoHandler
from undomanager import UndoManager

class Test_First_Functionality(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def test_create_book(self):
        bookId = 20
        bookTitle = "Here I am"
        bookAuthor = "John Smith"
        b = Book(bookId, bookTitle, bookAuthor)
        

        assert(b.bookID == 20)
        assert(b.bookTitle == "Here I am")
        assert(b.bookAuthor == "John Smith")
        
        b.bookTitle = "New Title"
        assert(b.bookTitle == "New Title")
        
        b.bookAuthor = "New Author"
        assert(b.bookAuthor == "New Author")
        
        b2 = Book(20, "2nd Title", "2nd Author")
        assert(b == b2)
    
    def test_create_client(self):
        clientId = 15
        clientName = "George"
        c = Client(clientId, clientName)
        
        assert(c.clientID == 15)
        assert(c.clientName == "George")
        
        c1 = Client(15, None)
        c1.clientName = "Andrew"
        
        assert(c == c1)
        
    def test_add_book(self):
        repoBooks = Repo("Repobooks:")
        repoBooks.add(Book(1, "The Secret Crusade", "Oliver Bowden"))
        repoBooks.add(Book(2, "The Illustrated Man", "Ray Bradbury"))

        self.assertRaises(RepositoryError, lambda:repoBooks.add(Book(1, None, None)))
        
        assert(repoBooks.size() == 2)
        
        assert(repoBooks.get_all()[0].bookID == 1)
        assert(repoBooks.get_all()[1].bookID == 2)
        
        assert(repoBooks.get_all()[0].bookTitle == "The Secret Crusade")
        assert(repoBooks.get_all()[1].bookTitle == "The Illustrated Man")
        
        assert(repoBooks.get_all()[0].bookAuthor == "Oliver Bowden")
        assert(repoBooks.get_all()[1].bookAuthor == "Ray Bradbury")
        
    
    def test_add_client(self):
        repoClients = Repo("Repoclients:")
        repoClients.add(Client(20, "John Wright"))
        repoClients.add(Client(40, "Andrei Ivan"))
        
        assert(repoClients.size() == 2)
        
        assert(repoClients.get_all()[0].clientID == 20)
        assert(repoClients.get_all()[1].clientID == 40)
        
        assert(repoClients.get_all()[0].clientName == "John Wright")
        assert(repoClients.get_all()[1].clientName == "Andrei Ivan")
        
    def test_validate_book(self):
        validatorBooks = ValidateBook()
        b = Book(-50, "One", "Author")
        self.assertRaises(ValidationError, lambda:validatorBooks.validate_book(b))
        
        b = Book(50, "", "Author")
        self.assertRaises(ValidationError, lambda:validatorBooks.validate_book(b))
        
        b = Book(50, "One", "")
        self.assertRaises(ValidationError, lambda:validatorBooks.validate_book(b))
    
    def test_validate_client(self):
        validatorClients = ValidateClient()
        c = Client(-2, "Ionut")
        self.assertRaises(ValidationError, lambda:validatorClients.validate_client(c))

        c = Client(2, "")
        self.assertRaises(ValidationError, lambda:validatorClients.validate_client(c))
    
    def test_validate_integer(self):
        validatorInteger = ValidateInteger()
        
        with self.assertRaises(NumericalError) as context:
            validatorInteger.validate_integer("a9")
        self.assertTrue("\n[NUMERICAL ERROR] -> a9 is not an integer." in str(context.exception))
    
        self.assertRaises(NumericalError, lambda:validatorInteger.validate_integer("8a9"))
        self.assertRaises(NumericalError, lambda:validatorInteger.validate_integer("aa"))
    
    def test_validate_rental(self):
        validatorRental = ValidateRental()
        with self.assertRaises(ValidationError) as context:
            validatorRental.validate_rental(Rental(-2, Book(2, "Title2", "Author2"), Client(2, "Name2"), datetime.date(2019, 10, 6), datetime.date(2018, 10, 5)))
        self.assertTrue("\n[VALIDATION ERROR] -> Invalid Rental ID! Invalid returned Date!" in str(context.exception))
    
        self.assertRaises(ValidationError, lambda : validatorRental.validate_rental(Rental(-2, Book(2, "Title2", "Author2"), Client(2, "Name2"), datetime.date(2019, 10, 6), datetime.date(2018, 10, 5))))
    
    def test_validate_date(self):
        validatorDate = ValidateDate()
        self.assertRaises(NumericalError, lambda : validatorDate.validate_date(2018, 14, 90))
    
    def test_remove_book(self):
        repoBooks = Repo("Repobooks:")
        repoBooks.add(Book(1, "The Secret Crusade", "Oliver Bowden"))
        repoBooks.add(Book(2, "The Illustrated Man", "Ray Bradbury"))
        
        repoBooks.remove(Book(1, None, None))
        assert(repoBooks.size() == 1)
        assert(repoBooks.get_all()[0].bookID == 2)
        
        with self.assertRaises(RepositoryError) as context:
            repoBooks.remove(Book(22, None, None))
        self.assertTrue("\n[REPOSITORY ERROR] -> Repobooks: Inexistend ID!\n" in str(context.exception))
    
        #self.assertRaises(RepositoryError, lambda : repoBooks.remove(Book(22, None, None)))
    
    def test_remove_client(self):
        repoClients = Repo("Repoclients:")
        repoClients.add(Client(20, "John Wright"))
        repoClients.add(Client(40, "Andrei Ivan"))
        
        repoClients.remove(Client(40, None))
        assert(repoClients.size() == 1)
        assert(repoClients.get_all()[0].clientID == 20)

    def test_update_book(self):
        repoBooks = Repo("Repobooks:")
        repoBooks.add(Book(1, "The Secret Crusade", "Oliver Bowden"))
        repoBooks.add(Book(2, "The Illustrated Man", "Ray Bradbury"))
        
        repoBooks.update(Book(1, "New", "New2"))
        assert(repoBooks.get_all()[0].bookTitle == "New")
        assert(repoBooks.get_all()[0].bookAuthor == "New2")
        
        self.assertRaises(RepositoryError, lambda : repoBooks.update(Book(20, None, None)))
    
    def test_update_client(self):
        repoClients = Repo("Repoclients:")
        repoClients.add(Client(20, "John Wright"))
        repoClients.add(Client(40, "Andrei Ivan"))
        
        repoClients.update(Client(40, "New"))
        assert(repoClients.get_all()[1].clientName == "New")

    def test_search_book(self):
        repoBooks = Repo("Repobooks:")
        repoBooks.add(Book(1, "Title11", "Title12"))
        repoBooks.add(Book(2, "Title21", "Title22"))
        
        self.assertRaises(RepositoryError, lambda:repoBooks.search(Book(4, None, None)))
        b = repoBooks.search(Book(1, None, None))
        assert(b.bookTitle == "Title11")
        assert(b.bookAuthor == "Title12")

    def test_search_book_id(self):
        repoBooks = RepositoryBooks("Repobooks:")
        repoBooks.add(Book(1, "Title1", "Title2"))
        repoBooks.add(Book(12, "Title121", "Title122"))
        
        assert(len(repoBooks.searchBookId("1")) == 2)
        self.assertRaises(RepositoryError, lambda : repoBooks.searchBookId("8"))
    
    def test_search_book_author(self):
        repoBooks = RepositoryBooks("Repobooks:")
        repoBooks.add(Book(1, "Title1", "Title2"))
        repoBooks.add(Book(12, "Title121", "Title122"))
        
        assert(len(repoBooks.searchBookAuthor("iTl")) == 2)
        self.assertRaises(RepositoryError, lambda : repoBooks.searchBookAuthor("aa"))
    
    def test_search_book_title(self):
        repoBooks = RepositoryBooks("Repobooks:")
        repoBooks.add(Book(1, "Title1", "Title2"))
        repoBooks.add(Book(12, "Title121", "Title122"))
        
        assert(len(repoBooks.searchBookTitle("tLe")) == 2)
        self.assertRaises(RepositoryError, lambda : repoBooks.searchBookTitle("zz"))
    
    def test_get_all_authors(self):
        repoBooks = RepositoryBooks("Repobooks:")
        repoBooks.add(Book(1, "Title1", "Title2"))
        repoBooks.add(Book(2, "Title1", "Title2"))
        repoBooks.add(Book(12, "Title121", "Title122"))
        
        assert(len(repoBooks.get_all_authors()) == 2)
    
    def test_search_client_id(self):
        repoClients = RepositoryClients("Repoclients:")
        repoClients.add(Client(1, "Name1"))
        repoClients.add(Client(12, "Name12"))
        
        assert(len(repoClients.searchClientId("1")) == 2)
        self.assertRaises(RepositoryError, lambda : repoClients.searchClientId("8"))
    
    def test_search_client_name(self):
        repoClients = RepositoryClients("Repoclients:")
        repoClients.add(Client(1, "Name1"))
        repoClients.add(Client(12, "Name12"))
        
        assert(len(repoClients.searchClientName("aM")) == 2)
        self.assertRaises(RepositoryError, lambda : repoClients.searchClientName("8"))
    
    def test_search_unique(self):
        repoRental = RepositoryRentals("Reporentals:")
        repoRental.add(Rental(1, Book(1, "Title1", "Author1"), Client(1, "Name1"), datetime.date(2019, 10, 5), None))
        repoRental.add(Rental(2, Book(2, "Title2", "Author2"), Client(2, "Name2"), datetime.date(2019, 10, 6), None))
        
        self.assertRaises(RepositoryError, lambda : repoRental.search_unique(Rental(1, Book(2, "Title1", "Author1"), Client(1, "Name1"), datetime.date(2019, 10, 5), None)))
        self.assertRaises(RepositoryError, lambda : repoRental.search_unique(Rental(12, Book(1, "Title1", "Author1"), Client(1, "Name1"), datetime.date(2019, 10, 5), None)))
    
    def test_rental_remove_client(self):
        repoRental = RepositoryRentals("Reporentals:")
        repoRental.add(Rental(1, Book(1, "Title1", "Author1"), Client(1, "Name1"), datetime.date(2019, 10, 5), None))
        repoRental.add(Rental(2, Book(2, "Title2", "Author2"), Client(2, "Name2"), datetime.date(2019, 10, 6), None))
        
        repoRental.remove_client(1)
        assert(repoRental.size() == 1)
    
    def test_rental_remove_book(self):
        repoRental = RepositoryRentals("Reporentals:")
        repoRental.add(Rental(1, Book(1, "Title1", "Author1"), Client(1, "Name1"), datetime.date(2019, 10, 5), None))
        repoRental.add(Rental(2, Book(2, "Title2", "Author2"), Client(2, "Name2"), datetime.date(2019, 10, 6), None))
        
        repoRental.remove_book(2)
        assert(repoRental.size() == 1)
    
    def test_most_books(self):
        repoBooks = RepositoryBooks("Repobooks:")
        repoRental = RepositoryRentals("Reporentals:")
        
        repoBooks.add(Book(1, "Title1", "Author1"))
        repoBooks.add(Book(2, "Title2", "Author2"))
        repoRental.add(Rental(1, Book(1, "Title1", "Author1"), Client(1, "Name1"), datetime.date(2019, 10, 5), None))
        repoRental.add(Rental(2, Book(2, "Title2", "Author2"), Client(2, "Name2"), datetime.date(2019, 10, 6), None))
        
        b = repoBooks.get_all()
        blist = repoRental.most_books(b)
        assert(len(b) == len(blist))
        
    
    def test_most_clients(self):
        repoClients = RepositoryClients("Repoclients:")
        repoRental = RepositoryRentals("Reporentals:")
        
        repoClients.add(Client(1, "Name1"))
        repoClients.add(Client(2, "Name2"))
        repoRental.add(Rental(1, Book(1, "Title1", "Author1"), Client(1, "Name1"), datetime.date(2019, 10, 5), None))
        repoRental.add(Rental(2, Book(2, "Title2", "Author2"), Client(2, "Name2"), datetime.date(2019, 10, 6), datetime.date(2019, 10, 15)))
        
        c = repoClients.get_all()
        clist = repoRental.most_clients(c)
        assert(len(c) == len(clist))
    
    def test_most_authors(self):
        repoBooks = RepositoryBooks("Repobooks:")
        repoRental = RepositoryRentals("Reporentals:")
        
        repoBooks.add(Book(1, "Title1", "Author1"))
        repoBooks.add(Book(2, "Title2", "Author2"))
        repoRental.add(Rental(1, Book(1, "Title1", "Author1"), Client(1, "Name1"), datetime.date(2019, 10, 5), None))
        repoRental.add(Rental(2, Book(2, "Title2", "Author2"), Client(2, "Name2"), datetime.date(2019, 10, 6), None))
        
        a = repoBooks.get_all_authors()
        alist = repoRental.most_authors(a)
        assert(len(a) == len(alist))
    
    def test_book_str(self):
        b = Book(1, "Title1", "Author1")
        assert(str(b) == '|{:^5s}|{:<42s}|{:<42s}|'.format("1", "Title1", "Author1"))
    
    def test_client_str(self):
        c = Client(1, "Name1")
        assert(str(c) == '|{:^5s}|{:<42s}|'.format("1", "Name1"))
    
    def test_rental_DTO(self):
        rdt = RentalDTO(1, "Title1", "Name1", datetime.date(2019, 10, 6), None)
        rdt1 = RentalDTO(2, "Title1", "Name1", datetime.date(2019, 10, 6), datetime.date(2019, 10, 16))

        assert(str(rdt) == '|{:^5s}|{:<32s}|{:<32s}|{:^20s}|{:^20s}|'.format("1", "Title1", "Name1", "2019-10-06", "-"))
        assert(str(rdt1) == '|{:^5s}|{:<32s}|{:<32s}|{:^20s}|{:^20s}|'.format("2", "Title1", "Name1", "2019-10-06", "2019-10-16"))
    
    def test_command_error(self):
        cmd = ""
        with self.assertRaises(CommandError) as context:
            if cmd == "":
                raise CommandError("Enter is not an option.")
        self.assertTrue("\n[COMMAND ERROR] -> Enter is not an option." in str(context.exception))
    
class Test_SRV(unittest.TestCase):
    
    def setUp(self):
        repoBooks = RepositoryBooks("Repobooks:")
        repoClients = RepositoryClients("Repoclients:")
        repoRental = RepositoryRentals("Reporentals:")
        validatorBooks = ValidateBook()
        validatorClients = ValidateClient()
        validatorRental = ValidateRental()
        self.Srv = Service(repoBooks, repoClients, repoRental, validatorRental, validatorBooks, validatorClients)
    
    def test_srv_add_client(self):
        self.Srv.add_client(12, "Name1", True)
        assert(len(self.Srv.list_clients()) == 1)
        UndoManager.undo()
    
    def test_srv_remove_client(self):
        self.Srv.add_client(12, "Name1", True)
        self.Srv.add_client(13, "Name2", True)
        assert(len(self.Srv.list_clients()) == 2)
        self.Srv.remove_client(12, True)
        assert(len(self.Srv.list_clients()) == 1)
        UndoManager.undo()
    
    def test_srv_update_client(self):
        self.Srv.add_client(12, "Name1", True)
        self.Srv.update_client(12,"aaa", True)
        assert(self.Srv.list_clients()[0].clientName == "aaa")
        UndoManager.undo()
    
    def test_srv_add_book(self):
        self.Srv.add_book(12, "Title1", "Author1", True)
        assert(len(self.Srv.list_books()) == 1)
        UndoManager.undo()
    
    def test_srv_remove_book(self):
        self.Srv.add_book(12, "Title1", "Author1", True)
        self.Srv.add_book(14, "Title2", "Author1", True)
        assert(len(self.Srv.list_books()) == 2)
        self.Srv.remove_book(12, True)
        assert(self.Srv.get_no_books() == 1)
        UndoManager.undo()
    
    def test_srv_update_book(self):
        self.Srv.add_book(12, "Title", "Author", True)
        self.Srv.update_book(12, "aaa", "bbb", True)
        b = self.Srv.get_book_by_id(12)
        assert(b.bookTitle == "aaa")
        assert(b.bookAuthor == "bbb")
        UndoManager.undo()
    
    def test_srv_add_rental(self):
        self.Srv.add_book(1, "Title", "Author", True)
        self.Srv.add_client(1, "Name", True)
        self.Srv.add_rental(12, 1, 1, datetime.date(2019, 10, 11), None, True)
        self.Srv.update_rental(12, datetime.date(2019, 11, 10), True)
        assert(self.Srv.list_rental()[0]._rentalID == 12)
        UndoManager.undo()
    
    def test_srv_search_book(self):
        self.Srv.add_book(1, "Title1", "Author1", True)
        self.Srv.add_book(2, "iTas", "utal", True)
        assert(len(self.Srv.searchBookId(1)) == 1)
        assert(len(self.Srv.searchBookAuthor("uT")) == 2)
        assert(len(self.Srv.searchBookTitle("iT")) == 2)
        
    def test_srv_search_client(self):
        self.Srv.add_client(1, "First", True)
        self.Srv.add_client(12, "tira", True)
        assert(len(self.Srv.searchClientId(1)) == 2)
        assert(len(self.Srv.searchClientName("ir")) == 2)
    
    def test_srv_most_rented_books(self):
        self.Srv.add_book(1, "Title1", "Author1", True)
        self.Srv.add_book(2, "iTas", "utal", True)
        assert(len(self.Srv.list_most_rented_books()) == 2)
    
    def test_srv_most_active_clients(self):
        self.Srv.add_client(1, "First", True)
        self.Srv.add_client(12, "tira", True)
        assert(len(self.Srv.list_most_active_clients()) == 2)
        
    def test_srv_most_authors(self):
        self.Srv.add_book(1, "Title1", "Author1", True)
        self.Srv.add_book(2, "iTas", "utal", True)
        assert(len(self.Srv.list_most_authors()) == 2)
    
    def test_srv_remove_rental(self):
        self.Srv.add_book(1, "Title", "Author", True)
        self.Srv.add_client(1, "Name", True)
        self.Srv.add_rental(12, 1, 1, datetime.date(2019, 10, 11), None, True)
        self.Srv.remove_rental(12, True)
        assert(len(self.Srv.list_rental()) == 0)
        UndoManager.undo()
        
if __name__ == '__main__': 
    unittest.main()  
        