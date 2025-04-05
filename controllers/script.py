"""
Main controller class for managing order processing automation script.
Handles system checks, printer management, order processing, and error handling with retry logic.
"""

import time
import threading
import winsound

from utils.checks import check_url
from models.logger import Logger
from models.log_level import LogLevel
from models.error_type import ErrorType
from models.order import Order, OrderDto
from app.settings import CHECK_SERVER_HEALTH, CHECK_INTERNET_URL, MAX_ATTEMPTS, RETRY_DELAY
from services.printer import connect_printer, print_order
from services.auth import get_auth_tokens
from services.order_services import fetch_orders, dummy_fetch_orders, update_order_status


class ScriptController:
    """Main controller class for managing script execution and coordination between components."""
    
    def __init__(self):
        """Initialize script control variables and resources."""
        self.running = False              # Flag to track script running state
        self.thread = None                # Worker thread reference
        self.stop_event = threading.Event()  # Event flag for graceful shutdown
        self.status_message = "A correr sem problemas aparentes."  # Current status message
        self.logger = Logger()            # Logger instance for system logging
        self.lock = threading.Lock()       # Thread synchronization lock
        self.printer = None               # Printer connection reference

        # Sound alert control
        self.sound_stop_event = threading.Event()
        self.sound_thread = None
        

    def start_script(self):
        """Start the main processing thread if not already running."""
        if not self.running:
            with self.lock:  # Thread-safe start
                self.stop_event.clear()
                self.thread = threading.Thread(target=self.main_loop)
                self.thread.start()
                self.running = True

    def stop_script(self):
        """Stop the processing thread and wait for graceful shutdown."""
        with self.lock:  # Thread-safe stop
            if self.running:
                self.stop_event.set()
                if self.thread and self.thread.is_alive():
                    try:
                        self.thread.join(timeout=5)  # Wait for thread completion
                    except RuntimeError:
                        pass
                self.running = False
                self.stop_alert_sound()

    def start_alert_sound(self):
        """Start the alert sound loop in a dedicated thread."""
        # Stop any existing alert sound
        self.stop_alert_sound()
        
        # Start new alert thread
        self.sound_stop_event.clear()
        self.sound_thread = threading.Thread(target=self.play_alert_sound)
        self.sound_thread.start()

    def stop_alert_sound(self):
        """Stop the alert sound loop."""
        self.sound_stop_event.set()
        if self.sound_thread and self.sound_thread.is_alive():
            self.sound_thread.join()
        self.sound_thread = None
    
    def play_alert_sound(self):
        """Continuous alert sound until stopped (Windows beep example)."""
        while not self.sound_stop_event.is_set():
            try:
                # Windows system beep (1000Hz for 500ms)
                winsound.Beep(1000, 500)
                # Add interval between beeps
                time.sleep(0.5)
            except Exception as e:
                self.logger.log(LogLevel.ERROR, f"Sound error: {str(e)}")
                break

    def error_occurred(self, message: str, log_message: str):
        """
        Handle critical errors by updating status and stopping execution.
        
        Args:
            message (str): User-friendly error message
            log_message (str): Technical details for logging
        """
        with self.lock:
            self.status_message = f'ERROR: {message}. Reinicie o programa.'
            self.logger.log(LogLevel.ERROR, log_message)
            self.stop_event.set()  # Trigger shutdown
            self.start_alert_sound()

    def main_loop(self):
        """Main processing loop handling system checks, authentication, and order processing."""
        try:
            while not self.stop_event.is_set():
                # System health checks
                if not self.perform_system_checks():
                    time.sleep(10)  # Wait before retrying checks
                    continue

                # API authentication
                auth_status, token, auth_error = get_auth_tokens()
                if not auth_status:
                    self.error_occurred(ErrorType.AUTHENTICATION.value, auth_error)
                    continue  # Will exit if stop_event is set

                # Order processing with retry logic
                try:
                    # orders = dummy_fetch_orders()  # For testing without API
                    orders = fetch_orders(token)
                    print(orders)
                    if orders and not self.process_orders_with_retry(orders, token):
                        continue
                except Exception as e:
                    self.error_occurred(ErrorType.ORDER_PROCESSING.value, f'Erro pedidos: {str(e)}')
                    continue

                time.sleep(20)  # Normal interval between processing cycles

        except Exception as e:
            self.error_occurred(ErrorType.UNEXPECTED.value, f"Erro Inesperado: {str(e)}")
        finally:
            self.cleanup_resources()

    def perform_system_checks(self) -> bool:
        """
        Execute all system prerequisite checks.
        
        Returns:
            bool: True if all checks pass, False otherwise
        """
        checks = [
            # (check_function, error_message, log_message)
            (lambda: check_url(CHECK_INTERNET_URL), ErrorType.INTERNET_CONNECTION.value, "Sem conexão à internet."),
            (self.check_printer_connection, ErrorType.PRINTER_CONNECTION.value, "Sem conexão à impressora"),
            (lambda: check_url(CHECK_SERVER_HEALTH), ErrorType.SERVER_CONNECTION.value, "Sem conexão com o servidor")
        ]

        for check_fn, err_msg, log_msg in checks:
            if not self.safe_check(check_fn, err_msg, log_msg):
                return False
        return True

    def process_orders_with_retry(self, orders: list[OrderDto], token: str) -> bool:
        """
        Process order list with retry logic for both printing and status updates.
        
        Args:
            orders (list[Order]): List of orders to process
            token (str): Authentication token
            
        Returns:
            bool: True if all orders processed successfully, False if critical error occurred
        """
        for order in orders:
            if self.stop_event.is_set():
                return False  # Early exit requested

            # Print order with retry attempts
            if not self.retry_print_operation(order):
                return False

            # Update order status with retry attempts
            if not self.retry_status_update(order, token):
                return False

        return True

    def retry_print_operation(self, order: OrderDto) -> bool:
        """
        Attempt order printing with reconnection retries.
        
        Args:
            order (Order): Order to print
            
        Returns:
            bool: True if printed successfully, False if failed after max attempts
        """
        for attempt in range(MAX_ATTEMPTS):
            try:
                # Verify printer connection and attempt print
                if self.check_printer_connection() and print_order(order, self.printer, self.logger):
                    return True

                # Retry logic
                self.logger.log(LogLevel.WARNING, 
                              f'Retrying print {order.id} (attempt {attempt+1}/{MAX_ATTEMPTS})')
                time.sleep(RETRY_DELAY)
                self.printer = None  # Force printer reconnection on next attempt
            except Exception as e:
                self.logger.log(LogLevel.ERROR, 
                               f'Erro inesperado ao imprimir o pedido {order.id} : {str(e)}')

        # Critical failure after all attempts
        self.error_occurred(ErrorType.ORDER_PROCESSING.value, 
                           f'Falha após {MAX_ATTEMPTS} tentativas de imprimir o pedido n {order.id}')
        return False

    def retry_status_update(self, order: Order, token: str) -> bool:
        """
        Attempt order status update with retries.
        
        Args:
            order (Order): Order to update
            token (str): Authentication token
            
        Returns:
            bool: True if update successful, False after max attempts
        """
        for attempt in range(MAX_ATTEMPTS):
            try:
                if update_order_status(order, token):
                    return True
                time.sleep(RETRY_DELAY)
            except Exception as e:
                self.logger.log(LogLevel.ERROR,
                              f'Atualização de status de impressão do pedido n {order.id} falhou : {str(e)}')
        return False  # Non-critical failure, continues processing other orders

    def check_printer_connection(self) -> bool:
        """
        Manage printer connection state with automatic reconnection.
        
        Returns:
            bool: True if valid connection exists
        """
        try:
            # Check existing connection validity
            if self.printer and self.validate_printer_connection():
                return True
            
            # Establish new connection if needed
            status, new_printer = connect_printer(self.logger)
            if status:
                self.printer = new_printer
                return True
            return False
            
        except Exception as e:
            self.logger.log(LogLevel.ERROR, f'Conexão com impressora falhou: {str(e)}')
            return False

    def validate_printer_connection(self) -> bool:
        """
        Verify active printer connection by sending test command.
        
        Returns:
            bool: True if printer responds correctly
        """
        try:
            # Simple test command to verify connection
            self.printer.text("")
            return True
        except Exception as e:
            self.logger.log(LogLevel.WARNING, 
                           "Teste de atividade da impressora falhou, talvez esteja desconectada...")
            self.printer = None  # Reset connection reference
            return False

    def safe_check(self, check_func: callable, error_message: str, log_message: str) -> bool:
        """
        Execute a check function with error handling.
        
        Args:
            check_func (callable): Function returning boolean success status
            error_message (str): User-friendly error description
            log_message (str): Technical error details
            
        Returns:
            bool: True if check passed, False if failed or error occurred
        """
        try:
            result = check_func()
            if not result:
                self.error_occurred(error_message, log_message)
                return False
            return True
        except Exception as e:
            self.error_occurred(error_message, f"{log_message}: {str(e)}")
            return False
        
    def cleanup_resources(self):
        """Clean up system resources and reset state during shutdown."""
        try:
            if self.printer:
                self.printer.close()  # Properly close printer connection
        except Exception as e:
            self.logger.log(LogLevel.INFO, f'Cleanup error: {str(e)}')
        finally:
            self.printer = None
            self.running = False
            self.stop_event.set()  # Ensure event flag is reset