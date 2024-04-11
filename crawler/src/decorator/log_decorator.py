import functools
import logging
import typing
import time

def log_decorator(func: typing.Callable):
    '''log @Decorator to use in functions not asynchronous'''
    @functools.wraps(func)
    def time_funcao_wrapper(*args, **kwargs):
        start = time.perf_counter()
        print(f"Executing {func.__name__}(), args={args}, kwargs={kwargs}.")
        result = func(*args, **kwargs)
        end = time.perf_counter()
        time_taken = end - start
        logging.info(f'{func.__name__}() executed in {time_taken:.4f} seconds!')
        return result
    return time_funcao_wrapper
