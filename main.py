from ui import Console
from services import Service



from validators import ValidateBook, ValidateClient, ValidateInteger, ValidateRental, ValidateDate
from domain import Book, Client, Rental
import datetime
from settings import Settings
#from sqlrepository import SQLRepo

if __name__=="__main__":
    
    #_____________SETTINGS.PROPERTIES____________
    settings = Settings("settings.properties")
    f = settings.get_format()
    
    if f == "INMEMORY":
        from repository import RepositoryBooks, RepositoryClients, RepositoryRentals
        repoClients = RepositoryClients("Repoclients:")
        repoBooks = RepositoryBooks("Repobooks:")
        repoRental = RepositoryRentals("Reporentals:")
    elif f == "TEXTFILES":
        from textrepository import RepositoryBooks, RepositoryClients, RepositoryRentals
        files = settings.get_txt()
        repoBooks = RepositoryBooks("Repobooks:", files[0], Book.read_book, Book.write_book)
        repoClients = RepositoryClients("Repoclients:", files[1], Client.read_client, Client.write_client)
        repoRental = RepositoryRentals("Reporentals:", files[2], Rental.read_rental, Rental.write_rental)
    elif f == "BYNARYFILES":
        from picklerepository import RepositoryBooks, RepositoryClients, RepositoryRentals
        files = settings.get_bynary()
        repoBooks = RepositoryBooks("Repobooks:", files[0])
        repoClients = RepositoryClients("Repoclients:", files[1])
        repoRental = RepositoryRentals("Reporentals:", files[2])
    elif f == "JSONFILES":
        from jsonrepository import RepositoryBooks, RepositoryClients, RepositoryRentals
        files = settings.get_bynary()
        repoBooks = RepositoryBooks("Repobooks:", files[0])
        repoClients = RepositoryClients("Repoclients:", files[1])
        repoRental = RepositoryRentals("Reporentals:", files[2])
    elif f == "SQLDATABASE":
        from sqlrepository import RepositoryBooks, RepositoryClients, RepositoryRentals
        files = settings.get_sql()
        repoBooks = RepositoryBooks("Repobooks:", files[0])
        repoClients = RepositoryClients("Repoclients:", files[1])
        repoRental = RepositoryRentals("Reporentals:", files[2])
    
           
    #____________________________________________
    
    
    
    #VALIDATORS
    validatorBooks = ValidateBook()
    
    validatorClients = ValidateClient()
    validatorRental = ValidateRental()
    
    #SERVICES
    
    Srv = Service(repoBooks, repoClients, repoRental, validatorRental, validatorBooks, validatorClients)
    
    
    validatorInteger = ValidateInteger()
    validatorDate = ValidateDate()
    
    
    #hard-generate
    #________________BOOKS______________________________________________________
    repoBooks.add(Book(1, "The Secret Crusade", "Oliver Bowden"))
    repoBooks.add(Book(2, "The Illustrated Man", "Ray Bradbury"))
    repoBooks.add(Book(3, "The Glass Castle", "Jeannette Walls"))
    repoBooks.add(Book(4, "Still Alice", "Lisa Genova"))
    repoBooks.add(Book(5, "Olive, Again", "Elizabeth Strout"))
    repoBooks.add(Book(6, "The Nightshift Before Christmas", "Adam Kay"))
    repoBooks.add(Book(7, "The Tales of Beedle the Bard", "J K Rowling"))
    repoBooks.add(Book(8, "This is Going to Hurt", "Adam Kay"))
    repoBooks.add(Book(9, "Old new", "Oliver Bowden"))
    repoBooks.add(Book(10, "Quidditch Through the Ages", "J K Rowling"))
    #________________CLIENTS____________________________________________________
    repoClients.add(Client(20, "John Wright"))
    repoClients.add(Client(40, "Andrei Ivan"))
    repoClients.add(Client(35, "Frank Lampard"))
    repoClients.add(Client(78, "Gerard Pique"))
    repoClients.add(Client(24, "Moussa Dembele"))
    repoClients.add(Client(12, "Mohamed Salah"))
    repoClients.add(Client(4, "Virgil Van Dijk"))
    repoClients.add(Client(67, "Frenkie De Jong"))
    repoClients.add(Client(80, "Luuk De Jong"))
    repoClients.add(Client(36, "Joshua Kimmich"))
    #____________________________________________________________________________
    
    """
    repoRental.add(Rental(1, Book(1, "The Secret Crusade", "Oliver Bowden"), Client(20, "John Wright"), datetime.date(2019, 10, 5), None))
    repoRental.add(Rental(2, Book(2, "The Illustrated Man", "Ray Bradbury"), Client(40, "Andrei Ivan"), datetime.date(2019, 10, 7), None))
    
    #repoRental.add(Rental(3, Book(3, "The Glass Castle", "Jeannette Walls"), Client(35, "Frank Lampard"), datetime.date(2019, 10, 15), None))
    repoRental.add(Rental(4, Book(4, "Still Alice", "Lisa Genova"), Client(78, "Gerard Pique"), datetime.date(2019, 11, 1), None))
    repoRental.add(Rental(5, Book(5, "Olive Again", "Elizabeth Strout"), Client(24, "Moussa Dembele"), datetime.date(2019, 11, 7), None))
    repoRental.add(Rental(6, Book(6, "The Nightshift Before Christmas", "Adam Kay"), Client(12, "Mohamed Salah"), datetime.date(2019, 11, 9), None))
    repoRental.add(Rental(7, Book(7, "The Tales of Beedle the Bard", "J K Rowling"), Client(4, "Virgil Van Dijk"), datetime.date(2019, 11, 15), None))
    repoRental.add(Rental(8, Book(8, "This is Going to Hurt", "Adam Kay"), Client(80, "Luuk De Jong"), datetime.date(2019, 11, 17), None))
    """
    c = Console(Srv, validatorInteger, validatorDate)
    c.run()
    