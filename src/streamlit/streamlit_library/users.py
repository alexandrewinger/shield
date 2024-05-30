import json
import streamlit as st
import requests
import os
import pandas as pd
from pathlib import Path
import sys

root_path = Path(os.path.realpath(__file__)).parents[3]


def add_user():
    # -------------- Variables declaration: -----------------------------------
    localhost = "api" if os.environ.get('ENVIRONMENT') == 'docker' else "127.0.0.1" # noqa E501
    header_admin = {"identification": "admin:4dmin"}

    st.title(body="Ajouter un utilisateur:")

    # Other inputs ------------------------------------------------------------
    username = st.text_input("Nom d'utilisateur:")
    password = st.text_input("Mot de passe:")
    access = st.selectbox("Choisir les droits associés à l'utilisateur:",
                          ("Droits standards",
                           "Droits administrateur"))

    rights = 0 if access == "Droits standards" else 1
    new_user = {
        "username": username,
        "password": password,
        "rights": rights
    }
    if st.button("Valider le nouvel utilisateur"):
        response = requests.post(url=f"http://{localhost}:8000/add_user",
                                 json=new_user,
                                 headers=header_admin)
        st.write(response.json()[0])


def remove_user():
    # -------------- Variables declaration: -----------------------------------
    localhost = "api" if os.environ.get('ENVIRONMENT') == 'docker' else "127.0.0.1" # noqa E501
    header_admin = {"identification": "admin:4dmin"}

    st.title(body="Supprimer un utilisateur:")

    # Other inputs ------------------------------------------------------------
    response = requests.get(url=f"http://{localhost}:8000/get_users",
                            headers=header_admin)

    users_list = response.json().keys()

    user = st.selectbox(
        "Quel utilisateur voulez-vous supprimer?",
        users_list
    )

    # user = st.text_input("Quel utilisateur voulez-vous supprimer?")

    old_user = {"user": user}

    if st.button("Valider la suppression"):
        response = requests.delete(url=f"http://{localhost}:8000/remove_user",
                                   json=old_user,
                                   headers=header_admin)
        st.write(response.json()[0])


def get_all_users():
    # -------------- Variables declaration: -----------------------------------
    localhost = "api" if os.environ.get('ENVIRONMENT') == 'docker' else "127.0.0.1" # noqa E501
    header_admin = {"identification": "admin:4dmin"}

    # internal
    root_path = Path(os.path.realpath(__file__)).parents[3]
    sys.path.append(os.path.join(root_path, "src", "streamlit"))
    from streamlit_library import prepare_jsonl # noqa E402

    st.title(body="Obtenir tous les utilisateurs:")

    # -------------- Main code ------------------------------------------------
    response = requests.get(url=f"http://{localhost}:8000/get_users",
                            headers=header_admin)
    users_db = list(response.json().values())

    with open('users.jsonl', 'w') as file:
        for data in users_db:
            # Convert data in json string and save it inside file:
            file.write(json.dumps(data) + '\n')

    df = pd.read_json('users.jsonl', lines=True)
    st.dataframe(df)
