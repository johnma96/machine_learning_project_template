import warnings
from typing import List
from pyodbc import Row
import pandas as pd
import numpy as np
import inspect
import os
import time
from .path_manager import PathManager
from .read_file import read_file
from .make_connection import MakeConnection
from .exceptions import *

class ExecuteQuery(MakeConnection):

    def __init__(self, type_rdbms: str = 'impala', execute: bool = True, **kwargs) -> None:
        super().__init__()
        self.execute = execute

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

            # Add another kind of connection to Data Bases

        # Read local files
        else:
            pass

    def run_sql_query(self, query: str, verbose = True) -> None:

        if ".sql" in query:
            query = read_file(file_path=query)

        if verbose:
            print(query)

        cursor = self.conn.cursor()

        if self.execute:
            cursor.execute(query)
            cursor.close()
            if verbose:
                print("Query executed successfully!")
        else:
            print("Query was not executed!")
    
    def run_sql_query_and_fetch(self, query: str) -> List[Row]:
        cursor = self.conn.cursor()
        if self.execute:
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            return results 
        else:
            print("Query was not executed!")
    
    def run_sql_query_fetch_value(self, sql: str) -> int:
        
        cursor = self.conn.cursor()
        if self.execute:
            cursor.execute(sql)
            result = cursor.fetchval()
            cursor.close()
            return result
        else:
            print("Query was not executed!")
    
    def create_table_as(self, 
                        table_name: str, 
                        as_query: str, 
                        drop_table: bool = False,
                        drop_just_metadata: bool = True,
                        external_table: bool = True, 
                        partitoned: bool = False, 
                        columns_to_partition: list = None, 
                        verbose: bool = True):
        
        if columns_to_partition is None: columns_to_partition = []
        
        queries = []

        if (drop_table) and (not drop_just_metadata):
                self.__make_truncate_query(table_name)
                queries.append(self.truncate_query)

        if drop_table:
            self.__make_drop_query(table_name)
            queries.append(self.drop_query)

        if ".sql" in as_query:
            as_query = read_file(as_query)

        self.__make_create_as_query(table_name, as_query, external_table, 
                                    partitoned, columns_to_partition)
        self.__make_compute_stats_query(table_name, partitoned)

        queries.append(self.create_as_query)
        queries.append(self.compute_stats_query)

        self.create_table_as_query = '\n'.join(queries)

        if verbose:
            print(self.create_table_as_query)
        
        for q in queries:
            self.run_sql_query(query=q, verbose=False)

        if verbose and self.execute:
            print("\nTable created successfully")
    
    def create_empty_table(self, 
                        table_name: str,
                        columns: list,
                        types_columns: list = ["STRING"], 
                        drop_table: bool = False,
                        drop_just_metadata: bool = True,
                        external_table: bool = True, 
                        partitioned: bool = False, 
                        columns_to_partition: list = None, 
                        verbose: bool = True):
    
        if columns_to_partition is None: 
            columns_to_partition = []

        queries = []

        if (drop_table) and (not drop_just_metadata):
                self.__make_truncate_query(table_name)
                queries.append(self.truncate_query)

        if drop_table:
            self.__make_drop_query(table_name)
            queries.append(self.drop_query)

        self.__make_create_empty_query(table_name=table_name,
                                       columns=columns,
                                       external_table=external_table, columns_to_partition=columns_to_partition,
                                       types_columns=types_columns, partitoned=partitioned)

        queries.append(self.create_empty_query)

        self.create_empty_table_query = '\n'.join(queries)
        
        for q in queries:
            if verbose:
                print(q)
            if self.execute:
                self.run_sql_query(query=q, verbose=False)

        if verbose and self.execute:
            print("\nTable created successfully")

    def create_table_insert(self, 
                        table_name: str,
                        columns: list,
                        into: bool = True,
                        insert_query: str = None,
                        values: list = None,
                        type_insert: str = 'by_query',
                        types_columns: list = ["STR"], 
                        drop_table: bool = False,
                        drop_just_metadata: bool = True,
                        external_table: bool = True, 
                        partitioned: bool = False, 
                        columns_to_partition: list = [], 
                        partition_values: list = [], 
                        verbose: bool = True):
        
        
        original_params = locals()
        
        dict_create_empty_table = {k: v for k, v in original_params.items() if k in inspect.signature(self.create_empty_table).parameters}
        dict_insert = {k: v for k, v in original_params.items() if k in inspect.signature(self.insert_values).parameters}

        self.create_empty_table(**dict_create_empty_table)
        self.insert_values(**dict_insert)


    def insert_values(self, 
                    type_insert: str, 
                    table_name: str,
                    into: bool, 
                    insert_query: str = None,
                    values: list = None, 
                    partitioned: bool = False,
                    columns_to_partition: list = [], 
                    partition_values: list = [],
                    verbose: bool = True): 
        
        if '.sql' in insert_query:
            insert_query = read_file(insert_query)
        
        original_params = locals()

        if insert_query is None:
            original_params.pop('insert_query')

        if values is None:
            original_params.pop('values')

        dict_insert = {k: v for k, v in original_params.items() if k in inspect.signature(self.__make_insert_query).parameters}

        self.__make_insert_query(**dict_insert)
        self.__make_compute_stats_query(table_name=table_name, partitoned=partitioned)

        if verbose:
            print(self.insert_query)
            print(self.compute_stats_query)

        if self.execute:
            self.run_sql_query(query=self.insert_query, verbose=False)
            self.run_sql_query(query=self.compute_stats_query, verbose=False)

            if verbose:
                print("Values inserted successfully")
            

    
    def drop_table(self, 
                   query: str = None, 
                   table_name: str = None, 
                   external_table: bool = True, 
                   just_metada: bool = True,  
                   verbose: bool = True) -> None:
        
        if query is not None:
            self.drop_query = query
        else:
            self.__make_drop_query(table_name, external_table, just_metada)
            
            if not just_metada:
                self.__make_truncate_query(table_name)
                self.run_sql_query(query=self.truncate_query, verbose=verbose)

        self.run_sql_query(query=self.drop_query, verbose=verbose)

    def insert_records(self, table_name: str, data: str | pd.DataFrame, batch_size: int = 10000, sep: str = ','):
    #     # Verificar si la tabla existe
    #     try:
    #         results = self.run_sql_query_and_fetch(f"DESCRIBE {table_name}")
    #     except:
    #         raise TableNotExistsError(table=table_name)
    #     # Determinar si la tabla es o no externa


    #     # Obtener los nombres
    #     cols = [row[0] for row in results]

    #     # Obtener los tipos de los campos
    #     cols_types = [row[1] for row in results]

    #     # Cargar datos si data es un string(path)
    #     if isinstance(data, str):
    #         if os.sep in data:
    #             path = data
    #         else:
    #             path = PathManager().get_abs_path_file(data) 
    #         df = pd.read_csv(path, sep)
    #     elif isinstance(data, pd.DataFrame):
    #         df = data
    #         print(f"\nLoading data into the table {table_name} ...")
    #     else:
    #         raise ValueError("You must pass the name of a file, the full path or a pandas dataframe object")
    #     # Verificar si los nombres de las columnas coinciden
    #     #   Si no coinciden lanzar error por nombres de columnas
    #     # Verificar si los tipos de datos coinciden
    #     #   Si no coinciden tratar de llevar los datos a los tipos de la tabla
    #     #   Si no funciona lanzar error por tipo de datos
    #     # Comenzar carga en lotes
    #     insert_query = self.__make_insert_query(table_name=table_name, columns=df.columns.to_list())
    #     start_time = time.time()
    #     self.__execute_many_batches(sql=insert_query, df=df, batch_size=batch_size)
    #     end_time = time.time()
    #     elapsed_time = end_time - start_time
    #     print(f"\n\nTiempo tomado para llevar {df.shape[0]} registros a bodega fue: {elapsed_time/60:.2f} minutos")
    #     time.sleep(2)
        pass

    def __execute_many_batches(self, sql: str, df: pd.DataFrame, batch_size: int = 10000) -> None:
        """Inserta valores en tabla SQL en datalake en batch a partir de un dataframe.
        Utiliza conexión ODBC vía pyodbc.

        Args:
            sql: Query SQL tipo INSERT INTO con parameter markers tipo ?.
            df: DataFrame de Pandas.
            batch_size: Tamaño del batch. Por defecto 10000.
        """

        # se realiza split en n batches de size 10000
        
        if int(batch_size) >= len(df):
            print(f"Specified number of batches {batch_size} is greater than the number of records, a single batch of {len(df)} will be made")
            batches = [df]
            batch_size = len(df)
        else:
            batch_size = int(batch_size)
            batches = np.array_split(df, len(df)//batch_size)

        records = 0
        print(f"\nThere will be shipments of {len(batches)} lots of size {len(batches[0])} ...\n")

        cursor = self.conn.cursor()
        cursor.fast_executemany = True
        for batch in batches:
            values = batch.values.tolist()
            cursor.executemany(sql, values)
            records += len(batch)
            print(f"{records} records loaded of {df.shape[0]} ...", end="\r")

        cursor.close()

    def __make_create_empty_query(self, 
                                    table_name: str,
                                    columns: list,
                                    external_table: bool = True, 
                                    columns_to_partition: list = None, 
                                    types_columns: list = ['STRING'],
                                    partitoned: bool = False):
        

        if len(columns) == 0:
            raise ValueError("Add table's columns")
        
        if len(columns) != len(types_columns):
            print('The number of columns does not match the number of types provided. All columns will be of type STR by default')
            types_columns = ['STRING']*len(columns)

        if columns_to_partition is None:
            columns_to_partition = []

        columns = [col.lower() for col in columns]

        dict_cols_types = {col: type_ for col, type_ in zip(columns, types_columns)}

        if partitoned is True and len(columns_to_partition) != 0:
            dict_partitions = {key: val for key, val in dict_cols_types.items() if key in columns_to_partition}
            [dict_cols_types.pop(k) for k in columns_to_partition]

        cols_types = [f"{col} {type_}" for col, type_ in dict_cols_types.items()]

        base = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(cols_types)}) STORED AS PARQUET;"

        if external_table: 
            base = base.replace('TABLE', 'EXTERNAL TABLE')

        if partitoned is True and len(columns_to_partition) != 0:
            base_ = base.split('STORED')
            cols_types_partition = [f"{col} {type_}" for col, type_ in dict_partitions.items()]
            base_.insert(1, f"PARTITIONED BY ({', '.join(cols_types_partition)}) STORED")
            base = ''.join(base_)

        self.create_empty_query = base.strip()
            
    def __make_insert_query(self, 
                            type_insert: str, 
                            table_name: str,
                            into: bool,
                            insert_query: str = None,
                            values: list = None, 
                            partitioned: bool = False,
                            columns_to_partition: list = [], 
                            partition_values: list = []):
            
            if into:
                base = f"INSERT INTO {table_name}"
            else:
                base = f"INSERT OVERWRITE {table_name}"

            if type_insert == "by_values": 
                pass

            elif type_insert == "by_query":

                columns_to_partition = [col.lower() for col in columns_to_partition]

                if (partitioned is True) and len(columns_to_partition) != 0:
                    if len(partition_values) == 0:
                        base = base + f" PARTITION ({', '.join(columns_to_partition)})"
                    else:
                        partitions = ', '.join([f"{i} = {j}" for z, (i, j) in enumerate(zip(columns_to_partition, partition_values))])
                        base = base + f" PARTITION ({partitions})"

                base = base.strip() + f"\n{insert_query.strip()}"

            else:
                raise ValueError("This insert type doesn't exits")
            
            base = base + ';'
            self.insert_query = base.strip()


    def __make_insertvalues_query(self, table_name: str, columns: List[str]) -> None:
        # insert_query = f"INSERT INTO {table_name} ("
        # values = "VALUES ("

        # for i in range(len(columns)):
        #     # If it is not the last column it is added to the string sequence
        #     if i != max(range(len(columns))):            
        #         values = values + "?, "
        #         insert_query = insert_query + f"{columns[i]}, "
        #     # If it is the last column, it is added to the string sequence and the SQL statement 
        #     # is closed according to the type of statement (INSERT)
        #     else:
        #         values = values + "?)"
        #         insert_query = insert_query + f"{columns[i]}) " + values

        # self.insert_query = insert_query.strip()
        pass

    def __make_truncate_query(self, table_name: str) -> None:
        self.truncate_query = f"TRUNCATE TABLE IF EXISTS {table_name};".strip()

    def __make_drop_query(self, table_name: str) -> None:
        self.drop_query = f"DROP TABLE IF EXISTS {table_name};".strip()

    def __make_create_as_query(self, 
                            table_name: str, 
                            as_query: str, 
                            external_table: bool = True, 
                            partitoned: bool = False, 
                            columns_to_partition: list = None) -> None:
        
        columns_to_partition = [col.lower() for col in columns_to_partition]

        base = f"CREATE TABLE IF NOT EXISTS {table_name} STORED AS PARQUET AS\n{as_query};"

        if external_table: 
            base = base.replace('TABLE', 'EXTERNAL TABLE')

        if partitoned is True and len(columns_to_partition) != 0:
            base_ = base.split('STORED')
            base_.insert(1, f"PARTITIONED BY ({', '.join(columns_to_partition)}) STORED")
            base = ''.join(base_)

        self.create_as_query = base.strip()

    def __make_compute_stats_query(self, table_name: str, partitoned: bool = False) -> None:
        if partitoned:
            self.compute_stats_query = f"COMPUTE INCREMENTAL STATS {table_name};".strip()
        else:
            self.compute_stats_query = f"COMPUTE STATS {table_name};".strip()