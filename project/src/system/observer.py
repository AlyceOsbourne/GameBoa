# we want a class that lets us look at values that have been registered to it, such as memory addresses or registers
import weakref
from typing import Callable


class Observer:
    observed: weakref.WeakKeyDictionary = weakref.WeakKeyDictionary()

    @classmethod
    def observe(cls, key: object, observed_func: Callable):
        cls.observed[key] = observed_func

    @classmethod
    def observable(cls, key):
        def decorator(func):
            cls.observe(key, func)
            return func
        return decorator

    def request_observation(self, key: object, *args, **kwargs):
        if key in self.observed:
            return self.observed[key](*args, **kwargs)
        else:
            raise KeyError(f'No observer found for key: {key}')



