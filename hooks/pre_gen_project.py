import json
import os
import pytz
from datetime import datetime
import unicodedata

ERROR_COLOR = "\x1b[31m"
MESSAGE_COLOR = "\x1b[34m"
RESET_ALL = "\x1b[0m"

# with open('../cookiecutter.json', 'r') as json_file:
#     cookicutter_config = json.load(json_file)

# project_slug = "".join(c for c in unicodedata.normalize("NFD", cookicutter_config['project_slug']).lower().replace(" ", "_") if unicodedata.category(c) != "Mn")
# cookicutter_config['project_slug'] = project_slug

# if cookicutter_config["project_start_date"] == "Current date (YYYY-mm-dd)":
#     timezone_colombia = pytz.timezone('America/Bogota')
#     current_date = datetime.now(timezone_colombia).strftime('%Y-%m-%d')    
#     cookicutter_config['project_start_date'] = current_date

# with open('temporal.json', 'w') as json_file:
#     json.dump(cookicutter_config, json_file, indent=4)