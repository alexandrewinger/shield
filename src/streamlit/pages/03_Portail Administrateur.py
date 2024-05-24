import streamlit as st
import requests
import os
from pathlib import Path
import sys

# internal
root_path = Path(os.path.realpath(__file__)).parents[3]
sys.path.append(os.path.join(root_path, "src", "streamlit"))
from streamlit_library import prepare_jsonl # noqa E402

# -------------- Variables declaration: ---------------------------------------
localhost = "127.0.0.1"
# user_payload = st.session_state['id']
header_admin = {"identification": "admin:4dmin"}
header_user = {"identification": "fdo:c0ps"}

# --------------- Page --------------------------------------------------------
st.title("SHIELD")
st.write("Bienvenue sur le portail SHIELD admin")

# ----- Predict from test:
if st.button("Effectuer une prédiction à partir de l'ensemble de test:"):
    response = requests.get(url=f"http://{localhost}:8000/predict_from_test",
                            headers=header_admin)
    st.write(response.json())

# ----- Get jsonl:
data = st.container(border=True)
option = data.selectbox(
    "Quel type d'information souhaitez-vous?",
    ("f1_score", "preds_call", "preds_labeled",
     "preds_test", "train", "update_data"))
log_data = {"name": option}

if data.button("Visualiser les logs"):
    response = requests.post(url=f"http://{localhost}:8000/get_logs",
                             json=log_data,
                             headers=header_admin)
    data_jsonl = response.json()
    df = prepare_jsonl.jsonl_to_df(data_jsonl)
    data.dataframe(df)

# ----- Get id
# if st.button("Afficher l'identifiant"):
#     st.write(st.session_state['id'])
