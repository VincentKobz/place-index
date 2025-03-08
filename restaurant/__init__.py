import os
import logging
from dotenv import load_dotenv

load_dotenv()

GMAPS_API_KEY = os.getenv("GMAPS_API_KEY")
TRIP_API_KEY = os.getenv("TRIP_API_KEY")
LLM_KEY = os.getenv("OPEN_AI_KEY")

# Define log level
logging.basicConfig(level=logging.INFO)
