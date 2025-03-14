"""Module containing the CustomException class"""

class CustomException(Exception):
    """
    The base class for all custom exceptions
    
    If no arguments are provided at instantiation, the default error message is used
    """

    def __init__(self, *args, **kwargs):
        default_message = type(self).default_message

        if args:
            super().__init__(*args, **kwargs)
        else:
            # exception was raised without args
            super().__init__(default_message, **kwargs)

    default_message = ""
