import os
from dotenv import load_dotenv
import requests

load_dotenv()

key = os.getenv("APCA_API_KEY_ID")
secret = os.getenv("APCA_API_SECRET_KEY")
base_url = os.getenv("APCA_API_BASE_URL")

if not key or not secret or not base_url:
    raise ValueError("Faltan variables de entorno de Alpaca en .env")

url = f"{base_url}/account"
headers = {
    "APCA-API-KEY-ID": key,
    "APCA-API-SECRET-KEY": secret
}

response = requests.get(url, headers=headers, timeout=20)
print(response.status_code)
print(response.text)
