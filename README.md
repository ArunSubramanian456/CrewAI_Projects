# CrewAI Projects

This repository will contain several independent Crew AI projects, each located in its own subfolder. As I add more projects exploring more tools & workflows, I plan to continuously update this repo.


## Project Structure

*   `subfolder1/`: Description of project 1
    *   `requirements.txt`: Project 2 dependencies
    *   `.env`: Environment variables

*   `subfolder2/`: Description of project 2
    *   `requirements.txt`: Project 2 dependencies
    *   `.env`: Environment variables


## Setup

Within the parent folder :
1. Create a virtual environment: `conda create -p my_venv python==3.12 -y` if you have Anaconda or `python -m venv my_venv` on Windows w/o Anaconda
2. Add a `.gitignore` file and update it with relevant exclusions

For each subproject:

1.  Navigate to the subfolder: `cd subfolder1`
2.  Activate the environment: `conda activate <path>\my_venv` if you have Anaconda or `<path>\my_venv\Scripts\activate`  on Windows w/o Anaconda
3.  Install dependencies: `pip install -r requirements.txt`
4.  Create a `.env` file to store the api keys and fill in the appropriate values.
