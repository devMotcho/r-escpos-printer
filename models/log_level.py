from enum import Enum

class LogLevel(Enum):
    """
    An enumeration for log levels to help classify log messages.

    Attributes:
        ERROR (int): Represents critical errors.
        WARNING (int): Represents warning messages.
        INFO (int): Represents informational messages.
    """
    ERROR = 1
    WARNING = 2
    INFO = 3

    def __str__(self):
        return f'[{self.name}]'
