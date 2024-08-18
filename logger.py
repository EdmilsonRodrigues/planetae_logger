from datetime import datetime
from typing import Any


class _LoggerDecorator:
    def __init__(self, cls) -> None:
        self.cls = cls

    def __call__(self, *args, **kwargs) -> Any:
        instance = self.cls(*args, **kwargs)
        for method in self.cls.__dict__:
            if callable(getattr(self.cls, method)):
                instance.__dict__[method] = self._decorate(getattr(self.cls, method), standard_output=instance.standard_output, exception_output=instance.exceptions_output)
        return instance

    def _decorate(self, func: Any, standard_output: str, exception_output: str) -> Any:
        def wrapper(*args, **kwargs) -> Any:
            try:
                result = func(*args, **kwargs)
                self._log_output(result, filename=standard_output)
                return result
            except Exception as e:
                self._log_output(e, filename=exception_output)

        return wrapper

    @staticmethod
    def _log_output(output: Any, filename: str) -> None:
        with open(filename, "a") as log_file:
            log_file.write(str(output) + " " + datetime.now().isoformat() + " " + "\n")


@_LoggerDecorator
class Logger:
    """
    A class for creating a logger instance

    This class provides methods to log exceptions, strings, iterables, dictionaries,
    and objects. The logs are stored in specified output strings.
    """
    standard_output: str
    exceptions_output: str

    def __init__(self, standard_output: str, exceptions_output: str) -> None:
        """
        Initialise a logger instance

        :param standard_output: The output destination for standard logs.
        :type standard_output: str
        :param exceptions_output: The output destination for exception logs.
        :type exceptions_output: str
        """
        self.standard_output = standard_output
        self.exceptions_output = exceptions_output

    @staticmethod
    def log_exception(exception: Exception) -> None:
        """
        Logs an exception to the output destination

        :param exception: The exception to be logged.
        :type exception: Exception
        """
        raise exception

    @staticmethod
    def log_string(string: str) -> str:
        """
        Logs a string to the output destination and returns it

        :param string: The string to be logged.
        :type string: str
        :return: The logged string.
        :rtype: str
        """
        return string

    @staticmethod
    def log_iterable(iterable: list | tuple, name: str = "Array") -> str:
        """
        logs an iterable to the output destination and returns its string
        :param iterable: The iterable to be logged.
        :type iterable: list | tuple
        :param name: The name of the iterable to be logged.
        :type name: str
        :return: The logged iterable.
        :rtype: str
        """
        string = name + ":\n"
        for i in iterable:
            string += "\t" + str(i)
        return string + "\n"

    @staticmethod
    def log_dict(json: dict, name: str = "json") -> str:
        """
        Logs a dictionary to the output destination and returns its string

        :param json: The dictionary to be logged.
        :type json: dict
        :param name: The name of the dictionary to be logged.
        :type name: str
        :return: The logged dictionary.
        :rtype: str

        """
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
    def log_object(obj: object) -> str:
        """
        Logs an object to the output destination and returns its string
        :param obj: The object to be logged.
        :type obj: object
        :return: The logged object.
        :rtype: str
        """
        return str(obj)
