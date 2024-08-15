from datetime import datetime
from typing import Any


class _LoggerDecorator:
    def __init__(self, cls) -> None:
        self.cls = cls

    def __call__(self, *args, **kwargs) -> Any:
        instance = self.cls(*args, **kwargs)
        for method in instance:
            if callable(getattr(self.cls, method)):
                self.cls.__dict__[method] = self._decorate(getattr(self.cls, method), standard_output=instance.response_output, exception_output=instance.response_output)
        return

    def _decorate(self, func: Any, standard_output: str, exception_output: str) -> Any:
        def wrapper(*args, **kwargs) -> Any:
            try:
                result = func(*args, **kwargs)
                self._log_output(result, filename=standard_output)
                return result
            except Exception as e:
                self._log_output(result, filename=exception_output)

        return wrapper

    @staticmethod
    def _log_output(output: Any, filename: str) -> None:
        with open(filename, "a") as log_file:
            log_file.write(str(output) + " " + datetime.now().isoformat() + " " + "\n")


@_LoggerDecorator
class Logger:
    standard_output: str
    exceptions_output: str

    def __init__(self, standard_output: str, exceptions_output: str) -> None:
        self.standard_output = standard_output
        self.exceptions_output = exceptions_output

    def log_exception(self, exception: Exception) -> None:
        raise exception

    def log_string(self, string: str) -> str:
        return string

    def log_iterable(self, iterable: list | tuple, name: str = "Array") -> str:
        string = name + ":\n"
        for i in iterable:
            string += "\t" + str(i)
        return string + "\n"

    def log_dict(self, json: dict, name: str = "json") -> str:
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

    def log_object(self, obj: object) -> str:
        return str(obj)
