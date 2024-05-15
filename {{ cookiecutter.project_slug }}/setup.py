from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().splitlines()

setup(
    name="{{ cookiecutter.project_slug }}",
    version="{{ cookiecutter.project_initial_version }}",
    author="{{ cookiecutter.project_author_name }}",
    author_email="{{ cookiecutter.project_author_email }}",
    description="{{ cookiecutter.project_short_description }}",
    long_description="{{ cookiecutter.project_long_description }}",
    url="{{ cookiecutter.project_remote_repository }}",
    packages=find_packages(),
    install_requires=install_requires
)
