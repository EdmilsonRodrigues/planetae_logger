import logging
from logging.handlers import RotatingFileHandler
import re


format = "{datetime} - {name} - {level} - {message}"


class Logger:
    """
    A class for creating a logger instance

    This class provides methods to log exceptions, strings, iterables, dictionaries,
    and objects. The logs are stored in specified output strings.
    """
    name: str
    log_file: str = None
    level: int = logging.DEBUG
    max_bytes: int = 1000000
    backup_count: int = 3

    def __init__(self, name: str, log_file: str = None, level: int = logging.DEBUG, max_bytes: int = 1000000, backup_count: int = 3) -> None:
        """
        Initialise a logger instance

        :param name: The name of the logger
        :type name: str
        :param log_file: The name of the log file
        :type log_file: str
        :param level: The logging level
        :type level: int
        :param max_bytes: The maximum size in bytes of the log file
        :type max_bytes: int
        :param backup_count: The number of log files to backup
        :type backup_count: int
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.name = name

        # Create a formatter
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        if log_file is not None:
            file_handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def _format_return(self, level: str, message: str) -> str:
        return format.format(datetime="AAAA-MM-DD HH:MM:SS,mmm", name=self.name, level=level, message=message)

    def debug(self, msg: str) -> str:
        self.logger.debug(msg)
        return self._format_return("DEBUG", msg)

    def info(self, msg: str) -> str:
        self.logger.info(msg)
        return self._format_return("INFO", msg)

    def warning(self, msg: str) -> str:
        self.logger.warning(msg)
        return self._format_return("WARNING", msg)

    def error(self, msg: str) -> str:
        self.logger.error(msg)
        return self._format_return("ERROR", msg)

    def critical(self, msg: str) -> str:
        self.logger.critical(msg)
        return self._format_return("CRITICAL", msg)
