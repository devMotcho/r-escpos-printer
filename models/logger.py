import os
from datetime import datetime
from app.settings import LOG_FILE

class Logger:
    """
    Provides logging capabilities to write messages to a text file for debugging and error tracking.

    Attributes:
        filename (str): The path to the log file where entries are recorded.
    """
    
    def __init__(self, filename: str = LOG_FILE):
        """
        Initializes the Logger instance.

        Args:
            filename (str): The log file path. Defaults to the LOG_FILE defined in settings.
        """
        self.filename = filename
        self.initialize_log_file()
        
    def initialize_log_file(self):
        """
        Creates the log file with a header if it doesn't already exist.
        The header includes a title and the creation timestamp.
        """
        if not os.path.exists(self.filename):
            with open(self.filename, "w", encoding="UTF-8") as f:
                f.write("========== LOGGING STARTED ==========\n")
                f.write(f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("====================================\n\n")
    
    def log(self, log_type: str, message: str):
        """
        Appends a log entry to the log file with the current timestamp.

        Args:
            log_type (str): The type of log (e.g., formatted using LogLevel, such as "[ERROR]").
            message (str): The log message to be recorded.
        """
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        log_entry = f"{log_type} {timestamp} {message}\n"

        with open(self.filename, "a", encoding="UTF-8") as f:
            f.write(log_entry)
