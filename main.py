from models.logger import Logger
from models.log_level import LogLevel
from services.order_services import dummy_fetch_orders
from services.printer import connect_printer, print_order
from app.settings import PRINTER_IP

from controllers.script import ScriptController

if __name__ == "__main__":
    
    controller = ScriptController()
    controller.start_script()


    