import os
import subprocess

MESSAGE_COLOR = "\x1b[34m"
RESET_ALL = "\x1b[0m"

print(f"{MESSAGE_COLOR}Almost done!\n")

# Initializing Git
print(f"Initializing a git repository ...\n{RESET_ALL}")
subprocess.call("git init".split(' '))
subprocess.call("git add *".split(' '))
subprocess.call(["git", "commit", "-m", '"Initial commit"'])
print(f"{MESSAGE_COLOR}\nDone!\n")

# Creating virtual environment using venv
if "{{ cookiecutter.project_env_type }}" == 'venv':
    print(f"{MESSAGE_COLOR}\nCreating virtual environment ...\n")

    subprocess.call("python -m venv .venv".split(' '))
    print(f"{MESSAGE_COLOR}Done!\n{RESET_ALL}")

    print(f"{MESSAGE_COLOR}\nInstalling libraries ...\n")

    python_venv = os.getcwd() + f"{os.sep}.venv{os.sep}Scripts{os.sep}python.exe"
    subprocess.call(f"{python_venv} -m pip install --upgrade pip".split(' '))
    subprocess.call([python_venv, '-m', "pip", "config", "set", "global.trusted-host", '"pypi.org files.pythonhosted.org pypi.python.org"'])
    subprocess.call(f"{python_venv} -m pip install --no-cache-dir -r requirements.txt".split(' '))

    print(f"{MESSAGE_COLOR}\nInstalling TuyaPY ...\n")
    subprocess.call(f"{python_venv} -m pip install //mdentyvrt01/Cuantificacion_de_riesgos/John_Mario_Montoya_Zapata/tuyapy/")

    # print(f"{MESSAGE_COLOR}\nInstalling current project as package ...\n")
    # subprocess.call(f"{python_venv} -m pip install .")

    print(f"{MESSAGE_COLOR}Done!\n{RESET_ALL}")

elif "{{ cookiecutter.project_env_type }}" == 'conda':

    # Creating virtual environment usind conda
    print(f"{MESSAGE_COLOR}\nCreating virtual environment and intalling libraries ...\n")
    subprocess.call("conda env create --file environment.yml".split(' '))
    print(f"{MESSAGE_COLOR}Done!\n{RESET_ALL}")
    
else:
    print(f"{MESSAGE_COLOR}\nA virtual environment has not been created!\n")


