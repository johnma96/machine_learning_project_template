# Custom project for machine learning and AI projects

Creator: John Mario Montoya Zapata

## Version history:
| User                      | Version | date       |
|---------------------------|---------|------------|
| John Mario Montoya Zapata |  0.1.0  | 2024/05/15 |
|                           |         |            |

## Description
Free project for the generation of a template of projects aimed at the development of machine learning and artificial intelligence models in general. Its objective is to minimize the load during the initial generation of the project and standardize the development of its code. You can consult the structure of the resulting repository [here](/{{%20cookiecutter.project_slug%20}}/README.md)

## Table of contents
1. [Create a new project](#create-a-new-project)
2. [Repository structure](#repository-structure)
3. [Cloning this repository](#cloning-this-repository)
4. [Setting up a virtual environment](#setting-up-a-virtual-environment)

## Create a new project

In the directory where you want to save your generated project.

**Note:** If you want to copy the version to another branch change the branch name **after the checkout parameter**

```bash
cookiecutter https://github.com/johnma96/machine_learning_project_template.git --checkout main
```

## Repository structure.

This project structure was partially influenced by the [Cookiecutter Data Science project](https://drivendata.github.io/cookiecutter-data-science/) and [reproducible-model](https://github.com/cmawer/reproducible-model) repository.

Check this [post](https://www.jeremyjordan.me/ml-projects-guide/) by Jeremy Jordan for get guidelines on managing ML projects.

Other resources.
- Books
    - [Clean Machine Learning Code](https://leanpub.com/cleanmachinelearningcode)

```
├── LICENSE                          <- Apache 2.0 Software License
|
├── README.md                        <- You are here
|
├── docs/                            <- A default Sphinx project; see sphinx-doc.org for details
|
├── {{ cookiecutter.project_slug }}/ <- Source code for use in this project. Here is the structure of 
|                                        folders and files used.
|
├── hooks/                           <- Hooks for executing .py or .sh code both at the beginning and at 
|                                        the end of using the template
|
├── environment.yml                  <- The environment file for reproducing the environment, e.g.
│                                        generated with `conda env export --from-history --file environment.yml`
|
├── requirements.txt                 <- The requirements file for reproducing the environment, e.g.
│                                        generated with `pip-chill > requirements.txt`
|
├── .gitignore                       <- Gitignore file 
|
└──cookicutter.json                  <- Initial configuration on which the template is generated
```

## Cloning this repository.

- To clone this repository using SSH run the next command in your git console
```bash
git clone git@github.com:johnma96/machine_learning_template.git
```
- To clone this repository using HTTPS run the next command in your git console
```bash
git clone https://github.com/johnma96/machine_learning_template.git
```

For more details see [Clone a repository](https://docs.gitlab.com/ee/gitlab-basics/start-using-git.html#clone-a-repository).

## Setting up a virtual environment.

In order to not create conflics between your libraries and the requirements libraries for this project, we highly recomend you to create a new virtual environment to install the requirements libraries in there.

**Check out the installation guide [here](/install.md)**

For more details consult:
- Click [here](https://docs.python.org/3/library/venv.html) to see how to create a virtual environment in python.
- Click [here](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) if you are using conda.

### Installing and updating project libraries.
The required libraries are listed in the file [`requirements.txt`](/requirements.txt) or [`environment.yml`](/environment.yml). **Please read [the installation guide](/install.md) information for greater detail.**
