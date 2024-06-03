import streamlit as st
import streamlit.components.v1 as components
import requests
from streamlit_library import features_dictionnary as feats_dict
import lime
import lime.lime_tabular
import joblib
import pandas as pd
import numpy as np
import os
from pathlib import Path

if os.environ.get('ENVIRONMENT') == 'docker':
    root_path = "/home/volume"
else:
    root_path = Path(os.path.realpath(__file__)).parents[3]

path_data_preprocessed = os.path.join(root_path, "data", "preprocessed")
path_X_train = os.path.join(path_data_preprocessed, "X_train.csv")
path_models = os.path.join(root_path, "models")


# --------------- Functions: --------------------------------------------------
def invert_dict(dict):
    inverted_dict = {value: key for key, value in dict.items()}
    return inverted_dict


def get_latest_model(path):
    """
    Get latest model version.
    Args:
        - path: str, path to directory containing model files
    Returns:
        - latest model name as str
    """
    model_names = os.listdir(path)
    if '.gitkeep' in model_names:
        model_names.remove('.gitkeep')
    minor_versions = []
    for model_name in model_names:
        version = model_name.split("_")[1]
        minor_version = int(version.split(".")[1])
        minor_versions.append(minor_version)
    latest_minor = max(minor_versions)
    latest_version = "rdf_v1." + str(latest_minor) + "_shield.joblib"
    return latest_version


def call():

    # -------------- Variables declaration: -----------------------------------
    localhost = "api" if os.environ.get('ENVIRONMENT') == 'docker' else "127.0.0.1" # noqa E501
    header_user = {"identification": "fdo:c0ps"}
    path_rdf = os.path.join(path_models, get_latest_model(path_models))

    st.title(body="Faire une prédiction à partir d'un appel")

    carac, lieu = st.columns(2)
    veh, usag = st.columns(2)

    # get input data for fiche baac, rubrique caractéristiques
    carac.header(body="Caractéristiques")

    # Other inputs ------------------------------------------------------------
    date_accident = carac.date_input(
        label="Date de l'accident",
        value="today",
    )
    heure_accident = carac.time_input(
        label=feats_dict.feature_names["hour"],
        value="now",
        step=3600,
    )
    lumiere = carac.selectbox(
        label=feats_dict.feature_names["lum"],
        options=feats_dict.lum.keys(),
    )
    departement = carac.selectbox(
        label=feats_dict.feature_names["dep"],
        options=feats_dict.deps.values(),
        placeholder="Sélectionnez un département",
    )
    commune = carac.selectbox(
        label=feats_dict.feature_names["com"],
        options=[com for com in feats_dict.coms.values()
                 if com[:2] == departement[:2]],
        placeholder="Sélectionnez une commune",
    )
    localisation = carac.selectbox(
        label=feats_dict.feature_names["agg_"],
        options=feats_dict.agg_.keys(),
    )
    intersection = carac.selectbox(
        label=feats_dict.feature_names["inter"],
        options=feats_dict.inter.keys(),
    )
    conditions_atmospheriques = carac.selectbox(
        label=feats_dict.feature_names["atm"],
        options=feats_dict.atm.keys(),
    )
    type_collision = carac.selectbox(
        label=feats_dict.feature_names["col"],
        options=feats_dict.col.keys(),
    )
    latitude = carac.number_input(
        label=feats_dict.feature_names["lat"],
        min_value=-90.0,
        max_value=90.0,
        step=0.001,
    )
    longitude = carac.number_input(
        label=feats_dict.feature_names["long"],
        min_value=-180.0,
        max_value=180.0,
        step=0.001,
    )
    # get input data for fiche baac, rubrique lieux
    lieu.header(body="Lieux")
    categorie_route = lieu.selectbox(
        label=feats_dict.feature_names["catr"],
        options=feats_dict.catr.keys(),
    )
    regime_circulation = lieu.selectbox(
        label=feats_dict.feature_names["circ"],
        options=feats_dict.circ.keys(),
    )
    etat_surface = lieu.selectbox(
        label=feats_dict.feature_names["surf"],
        options=feats_dict.surf.keys(),
    )
    situation_accident = lieu.selectbox(
        label=feats_dict.feature_names["situ"],
        options=feats_dict.situ.keys(),
    )
    vitesse_max_autorisee = lieu.number_input(
        label=feats_dict.feature_names["vma"],
        min_value=0,
        max_value=300,
        step=1,
    )
    # get input data for fiche baac, rubrique véhicules
    veh.header(body="Véhicules")
    categorie_vehicule = veh.selectbox(
        label=feats_dict.feature_names["catv"],
        options=feats_dict.catv.keys(),
    )
    obstacle_mobile = veh.selectbox(
        label=feats_dict.feature_names["obsm"],
        options=feats_dict.obsm.keys(),
    )
    type_motorisation = veh.selectbox(
        label=feats_dict.feature_names["motor"],
        options=feats_dict.motor.keys(),
    )
    nombre_vehicules = veh.number_input(
        label=feats_dict.feature_names["nb_vehicules"],
        min_value=0,
        max_value=100,
        step=1,
    )
    # get input data for fiche baac, rubrique usagers
    usag.header(body="Usagers")
    place_occupee = usag.slider(
        label=feats_dict.feature_names["place"],
        min_value=0,
        max_value=10,
        step=1,
        help="Le détail est donné par l’illustration ci-dessous. " +
        "Pour un piéton, sélectionnez « 10 ».",
    )
    categorie_usager = usag.selectbox(
        label=feats_dict.feature_names["catu"],
        options=feats_dict.catu.keys(),
    )
    sexe_usager = usag.selectbox(
        label=feats_dict.feature_names["sexe"],
        options=feats_dict.sexe.keys(),
    )
    age_usager = usag.number_input(
        label=feats_dict.feature_names["victim_age"],
        min_value=0,
        max_value=100,
        step=1,
    )
    equipement_securite = usag.selectbox(
        label=feats_dict.feature_names["secu1"],
        options=feats_dict.secu1.keys(),
    )
    nombre_usagers = usag.number_input(
        label=feats_dict.feature_names["nb_victim"],
        min_value=0,
        max_value=25,
        step=1,
    )
    st.write("")
    if st.button("Valider les données"):
        features_values = [
            int(place_occupee),
            int(feats_dict.catu[categorie_usager]),
            int(feats_dict.sexe[sexe_usager]),
            float(feats_dict.secu1[equipement_securite]),
            int(date_accident.year),
            int(age_usager),
            int(feats_dict.catv[categorie_vehicule]),
            int(feats_dict.obsm[obstacle_mobile]),
            int(feats_dict.motor[type_motorisation]),
            int(feats_dict.catr[categorie_route]),
            int(feats_dict.circ[regime_circulation]),
            int(feats_dict.surf[etat_surface]),
            int(feats_dict.situ[situation_accident]),
            int(vitesse_max_autorisee),
            int(date_accident.day),
            int(date_accident.month),
            int(feats_dict.lum[lumiere]),
            int(departement.split(" ")[0]),
            int(commune.split(" ")[0]),
            int(feats_dict.agg_[localisation]),
            int(feats_dict.inter[intersection]),
            int(feats_dict.atm[conditions_atmospheriques]),
            int(feats_dict.col[type_collision]),
            float(latitude),
            float(longitude),
            int(heure_accident.hour),
            int(nombre_usagers),
            int(nombre_vehicules)
        ]
        features = dict(zip(feats_dict.feature_names, features_values))
        if 'features' not in st.session_state:
            st.session_state['features'] = features
        st.write("Les données ont bien été validées. " +
                 "Vous pouvez effectuer la prédiction.")

    if st.button("Faire la prédiction"):
        # Get previous features:
        features = st.session_state['features']

        # Make prediction request:
        url_pred = f"http://{localhost}:8000/predict_from_call"
        response = requests.post(url=url_pred,
                                 json=features,
                                 headers=header_user)

        # Write result:
        st.write(response.json())

        # Display features importances with lime:
        # TODO: change for volume reference:
        rdf = joblib.load(path_rdf)
        X_train = pd.read_csv(path_X_train)
        input = dict(zip(invert_dict(feats_dict.feature_names), features))

        explainer = lime.lime_tabular.LimeTabularExplainer(
            X_train.values,
            feature_names=input.keys(),  # list of features
            class_names=["Non Prioritaire", "Prioritaire"],  # list of classes
            discretize_continuous=True)

        exp = explainer.explain_instance(
            np.array(list(features.values())),
            rdf.predict_proba,
            num_features=5)

        st.title('Explication des prédictions avec LIME')
        st.write('## Explication LIME')
        components.html(exp.as_html(), height=800)
