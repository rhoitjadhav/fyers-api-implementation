# Packages
import os

# Server Config
HOST = "localhost"
PORT = 8000
SERVER_URL = f"http://{HOST}:{PORT}"

# Fyers Credentials
APP_ID = os.getenv("APP_ID")
REDIRECT_URL = os.getenv("REDIRECT_URL")
APP_SECRET = os.getenv("APP_SECRET")
CLIENT_ID = os.getenv("CLIENT_ID")
