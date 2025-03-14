"""Module containing the WrongTypeError class"""

from .custom_exception import CustomException

class WrongTypeError(CustomException):
    """Exception raised when a value wasn't of an expected type"""

    def __init__(self, *args, **kwargs):
        if args and isinstance(args[0], tuple):
            super().__init__(f"Expected {args[0][1]}, received {type(args[0][0])}", *args[1::], **kwargs)
        else:
            super().__init__(*args, **kwargs)

    default_message = "Received an unexpected type"
