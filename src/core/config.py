# Packages
import os
from dotenv import load_dotenv

load_dotenv()

# API Server Config
API_SERVER_HOST = os.getenv("API_SERVER_HOST")
API_SERVER_PORT = int(os.getenv("API_SERVER_PORT"))
API_SERVER_URL = f"http://{API_SERVER_HOST}:{API_SERVER_PORT}"

# Fyers Credentials
FYERS_USERNAME = os.getenv("FYERS_USERNAME")
FYERS_PASSWORD = os.getenv("FYERS_PASSWORD")
PAN_ID = os.getenv("PAN_ID")
APP_ID = os.getenv("APP_ID")
REDIRECT_URL = os.getenv("REDIRECT_URL", f"http://{API_SERVER_HOST}:{API_SERVER_PORT}/generate-access-token")
APP_SECRET = os.getenv("APP_SECRET")

# Redis Config
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT"))
REDIS_DB = 0

# ZMQ Configuration
ZMQ_HOST = os.getenv("ZMQ_HOST")
ZMQ_PORT = int(os.getenv("ZMQ_PORT"))
