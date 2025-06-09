# app/config.py

import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# API URLs
GATEWAY_API_URL = os.getenv("GATEWAY_API_URL")
DEVICE_API_URL = os.getenv("DEVICE_API_URL")
GATEWAY_STATUS_API_URL = os.getenv("GATEWAY_STATUS_API_URL")
DEVICE_STATUS_API_URL = os.getenv("DEVICE_STATUS_API_URL")