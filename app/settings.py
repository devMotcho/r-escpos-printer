import os
from dotenv import load_dotenv

load_dotenv()

MAX_ATTEMPTS = 3 # n of max attempts until the script stops
LINE_WIDTH = 48 # 80mm line width

LOG_FILE = "log.txt"

BASE_URL = os.getenv("BASE_URL")
PRINTER_IP = os.getenv("PRINTER_ID")
PRINTER_PORT = os.getenv("PRINTER_PORT")