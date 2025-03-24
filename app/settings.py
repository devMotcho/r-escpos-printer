import os
from dotenv import load_dotenv

load_dotenv()

MAX_ATTEMPTS = 3 # n of max attempts until the script stops
RETRY_DELAY = 2 # seconds between attempts
LINE_WIDTH = 48 # 80mm line width

LOG_FILE = "log.txt"

BASE_URL = os.getenv("BASE_URL")
PRINTER_IP = os.getenv("PRINTER_ID")
PRINTER_PORT = os.getenv("PRINTER_PORT")

AUTH_URL = f'{BASE_URL}auth/'
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

ORDERS_URL = f'{BASE_URL}order/print-orders/'
UPDATE_ORDER_URL = f'{BASE_URL}order/print-orders-status/' # add order.id