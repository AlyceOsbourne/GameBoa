# we want a class that lets us look at values that have been registered to it, such as memory addresses or registers
import weakref
from functools import wraps
from typing import Callable, Hashable


class Observer:
    observed: weakref.WeakKeyDictionary = weakref.WeakKeyDictionary()

    @classmethod
    def observe(cls, key: Hashable, observed_func: Callable):
        cls.observed[key] = observed_func

    @classmethod
    def observable(cls, key: Hashable):
        def decorator(func: Callable):
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            cls.observe(key, wrapper)
            return wrapper
        return decorator

    @classmethod
    def peep(cls, key: Hashable, *args, **kwargs):
        if key in cls.observed:
            return cls.observed[key](*args, **kwargs)
        else:
            raise KeyError(f"Key {key} not found in observed.")


