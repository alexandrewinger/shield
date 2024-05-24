import streamlit as st
import requests
from streamlit_library import prepare_jsonl


def from_call():

    # -------------- Variables declaration: -----------------------------------
    localhost = "127.0.0.1"
    header_user = {"identification": "fdo:c0ps"}
    log_data = {"name": "preds_call"}

    st.title(body="Retour Utilisateur: Vérifier une prédiction")

    # --------------- Label prediction: ---------------------------------------
    response = requests.post(url=f"http://{localhost}:8000/get_logs",
                                 json=log_data,
                                 headers=header_user)
    data_jsonl = response.json()
    df = prepare_jsonl.jsonl_to_df(data_jsonl)

    st.write("Prédiction non labellisées:")
    st.dataframe(df)

    request_id = st.selectbox(
        label="Choisir dans la liste l'identifiant de la prédiction " +
              "à vérifier:",
        options=df['request_id'].to_list()
    )

    st.write("")

    verify_pred = st.radio(
        "Quelle a été la priorité réelle de l'accident?",
        ["Non Prioritaire", "Prioritaire"]
    )
    if verify_pred == "Non Prioritaire":
        prediction = {"request_id": request_id,
                      "y_true": 0}
    if verify_pred == "Prioritaire":
        prediction = {"request_id": request_id,
                      "y_true": 1}

    if st.button("Valider le retour"):
        url = f"http://{localhost}:8000/label_prediction"
        response = requests.post(url=url,
                                 json=prediction,
                                 headers=header_user)
        st.write("Merci pour votre retour!")
