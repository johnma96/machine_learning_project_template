import os
from .path_manager import PathManager

def read_file(file_path: str, **kwargs) -> str:
    if 'encoding' not in kwargs: kwargs['encoding'] = 'utf-8'

    if os.sep not in file_path:
        file_path = PathManager().get_abs_path_file(file_path)
        
    with open(file_path, 'r', **kwargs) as f:
        return f.read()