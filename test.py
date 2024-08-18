import unittest
from unittest import TestCase
from planetae_logger import Logger


log_file = "test.log"

logger = Logger(name="test", log_file=log_file)


class TestLogs(TestCase):
    def test_clean_log(self):
        with open(log_file, "w") as f:
            f.write("")
        with open(log_file) as f:
            empty = f.read()
        self.assertEqual(empty, "")

    def test_log_debug_logger(self):
        debug_message = logger.debug('debug message')
        self.assertEqual(debug_message, "AAAA-MM-DD HH:MM:SS,mmm - test - DEBUG - debug message")

    def test_log_info_logger(self):
        info_message = logger.info("info message")
        self.assertEqual(info_message, "AAAA-MM-DD HH:MM:SS,mmm - test - INFO - info message")

    def test_log_warning_logger(self):
        warning_message = logger.warning("warning message")
        self.assertEqual(warning_message, "AAAA-MM-DD HH:MM:SS,mmm - test - WARNING - warning message")

    def test_log_error_logger(self):
        error_message = logger.error("error message")
        self.assertEqual(error_message, "AAAA-MM-DD HH:MM:SS,mmm - test - ERROR - error message")

    def test_log_critical_logger(self):
        critical_message = logger.critical("critical message")
        self.assertEqual(critical_message, "AAAA-MM-DD HH:MM:SS,mmm - test - CRITICAL - critical message")

    def test_read_logger(self):
        with open(log_file) as f:
            loggings = f.read().strip().split("\n")
        log_types = ["CRITICAL", "ERROR", "DEBUG", "INFO", "WARNING"]
        log_types.sort()
        for index, logging in enumerate(loggings):
            logs = logging.split(" - ")
            self.assertRegex(logs[0], r"(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})")
            self.assertEqual(logs[1], "test")
            self.assertEqual(logs[2], log_types[index])
            self.assertEqual(logs[3], f"{log_types[index].lower()} message")


if __name__ == "__main__":
    unittest.main()
