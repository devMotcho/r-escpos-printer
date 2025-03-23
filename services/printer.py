import time
from models.logger import Logger
from escpos.printer import Network
from models.log_level import LogLevel
from app.settings import MAX_ATTEMPTS, PRINTER_IP

def connect_printer() -> tuple:
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
            logger = Logger()
            logger.log(LogLevel.ERROR, f"Erro ao conectar com a impressora após {attempt+1} tentativas. {str(e)}")
        time.sleep(2)
    return (False, None)
            

