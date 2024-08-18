import unittest
from unittest import TestCase
from .logger import Logger


logs_file = "logs.txt"
crash_logs_file = "crash_logs.txt"

logger = Logger(standard_output=logs_file, exceptions_output=crash_logs_file)


class TestLogs(TestCase):
    def test_clean_logs(self):
        with open(logs_file, "w") as f:
            f.write("")
        with open(crash_logs_file, "w") as f:
            f.write("")
        with open(logs_file) as f:
            empty = f.read()
        self.assertEqual(empty, "")
        with open(crash_logs_file) as f:
            empty = f.read()
        self.assertEqual(empty, "")

    def test_logger(self):
        logger.log_string("testing 01")
        with open(logs_file, "r") as file:
            logs = " ".join(file.read().strip().split()[:2])
        self.assertEqual(logs, "testing 01")

    def test_crash_logger(self):
        logger.log_exception(ValueError("Alô som, 1, 2, 3"))
        with open(crash_logs_file) as f:
            crash_logs = " ".join(f.read().strip().split()[:5])
        self.assertEqual(crash_logs, "Alô som, 1, 2, 3")


if __name__ == "__main__":
    unittest.main()
