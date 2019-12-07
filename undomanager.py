class UndoOperations:
    def __init__(self, s_obj, h, args):
        self.__source_obj = s_obj
        self.__handler = h
        self.__args = args

    def get_args(self):
        return self.__args

    def get_source_obj(self):
        return self.__source_obj

    def get_handler(self):
        return self.__handler

class UndoManager:
    __undo_operations = [] 
    
    @staticmethod
    def register_operation(s_obj, h, *args):
        UndoManager.__undo_operations.append(UndoOperations(s_obj, h, args))
        #print(len(UndoManager.__undo_operations))

    @staticmethod
    def undo():
        if len(UndoManager.__undo_operations) == 0:
            raise ValueError("Nothing to undo.")
        undo_operation = UndoManager.__undo_operations.pop()
        undo_operation.get_handler()(undo_operation.get_source_obj(), *undo_operation.get_args())
