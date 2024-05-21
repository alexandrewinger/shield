import streamlit as st
import requests

localhost = "127.0.0.1"
user_payload = st.session_state['id']

st.title("SHIELD")
st.write("Bienvenue sur le portail SHIELD admin")

if st.button("Effectuer une prédiction à partir de l'ensemble de test:"):
    response = requests.get(url=f"http://{localhost}:8000/predict_from_test",
                            headers=user_payload)
    st.write(response.json())


option = st.selectbox(
    "Quel type d'information souhaitez-vous?",
    ("f1_score", "preds_call", "preds_labelled", "preds_test", "train", "update_data"))
log_data = {"name": option}

if st.button("Visualiser les logs"):
    response = requests.get(url=f"http://{localhost}:8000/get_logs",
                            json=log_data,
                            headers=user_payload)
    st.write(response.json())


if st.button("Afficher l'identifiant"):
    st.write(st.session_state['id'])