#!/bin/bash

# Fichier utilisé pour la conteneurisation de notre appli SHIELD.

# Création du volume:
     volume create --name shield_volume

# Pour rentrer dans un conteneur en cours d'exécution:
     exec -it <name> bash # si l'interpréteur est bash sur les images crées FROM ubuntu
     exec -it <name> sh # si l'interpréteur est sh sur les images crées FROM alpine
# Command to keep container running for debugging if needed:
    tail -f /dev/null

# -------------- 1. Image Import Data -----------------------------------------

# Création de l'image depuis la racine:
    docker image build  -f ./src/data/import_data.Dockerfile -t alexandrewinger/shield:import_data .

# Lancement depuis la racine: 
    docker run --rm --mount type=volume,src=shield_volume,dst=/home/volume alexandrewinger/shield:import_data

# -------------- 2. Image Make Dataset -----------------------------------------

# Création de l'image depuis la racine:
    docker image build  -f ./src/data/make_dataset.Dockerfile -t alexandrewinger/shield:make_dataset .

# Lancement depuis la racine: 
    docker run --rm --mount type=volume,src=shield_volume,dst=/home/volume alexandrewinger/shield:make_dataset


# -------------- Image 3. Create users db ---------------------------------------

# Création de l'image depuis la racine:
    docker image build  -f ./src/users_db/create_users_db.Dockerfile -t alexandrewinger/shield:create_users_db .

# Lancement depuis la racine: 

    docker run --rm --mount type=volume,src=shield_volume,dst=/home/volume alexandrewinger/shield:create_users_db


# -------------- Image 4. Train Model ---------------------------------------

# Création de l'image depuis la racine:
    docker image build  -f ./src/models/model.Dockerfile -t alexandrewinger/shield:train_model .

# Lancement depuis la racine: 

    docker run --rm --mount type=volume,src=shield_volume,dst=/home/volume alexandrewinger/shield:train_model

# --------------- Image 5. API ---------------------------------------------------
# Création de l'image `api`: 
    docker image build  -f ./src/api/api.Dockerfile -t alexandrewinger/shield:api .

# Lancement du conteneur à partir de l'image:
    docker run -p 8000:8000 --rm --mount type=volume,src=shield_volume,dst=/home/volume/ --network=shield-network --name api alexandrewinger/shield:api

    docker run -p 8000:8000 --rm --mount type=volume,src=shield_volume,dst=/home/volume/ --name api alexandrewinger/shield:api

# Test de l'api dans un autre terminal:
curl.exe -X GET -i http://127.0.0.1:8000/status

# L'autre voie  en utilisant l'IP du conteneur ne fonctionne pas, malgré beaucoup d'essais et d'investigation:
curl.exe -X GET -i http://172.17.0.2:8000/status
# curl: (28) Failed to connect to 172.17.0.2 port 8000 after 21042 ms: Couldn't connect to server

# --------------- Image 6. Test -----------------------------------------------
# Création de l'image `test_api`: 
    # docker image build  -f ./src/api/test_api.Dockerfile -t alexandrewinger/shield:test_api .

# Lancement depuis la racine: 

    # docker run --rm --mount type=volume,src=shield_volume,dst=/home/volume alexandrewinger/shield:test_api

# --------------- Image 7. Test Shield -----------------------------------
# Création de l'image `test_shield`: 
docker image build  -f ./src/test/test_shield.Dockerfile -t alexandrewinger/shield:test_shield .

# Lancement depuis la racine: 

    docker run --rm --mount type=volume,src=shield_volume,dst=/home/volume --network=shield-network --name test_shield alexandrewinger/shield:test_shield


# --------------- Image 8. Monitoring -----------------------------------------
# Création de l'image `monitoring`: 
docker image build  -f ./src/monitoring/monitoring.Dockerfile -t alexandrewinger/shield:monitoring .

# Lancement du conteneur à partir de l'image:
docker run -p 8008:8008 --rm --mount type=volume,src=shield_volume,dst=/home/volume/ --network=shield-network --name monitoring alexandrewinger/shield:monitoring

docker run -p 8008:8008 --rm --mount type=volume,src=shield_volume,dst=/home/volume/ --name monitoring alexandrewinger/shield:monitoring

# Test de l'api dans un autre terminal:
curl.exe -X GET -i http://127.0.0.1:8008/status

# --------------- Image 9. Cron Monitor -----------------------------------------
# Création de l'image `cron-monitor`: 
docker image build  -f ./src/cron-monitor/cron-monitor.Dockerfile -t alexandrewinger/shield:cron-monitor .

# Lancement du conteneur à partir de l'image:
docker run -p 8009:8009 --rm --mount type=volume,src=shield_volume,dst=/home/volume/ --init --network=shield-network --name cron-monitor alexandrewinger/shield:cron-monitor

docker run -p 8009:8009 --rm --mount type=volume,src=shield_volume,dst=/home/volume/ --init --name cron-monitor alexandrewinger/shield:cron-monitor

# --------------- Image 10. Streamlit -----------------------------------------
# Création de l'image `streamlit`: 
docker image build  -f ./src/streamlit/streamlit.Dockerfile -t alexandrewinger/shield:streamlit .

# Lancement du conteneur à partir de l'image:
docker run -p 8501:8501 --rm --mount type=volume,src=shield_volume,dst=/home/volume/ --init --network=shield-network --name streamlit alexandrewinger/shield:streamlit

docker run -p 8501:8501 --rm --mount type=volume,src=shield_volume,dst=/home/volume/ --init --name streamlit alexandrewinger/shield:streamlit