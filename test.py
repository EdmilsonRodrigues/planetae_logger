from logger import Logger

logger = Logger(standard_output="logs.txt", exceptions_output="crash_logs.txt")
logger.log_string("testing 01")