
class RedoOperations:
    def __init__(self, s_obj, h, args):
        self.__source_obj = s_obj
        self.__handler = h
        self.__args = args

    def get_source_obj(self):
        return self.__source_obj

    def get_args(self):
        return self.__args

    def get_handler(self):
        return self.__handler


class RedoManager:
    __redo_operations = []

    @staticmethod
    def register_operation(s_obj, h, *args):
        RedoManager.__redo_operations.append(RedoOperations(s_obj, h, args))

    @staticmethod
    def redo():
        if len(RedoManager.__redo_operations) == 0:
            raise ValueError("Nothing to redo.")
        redo_operation = RedoManager.__redo_operations.pop()
        redo_operation.get_handler()(redo_operation.get_source_obj(), *redo_operation.get_args())

    @staticmethod
    def delete():
        __redo_operations = []
