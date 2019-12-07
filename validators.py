import datetime
from exceptions import NumericalError, RepositoryError, ValidationError

class ValidateBook(object):
    
    def __init__(self):
        pass
    
    def validate_book(self, book):
        #validates a book
        #a book is not valid if its id is a negative integer, if its title is an empty string or if its author its an empty string
        #raises a ValidationError if the book is not valid
        errors = ""
        if book.bookID < 0:
            errors += " Invalid book ID!"
        if book.bookTitle == "":
            errors += " Invalid book title!"
        if book.bookAuthor == "":
            errors += " Invalid book Author!"
        if len(errors) > 0:
            raise ValidationError(errors)
        

class ValidateClient(object):
    
    def __init__(self):
        pass
        
    def validate_client(self, client):
        #validates a client
        #a client is not valid if its id is a negative integer or if its name is an empty string
        #raises a ValidationError if the client is not valid
        errors = ""
        if client.clientID < 0:
            errors += " Invalid client ID!"
        if client.clientName == "":
            errors += " Invalid client name!"
        if len(errors) > 0:
            raise ValidationError(errors)
    
class ValidateRental(object):
    
    def __init__(self):
        pass
        
    def validate_rental(self, rent):
        #validates a rent
        #raises a ValidationError if the client is not valid
        errors = ""
        
        if int(rent.rentalID) < 0:
            errors += " Invalid Rental ID!"
        
        if rent.returnedDate is not None:
            if rent.returnedDate < rent.rentedDate:
                errors += " Invalid returned Date!"
        
        if len(errors) > 0:
            raise ValidationError(errors)
        
        
        
class ValidateInteger(object):
    
    def __init__(self):
        pass
    
    def validate_integer(self, x):
        #checks if a given variable is an integer
        #x = (str) the variable
        #raises a NumericalError exception if not
        try:
            x = int(x)
        except:
            raise NumericalError(str(x) + " is not an integer.")

class ValidateDate(object):
    
    def __init__(self):
        pass
    
    def validate_date(self, day, month, year):
        #checks if a given set of variable could form a date
        #day = (int) the day
        #month = (int) the month
        #year = (int) the year
        #raises a NumericalError exception if not
        x = 0
        try:
            x = datetime.date(year, month, day)
        except:
            raise NumericalError(str(day) + "|" + str(month) + "|" + str(year) + " is not a valid date.")