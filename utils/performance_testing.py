import time
import inspect


# decorator for testing the speed of a function
def timeit(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter_ns()
        result = func(*args, **kwargs)
        end = time.perf_counter_ns()
        func_args_as_str = ', '.join([str(arg) for arg in args])
        func_kwargs_as_str = ', '.join([f'{key}={value}' for key, value in kwargs.items()])
        # as seconds
        print(f'{func.__name__}({func_args_as_str}{func_kwargs_as_str}) took {(end - start) * 1e-9:3f} seconds')
        return result

    return wrapper
