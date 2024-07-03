import re
import pandas as pd
from .randomize_query import RandomizeQuery
from .read_file import read_file
from .path_manager import PathManager


class FormatQuery:
    def __init__(self) -> None:
        pass
        
    def base_to_historical(self,
                    dates: pd.DatetimeIndex,
                    query: str,
                    columns: list = None,
                    add_date_as_col: bool = True,
                    random_sample: bool = False,
                    sample_size: int | float = 0.2,
                    formats_for_tables: list = "%Y%m",
                    verbose: bool = False, 
                    **kwargs) -> str:
    
        if ".sql" in query:
            query = read_file(file_path=query, **kwargs)

        query_ = re.split('(?i)from', query)

        predefined_columns = len(re.split('(?i)select', query_[0])[-1].strip()) != 0
        add_new_cols = (isinstance(columns, list)) and (len(columns) != 0)

        # Evaluate if the query already has predefined columns
        
        # Format columns
        if predefined_columns and (add_new_cols or add_date_as_col):
            query_[0] = query_[0].strip() + ',\n'

        if add_new_cols:
            if add_date_as_col:
                str_to_add = '\t{},\nFROM'
            else: 
                str_to_add = '\t{}\nFROM'
    
            columns_to_add = [', \n\t'.join([str(col) for col in columns])]
        else:
            str_to_add = 'FROM'
            columns_to_add = []

        query_.insert(1, str_to_add)
        query = ''.join(query_)
           
        # Tables to format
        times_braces = re.split('(?i)from', query)[-1].count('{}')

        # Add date as new col
        query_ = re.split('(?i)from', query)
        if add_date_as_col:
            num_times_date = 1 + times_braces
            query_.insert(1, '\t{} AS FA\nFROM')
            query = ''.join(query_)
        else:
            num_times_date = times_braces

        if verbose:
            print(f"Query to format:\n{query}")

        # One or multiple date for historical data
        if len(dates) == 1:

            # Set date formats
            args = self.__args_for_format_query(dates[0], columns_to_add, formats_for_tables, num_times_date)
            new_query = query.format(*args).strip()

        else:
            queries_by_dates = []
            
            for date in dates:
                
                # Set date formats
                args = self.__args_for_format_query(date, columns_to_add, formats_for_tables, num_times_date)
                queries_by_dates.append(query.format(*args))

            queries_by_dates = [q.strip() for q in queries_by_dates]
            new_query = '\nUNION ALL\n'.join(queries_by_dates).strip('\n')
        
        if random_sample:
            return RandomizeQuery(original_query=new_query, sample_size=sample_size).randomize_samples()
        else:
            return new_query 
        
    def __args_for_format_query(self, date, columns_to_call, formats_for_tables, num_times_date):
        if isinstance(formats_for_tables, str):
            args = columns_to_call + [date.strftime(format=formats_for_tables)]*num_times_date
        elif isinstance(formats_for_tables, list) and len(formats_for_tables) == num_times_date:
            args = columns_to_call + [date.strftime(format=f) for f in formats_for_tables]
        else:
            raise ValueError(f"The number of formats provided is incorrect. Proportion {num_times_date} formats")
        
        return args