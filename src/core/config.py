# Packages
import os

# API Server Config
HOST = "localhost"
PORT = 8545
SERVER_URL = f"http://{HOST}:{PORT}"

# Fyers Credentials
APP_ID = os.getenv("APP_ID", "BEPTBTGALL-100")
REDIRECT_URL = os.getenv("REDIRECT_URL", f"http://{HOST}:{PORT}/generate-access-token")
APP_SECRET = os.getenv("APP_SECRET", "DOXRLGHAG2")
CLIENT_ID = os.getenv("CLIENT_ID", "XR09997")

# Redis Config
REDIS_HOST = "localhost"
REDIS_PORT = 6390
REDIS_DB = 0
