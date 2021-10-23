# Packages
import os
from dotenv import load_dotenv

load_dotenv()

# API Server Config
HOST = "localhost"
PORT = 8545
SERVER_URL = f"http://{HOST}:{PORT}"

# Fyers Credentials
FYERS_USERNAME = os.getenv("FYERS_USERNAME")
FYERS_PASSWORD = os.getenv("FYERS_PASSWORD")
PAN_ID = os.getenv("PAN_ID")
APP_ID = os.getenv("APP_ID")
REDIRECT_URL = os.getenv("REDIRECT_URL", f"http://{HOST}:{PORT}/generate-access-token")
APP_SECRET = os.getenv("APP_SECRET")

# Redis Config
REDIS_HOST = "localhost"
REDIS_PORT = 6390
REDIS_DB = 0
