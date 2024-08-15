from datetime import datetime
from typing import Any


class _LoggerDecorator:
    def __init__(self, function) -> None:
        self.function = function

    def __call__(self, *args, **kwargs) -> None:
        try:
            print(args, kwargs)
            result = self.function(*args, **kwargs)
            self._log_output(result, filename="log.txt")
        except Exception as e:
            self._log_output(e, filename="crash_log.txt")
            raise

    @staticmethod
    def _log_output(output: Any, filename: str) -> None:
        with open(filename, "a") as log_file:
            log_file.write(str(output) + " " + datetime.now().isoformat() + " " + "\n")


class Logger:
    standard_output: str
    exceptions_output: str

    def __init__(self, standard_output: str, exceptions_output: str) -> None:
        self.standard_output = standard_output
        self.exceptions_output = exceptions_output

    @staticmethod
    @_LoggerDecorator
    def log_exception(exception: Exception) -> None:
        raise exception

    @staticmethod
    @_LoggerDecorator
    def log_string(string: str) -> str:
        return string

    @staticmethod
    @_LoggerDecorator
    def log_iterable(iterable: list | tuple, name: str = "Array") -> str:
        string = name + ":\n"
        for i in iterable:
            string += "\t" + str(i)
        return string + "\n"

    @staticmethod
    @_LoggerDecorator
    def log_dict(json: dict, name: str = "json") -> str:
        def pprint_json(dictionary: dict | list) -> str:
            pprint_string = ""
            if isinstance(dictionary, dict):
                pprint_string = "{\n"
                for key, value in dictionary:
                    if not isinstance(value, dict):
                        pprint_string += f"\t{key}: {value}\n"
                    else:
                        pprint_string += f"\t{key}: {pprint_json(value)}\n"
                pprint_string += "}"
            elif isinstance(dictionary, list):
                pprint_string = "[\n"
                for i in dictionary:
                    pprint_string += f"\t{i},\n"
                pprint_string = "]"
            return pprint_string

        string = name + ":\n"
        string += pprint_json(dictionary=json)
        return string

    @staticmethod
    @_LoggerDecorator
    def log_object(obj: object) -> str:
        return str(obj)
