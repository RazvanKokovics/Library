
class CommandError(Exception):
    #Raised when a command is not in commands
    def __init__(self, error):
        self._err = str(error)
    
    def __str__(self):
        return str("\n[COMMAND ERROR] -> " + self._err)

class NumericalError(Exception):
    #Raised when the data type of te user does not match
    def __init__(self, error):
        self._err = str(error)
    
    def __str__(self):
        return str("\n[NUMERICAL ERROR] -> " + self._err)
 
class RepositoryError(Exception):
    #Raised when the id of the object is not valid
    def __init__(self, error):
        self._err = str(error)
    
    def __str__(self):
        return str("\n[REPOSITORY ERROR] -> " + self._err)
    
class ValidationError(Exception):
    #Raised when a string is empty
    def __init__(self, error):
        self._err = str(error)
    
    def __str__(self):
        return str("\n[VALIDATION ERROR] ->" + self._err)