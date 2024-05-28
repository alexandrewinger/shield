import os
import requests
import streamlit as st

# -------------- Variables declaration: ---------------------------------------
localhost = "api" if os.environ.get('ENVIRONMENT') == 'docker' else "127.0.0.1" # noqa E501

# -------------- Homepage: ----------------------------------------------------
st.title("SHIELD")
st.write("Identification")
st.sidebar.title(":shield: Shield App")

username = st.text_input("Nom d'utilisateur:")
password = st.text_input("Mot de passe:")
id = username + ":" + password
user_payload = {"identification": id}

if st.button("S'identifier"):
    response = requests.get(url=f"http://{localhost}:8000/get_rights",
                            headers=user_payload)
    rights = response.json()

    if 'id' not in st.session_state:
        st.session_state['id'] = user_payload

    if rights == 0:
        st.switch_page("pages/standard_user_page.py")
    else:
        st.switch_page("pages/admin_page.py")
