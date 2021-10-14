"""Decorators to be used in this project"""
from functools import wraps

def my_logger(orig_func):
    """log the args & kwargs of a function"""
    import logging
    logging.basicConfig(filename=f"{orig_func.__name__}.log", level=logging.INFO)

    @wraps(orig_func)
    def wrapper(*args, **kwargs):
        logging.info(f"Ran with args: {args} and kwargs: {kwargs}")
        return orig_func(*args, **kwargs)

    return wrapper


def my_timer(orig_func):
    """measure and print the execution time of a function"""
    import time

    @wraps(orig_func)
    def wrapper(*args, **kwargs):
        t1 = time.time()
        result = orig_func(*args, **kwargs)
        t2 = time.time() - t1
        print(f"{orig_func.__name__} ran in: {t2} seconds")
        return result

    return wrapper
