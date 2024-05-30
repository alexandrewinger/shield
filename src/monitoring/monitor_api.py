# ---------------------------- Imports ----------------------------------------
from fastapi import FastAPI
import subprocess

# ---------------------------- HTTP Exceptions --------------------------------
responses = {
    200: {"description": "OK"},
    401: {"description": "Identifiant ou mot de passe invalide(s)"}
}

# ---------------------------- API --------------------------------------------

api = FastAPI(
    title="🛡️ Watch Model Performances",
    description="API to watch over performances of SHIELD model.",
    version="0.1",
    openapi_tags=[
        {'name': 'MONITOR',
         'description': 'Monitor model perfomances and update if necessary'}
        ])

# ---------- 1. Vérification du fonctionnement de l’API: ----------------------


@api.get('/status', name="Checks if API is functionnal")
async def is_fonctionnal():
    """
    Checks if API is functionnal
    """
    return {"Montoring API available."}


# ---------- EP2: Monitoring --------------------------------------------------
@api.get('/monitor',
         name="Monitor model perfomances and update if necessary"
         )
async def monitor():
    subprocess.run(['python3', 'src/monitoring/monitoring.py'])
