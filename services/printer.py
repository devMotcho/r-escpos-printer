import time
from escpos.printer import Network

from models.order import Order
from models.logger import Logger
from models.customer import Customer
from models.log_level import LogLevel
from app.settings import MAX_ATTEMPTS, PRINTER_IP, RETRY_DELAY
from utils.strings import wrapper, calculated_space_between

def connect_printer(logger: Logger) -> tuple:
    """
    Attempts to connect to a network printer and configure it for text printing.

    The function tries to establish a connection with the printer up to a maximum number of
    attempts defined by MAX_ATTEMPTS. On each attempt, it:
      - Instantiates a Network printer object using the PRINTER_IP.
      - Sets the printer's character encoding to 'CP858' (this may be adjusted based on the printer).
      - Opens the connection to the printer.
      - Checks if the printer is online, and if so, sends an empty text to verify connectivity,
        then returns a tuple (True, printer).

    If the printer is not online, the connection is closed and the function waits for 2 seconds
    before retrying. In case of any exception during connection, the error is logged with the Logger.
    If the connection fails after all attempts, the function returns (False, None).

    Returns:
        tuple: A tuple where the first element is a boolean indicating whether the connection
               was successful, and the second element is the printer object (or None if unsuccessful).
    """
    for attempt in range(MAX_ATTEMPTS):
        try:
            printer = Network(PRINTER_IP)
            printer.charcode('CP858') # change to other charset if your printer allows
            printer.open()
            
            if printer.is_online():
                printer.text("")
                return (True, printer)
            printer.close()
        
        except Exception as e:
            logger.log(LogLevel.ERROR, f"Erro ao conectar com a impressora após {attempt+1} tentativas. {str(e)}")
        time.sleep(RETRY_DELAY)
    return (False, None)


def print_order(order : Order, customer: Customer, printer : Network.Printer, logger : Logger) -> bool:
    """
    Prints an order receipt to an 80mm printer with formatted customer and order details.

    This function formats and sends order details to a network-connected printer. It uses the provided
    `order` and `customer` objects to build a formatted receipt, which includes order information,
    customer details, and a list of ordered products. The text is wrapped using the `wrapper` function to
    fit within the printer's width constraints. Printer settings like alignment and bold formatting are
    applied to enhance the printed output. If any errors occur during printing, the error is logged,
    and the printer connection is closed.

    Args:
        order (Order): The order instance containing details such as order ID, delivery information,
                       order products, and total price.
        customer (Customer): The customer instance with details such as name, email, NIF, address,
                             and phone number.
        printer (Network.Printer): An instance of the printer, expected to have the method `set` and
                                   other printing methods like `text` and `cut`.
        logger (Logger): An instance of the Logger class used to log errors.

    Returns:
        bool: True if the order was printed successfully, False if any errors occurred or if the printer
              is not properly connected.
    """

    if not printer or not hasattr(printer, 'set'):
        logger.log(LogLevel.ERROR, f"Sem impressora conectada.")
        return False
    
    try:
        # A dictionary with formatted order and customer details.
        data = {
            "title" : f"Pedido n.{str(order.id)} Rodízio Ementa Digital",

            "order_type" : f"Tipo do Pedido: {order.order_type()}",
            "delivery_date" : f"Data de Entrega: {order.formated_date()}",
            "delivery_time" : f"Hora de Entrega: {order.formated_time()}",
            
            "customer_title" : f"Informações do Cliente",
            "nif" : f"NIF: {customer.nif}",
            "full_address" : f"Morada: {customer.full_address}",
            "customer" : f"Cliente: {customer.name}",
            "email" : f"Email: {customer.email}",
            "phone_number" : f"Tel.: {customer.phone_number}",

            "product_order_title" : f"Produtos do Pedido:",
            "total" : f"TOTAL: {order.total_price} EUR"
        }

        # Print Order most critical data info
        printer.set(align="center", bold=True)
        printer.text(wrapper(data["title"]))
        printer.text(wrapper(data["order_type"]))
        printer.text(wrapper(data["delivery_date"]))
        printer.text(wrapper(data["delivery_time"]))
        printer.text(wrapper(data["nif"]))
        printer.text(wrapper(data["full_address"]))
        printer.text("\n")

        # Print Customer only info
        printer.set(align="center", bold=True)
        printer.text(wrapper(data["customer_title"]))
        printer.set(align="left", bold=False)
        printer.text(wrapper(data["customer"]))
        printer.text(wrapper(data["email"]))
        printer.text(wrapper(data["phone_number"]))
        printer.text("\n")

        # Print the product details of the order
        printer.set(align="center", bold=True)
        printer.text(wrapper(data["product_order_title"]))
        printer.set(align="left", bold=False)

        # Iterate through each ordered product and print its details.
        for instance in order.order_products:

            printer.text(wrapper(instance.product_name))
            printer.text(wrapper(instance.product_accompaniment))

            # Format a line that shows the quantity and price with appropriate spacing.
            quantity_price_line = calculated_space_between(f'{instance.quantity} x', instance.price_str())
            printer.text(quantity_price_line + '\n')

            printer.text(wrapper(f'Nota do Pedido: {instance.note}'))
            printer.text("\n")
        
        printer.text("\n")
        printer.text(data["total"])

        printer.cut()
        return True            

    except (AttributeError, OSError) as e:
        logger.log(LogLevel.ERROR, f"Erro ao imprimir o pedido nº{order.id} : {str(e)}")
        printer.close()
        return False
    
