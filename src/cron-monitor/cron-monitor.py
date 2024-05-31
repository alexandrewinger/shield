import requests
import os

localhost = "monitoring" if os.environ.get('ENVIRONMENT') == 'docker' else "127.0.0.1" # noqa E501

response = requests.get(url=f"http://{localhost}:8008/monitor")
