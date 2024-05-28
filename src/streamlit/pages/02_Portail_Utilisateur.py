import streamlit as st
import requests # noqa F401
import os
from pathlib import Path
import sys

# internal
root_path = Path(os.path.realpath(__file__)).parents[3]
sys.path.append(os.path.join(root_path, "src", "streamlit"))
from streamlit_library import prepare_jsonl, predict, label_prediction # noqa E402

# -------------- Variables declaration: ---------------------------------------
localhost = "127.0.0.1"
# user_payload = st.session_state['id']
header_admin = {"identification": "admin:4dmin"}
header_user = {"identification": "fdo:c0ps"}

# --------------- Page --------------------------------------------------------
st.set_page_config(layout="wide")
st.title("SHIELD")
st.write("Bienvenue sur le portail SHIELD standard")

tab1, tab2 = st.tabs(["Utilisation", "Feedback"])

# ----- Predict from call:
with tab1:
    predict.call()

# ----- Label prediction:
with tab2:
    label_prediction.from_call()
