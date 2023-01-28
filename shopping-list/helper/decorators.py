from functools import wraps


def separator(func):
    @wraps(func)
    def wrapper_separator():
        print('************************************************')
        func()
        print('************************************************')
    return wrapper_separator
