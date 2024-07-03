import warnings
import pandas as pd

from .make_connection import MakeConnection
from .read_file import read_file

class ReadData(MakeConnection):

    def __init__(self, type_rdbms: str = 'impala', **kwargs) -> None:
        super().__init__()

        # Connections to databases
        if type_rdbms is not None:

            # Local connection to Impala
            if type_rdbms == "impala":
                try:
                    if kwargs.get('conn_str') is not None:
                        self.with_impala(conn_str=kwargs.get('conn_str'))
                    else:
                        self.with_impala()                
                except Exception as e:
                    warnings.warn(f"Error connecting to Impala: {e}")

        # Read local files
        else:
            pass
            
    def from_impala(self, query: str, verbose: bool = True, **kwargs):

        if ".sql" in query:
            query = read_file(file_path=query)

        if verbose:
            print(query)

        data = pd.read_sql(sql=query, con=self.conn, **kwargs)
        self.conn.close()
        return data