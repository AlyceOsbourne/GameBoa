import timeit

# timeit decorator
def timeit_decorator(func):
    def wrapper(*args, **kwargs):
        start = timeit.default_timer()
        result = func(*args, **kwargs)
        end = timeit.default_timer()
        print(f"Time taken by {func.__name__}: {end - start} seconds")
        return result
    return wrapper