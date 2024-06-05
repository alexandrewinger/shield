# 🛡️ Project Name: SHIELD

**SHIELD** (Safety Hazard Identification and Emergency Law Deployment) is an app that uses machine learning to predict the priority of a road accident based upon 28 caracteristics received by a police administrator during a call. Its purpose is to help prioritize interventions to gain in efficiency.

## Project Team:
SHIELD was first developped in its early stages by the team:

- Fabrice **Charraud** ([@FCharraud](https://github.com/FCharraud))
- Omar **Choa** ([@omarchoa](https://github.com/omarchoa))
- Michael **Deroche** ([@miklderoche](https://github.com/miklderoche))
- Alexandre **Winger** ([@alexandrewinger](https://github.com/alexandrewinger))

Now, it is only developped by **Alexandre WINGER**.

## Setup

### 1- First, you'll have to clone the repo:

    `git clone https://github.com/alexandrewinger/shield.git`

### 2- Let's change our current repository:
    `cd shield`

### 3- Launch the app:
    `docker-compose up`

### 4- The streamlit app should be ready for you to test in your favorite browser:
    `http://127.0.0.1:8501`

## Project Organization
------------

    ├── LICENSE
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── logs               <- Logs from training and predicting
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── api            <- Scripts concerning the api  
    │   │
    │   ├── cron-monitor   <- Files for monitoring via cronjob
    │   │
    │   ├── data           <- Scripts to download and preprocess data
    │   │
    │   ├── docker         <- Scripts to manage docker
    │   │
    │   ├── models         <- Files for training model
    │   │
    │   ├── monitoring     <- Files for monitoring
    │   │   
    │   ├── streamlit      <- Files for streamlit
    │   │  
    │   ├── test           <- Files for testing
    │   │  
    │   └── users_db       <- Files for managing users database

---------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
