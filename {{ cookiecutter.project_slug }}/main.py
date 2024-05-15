import os
import sys
import pytz
import mlflow
import pickle

import pandas as pd

from datetime import datetime
from dateutil.relativedelta import relativedelta

#--- Time zone for date handling
timezone_colombia = pytz.timezone('America/Bogota')

# Setting variables to model and save predictions
model_id = 'bccd331323ec459bb4eb8937dd9210ba'
dataset = 'db.table'
table_daily = 'daily_prediction_scoring'

def run_daily_prediction(save_to_db: bool = True, **kwargs):
    """
    Run daily predictions for customer defaults within the specified date range.

    Parameters
    ----------
    save_to_db : bool, optional
        If True, save prediction results to a database. Default is True.
    **kwargs : dict
        Additional keyword arguments:
        - start_date : str, optional
            Start date for prediction processing. If provided, it overrides the default start date.
        - end_date : str, optional
            End date for prediction processing. If provided, it overrides the default end date.

    Raises
    ------
    SystemExit
        If the model has already been executed for the specified date 
        range (last_date_model_execution matches current_date_str).

    Notes
    -----
    This function runs daily predictions for customer defaults based on the specified date range. It checks if the model has
    already been executed for the current date and raises a SystemExit exception if so. Otherwise, it iterates over the date
    range and executes predictions for each day within the range, using the `execute_prediction` function.
    """

def run_generate_features_to_train():
    pass

def run_train_model():
    pass

def run_make_backtesting():
    pass

if __name__ == '__main__':

    # Dictionary to select the process(function) to be executed

    process_to_run = {
        "daily_prediction": run_daily_prediction,
        "features_to_train": run_generate_features_to_train,
        "train_model": run_train_model,
        "make_backtesting": run_make_backtesting
    }[sys.argv[1]]

    try:
        kwargs = {value.split('=')[0]:value.split('=')[1] for value in sys.argv[2:]}
    except:
        raise ValueError('A value that does not specify the parameter to configure has been entered. It should have the form key=value')
    
    start_execution = datetime.now(timezone_colombia).strftime('%Y-%m-%d %H:%M:%S')
    print(f'-------- Process started at {start_execution} Colombian time --------\n')

    process_to_run(**kwargs)

    # python main.py daily_prediction start_date=2023-06-01 end_date=2023-06-08