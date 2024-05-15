#!/bin/bash
cd /path_to_project/{{ cookiecutter.project_slug }}/
source .venv/bin/activate
python3 main.py daily_prediction