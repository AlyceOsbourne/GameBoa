import timeit


def execution_time(function):
    def wrapper(*args, **kwargs):
        start = timeit.default_timer()
        function_result = function(*args, **kwargs)
        end = timeit.default_timer()
        print(f"{function.__name__} took {end - start} seconds")

        return function_result

    return wrapper
