from models.logger import Logger
from models.log_level import LogLevel
from services.order_services import dummy_fetch_orders
from services.printer import connect_printer, print_order
from app.settings import PRINTER_IP

if __name__ == "__main__":
    
    orders_dto = dummy_fetch_orders()
    logger = Logger()

    
    success, printer = connect_printer(logger)

    for dto in orders_dto:        
        print_order(dto, printer, logger)


    