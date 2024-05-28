import streamlit as st
import requests
import os
from pathlib import Path
# import plotly.figure_factory as ff
import plotly.express as px
import sys

# internal
root_path = Path(os.path.realpath(__file__)).parents[3]
sys.path.append(os.path.join(root_path, "src", "streamlit"))
from streamlit_library import prepare_jsonl # noqa E402
from streamlit_library import users # noqa E402

# -------------- Variables declaration: ---------------------------------------
localhost = "api" if os.environ.get('ENVIRONMENT') == 'docker' else "127.0.0.1" # noqa E501
# user_payload = st.session_state['id']
header_admin = {"identification": "admin:4dmin"}
header_user = {"identification": "fdo:c0ps"}

# --------------- Page --------------------------------------------------------
st.set_page_config(layout="wide")
st.title("SHIELD")
st.write("Bienvenue sur le portail SHIELD admin")
tab0, tab1, tab2, tab3 = st.tabs(["Dbug", "Users", "Model demo", "Monitoring"])

with tab0:
    # ----- Get jsonl:
    data = st.container(border=True)
    option = data.selectbox(
        "Quel type d'information souhaitez-vous?",
        ("f1_scores", "preds_call", "preds_labeled",
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

# --------------- Users management --------------------------------------------
with tab1:
    # ----- Add user:
    users.add_user()

    # ----- Remove user:
    users.remove_user()

    # ----- Get all users:
    users.get_all_users()

# --------------- Model demo --------------------------------------------------
with tab2:
    viz, ctrl = st.columns(2)

    # ---------- Control panel:
    ctrl.write("")
    ctrl.markdown("#### Panneau de commandes")
    # ----- Get f1_score:
    if ctrl.button("Obtenir le f1_score actuel"):
        response = requests.get(
            url=f"http://{localhost}:8000/get_f1_score",
            headers=header_admin)
        f1_score = response.json()
        ctrl.write(f1_score[0])

    # ----- Predict from test:
    if ctrl.button("Effectuer une prédiction à partir de l'ensemble de test"):
        response = requests.get(
            url=f"http://{localhost}:8000/predict_from_test",
            headers=header_admin)
        ctrl.write(response.json())

    # ----- Label preds test:
    if ctrl.button("Labelliser les prédictions faites à partir de l'ensemble de test"): # noqa E501
        response = requests.get(
            url=f"http://{localhost}:8000/label_pred_test",
            headers=header_admin)
        ctrl.write(response.json()[0])

    # ----- Update f1_score:
    if ctrl.button("Mettre le f1_score à jour"):
        response = requests.get(
            url=f"http://{localhost}:8000/update_f1_score",
            headers=header_admin)
        ctrl.write(response.json())

    # ---------- Vizualisation panel:
    # ----- Display graph f1_scores:
    log_data = {"name": "f1_scores"}
    response = requests.post(url=f"http://{localhost}:8000/get_logs",
                                 json=log_data,
                                 headers=header_admin)
    data_jsonl = response.json()
    df = prepare_jsonl.jsonl_to_df(data_jsonl)

    fig = px.line(df, y="f1_score_macro_average",
                  title="Evolution du f1_score")

    event = viz.plotly_chart(fig, key="time_stamp", on_select="rerun")
    viz.markdown("#### Logs f1_scores:")
    viz.dataframe(df)
# --------------- Monitoring and updates --------------------------------------
with tab3:
    st.write("Monitoring")
