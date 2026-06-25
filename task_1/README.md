# Task 1: GitHub, Virtual Environment, and Linux Basics
*brief description*
Task 1 involves familiarisation with git and linux basics. This folder demonstrates setting up a python project with a virtual environment, documenting linux commands and running a basic python script.

# Setup instructions
    1. create the Synergy_TP repo and clone it within your IDE using git clone.
       you may get a "cloned empty repository" warning but continue.
    2. change your current working directory to Synergy_TP.
    3. create and activate your virtual environment .
    4. create the .md and .txt files specified in problem statement.
    5. install required packages and generate the requirements.txt file.
    6. run the python script.
    7. push on github.

# Steps to create and activate the virtual environment 
    1.  To create a virtual environment, run the following instruction on git bash:
        python -m  venv venv
        now you will see a venv directory inside your project folder.
    2. To activate it, find the path to "activate" inside your venv which is mostly-->venv/Scripts/activate,
       once found run the following command:
        source venv/Scripts/activate

# Steps to install requirements
    1. Use the standardised package manager "pip" to install required pacakages, using the following command:
        pip install your package(Numpy in this case)
    2. After successful installation freeze all package dependencies to the "requirements.txt" file using:
        pip freeze > task_1/requirements.txt

# Command to run the Python file from Synergy_TP root 
    From the directory structure given in the problem statement we can see that the path to the python file from the root is:
    task_1/src/hello.py
    Therefore the command to run it would be:
        python task_1/src/hello.py
    Expected output::
        Hello, World!




