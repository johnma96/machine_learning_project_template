class DropTableException(Exception):
    def __init__(self, message="DROP cannot be executed without a WHERE clause"):
        super().__init__(message)

class TableNotExistsError(Exception):
    def __init__(self, table, message="The {} table does not exist"):
        super().__init__(message.format(table))

class DuplicatedColumnsError(Exception):
    """Raised when exists duplicates in column names of a DataFrame.
    """
    pass

class TableInconsistencyError(Exception):
    """Raised when a table does not exist.
    """
    pass

class SQLDataTypeError(Exception):
    """Raised when a data type is not correct.
    """
    pass