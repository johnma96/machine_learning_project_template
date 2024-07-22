from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().splitlines()

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name="{{ cookiecutter.project_slug }}",
    version="{{ cookiecutter.project_initial_version }}",
    description="{{ cookiecutter.project_short_description }}",
    package_dir={"":"{{ cookiecutter.project_slug }}"},
    author="{{ cookiecutter.project_author_name }}",
    author_email="{{ cookiecutter.project_author_email }}",
    long_description=long_description,
    url="{{ cookiecutter.project_remote_repository }}",
    packages=find_packages(where="{{ cookiecutter.project_slug }}"),
    python_requires=">={{ cookiecutter.python_version }}",
    install_requires=install_requires, 
    extras_require={
        "dev": [
                "wheel==0.43.0",
                "notebook==7.2.1"
                ]
    },
)
