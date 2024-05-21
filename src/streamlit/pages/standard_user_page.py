import streamlit as st
import requests
from streamlit_library import prepare_jsonl, predict

# -------------- Variables declaration: ---------------------------------------
localhost = "127.0.0.1"
user_payload = st.session_state['id']

# --------------- Page --------------------------------------------------------
st.title("SHIELD")
st.write("Bienvenue sur le portail SHIELD standard")

# ----- Predict from test:
test = st.container(border=True)
if test.button("Effectuer une prédiction à partir de l'ensemble de test:"):
    response = requests.get(url=f"http://{localhost}:8000/predict_from_test",
                            headers=user_payload)
    test.write(response.json())

# ----- Predict from call:
pred = st.container(border=True)
if pred.button("Effectuer une prédiction à partir d'un appel:"):
    # response = requests.get(url=f"http://{localhost}:8000/predict_from_test",
    # headers=user_payload)
    # call.write(response.json())
    predict.call()

# ----- Get jsonl:
data = st.container(border=True)
option = data.selectbox(
    "Quel type d'information souhaitez-vous?",
    ("f1_score", "preds_call", "preds_labelled",
     "preds_test", "train", "update_data"))
log_data = {"name": option}

if data.button("Visualiser les logs"):
    response = requests.post(url=f"http://{localhost}:8000/get_logs",
                             json=log_data,
                             headers=user_payload)
    data_jsonl = response.json()
    df = prepare_jsonl.jsonl_to_df(data_jsonl)
    data.dataframe(df)


# ----- Get id
if st.button("Afficher l'identifiant"):
    st.write(st.session_state['id'])
