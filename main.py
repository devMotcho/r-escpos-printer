from models.logger import Logger
from models.log_level import LogLevel

if __name__ == "__main__":
    logger = Logger()
    logger.log(LogLevel.INFO, "All running!")