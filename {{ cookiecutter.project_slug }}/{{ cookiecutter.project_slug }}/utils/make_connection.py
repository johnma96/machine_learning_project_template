import pyodbc

class MakeConnection():

    def __init__(self) -> None:
        pass

    def with_impala(self, conn_str: str = "DSN=impala_nube") -> None:
        self.conn = pyodbc.connect(conn_str, autocommit = True)