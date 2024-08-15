from datetime import datetime
from typing import Any


class LoggerDecorator:
    def __init__(self, function) -> None:
        self.function = function

    def __call__(self, *args, **kwargs) -> None:
        try:
            result = self.function(*args, **kwargs)
            self._log_output(result, kwargs["standard_output"])
        except Exception as e:
            self._log_output(e, kwargs["exceptions_output"])
            raise

    def _log_output(self, output: Any, filename: str) -> None:
        with open(filename, "a") as log_file:
            log_file.write(str(output) + " " + datetime.now().isoformat() + " " + "\n")


class Logger:
    standard_output: str
    exceptions_output: str

    def __init__(self, standard_output: str, exceptions_output: str) -> None:
        self.standard_output = standard_output
        self.exceptions_output = exceptions_output

    @LoggerDecorator
    def log_exception(self, exception: Exception) -> None:
        raise exception

    @LoggerDecorator
    def log_string(self, string: str) -> str:
        return string

    @LoggerDecorator
    def log_iterable(self, iterable: list | tuple, name: str = "Array") -> str:
        string = name + ":\n"
        for i in iterable:
            string += "\t" + str(i)
        return string + "\n"

    @LoggerDecorator
    def log_dict(self, json: dict, name: str = "json") -> str:
        def pprint_json(json: dict | list) -> str:
            if isinstance(json, dict):
                string = "{\n"
                for key, value in json:
                    if not isinstance(value, dict):
                        string += f"\t{key}: {value}\n"
                    else:
                        string += f"\t{key}: {pprint_json(value)}\n"
                string += "}"
            elif isinstance(json, list):
                string = "[\n"
                for i in json:
                    string += f"\t{i},\n"
                string = "]"
            return string

        string = name + ":\n"
        string += pprint_json(json=json)
        return string

    @LoggerDecorator
    def log_object(self, obj: object) -> str:
        return str(obj)
