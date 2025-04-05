from enum import Enum

class ErrorType(Enum):
    """
    An enumeration for error types and their description.

    Attributes:
        INTERNET_CONNECTION (str): Represents internet connection error.
        SERVER_CONNECTION (str): Represents server connection error.
        PRINTER_CONNECTION (str): Represents printer connection error.
        FETCHING_ORDERS (str): Represents fetching order error.
        ORDER_UPDATE (str): Represents order updating error.
        
    """
    INTERNET_CONNECTION = 'Verifique a sua conexão à internet.'
    SERVER_CONNECTION = 'A conexão com o servidor falhou. Tente reiniciar o programa.'
    PRINTER_CONNECTION = 'A conexão com a impressora falhou. Tente verificar o estado da impressora.'
    AUTHENTICATION = 'Aconteceu um erro ao autenticar no sistema. Tente reiniciar o programa. Se o problema persistir contacte o responsável.'
    FETCHING_ORDERS = 'Aconteceu um erro ao pegar os pedidos. Tente reiniciar o programa.'
    ORDER_UPDATE = 'Aconteceu um erro ao atualizar os pedidos. Tente reiniciar o programa.'
    ORDER_PROCESSING = 'Aconteceu um erro ao processar os pedidos. Tente reinicar o programa.'
    UNEXPECTED = "Aconteceu um erro inesperado. Tente reiniciar o programa. Se o problema persistir contacte o responsável."

    def __str__(self):
        return self.name