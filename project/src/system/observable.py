# we want a class that lets us look at values that have been registered to it, such as memory addresses or registers
import weakref
from typing import Callable


class Observer:
    observed: dict[str: Callable] = weakref.WeakValueDictionary()

    @classmethod
    def observe(cls, key: str, observed_func: Callable):
        cls.observed[key] = observed_func

    @classmethod
    def observable(cls, key):
        def decorator(func):
            cls.observe(key, func)
            return func
        return decorator

    def request_observation(self, key: str, *args, **kwargs):
        if key in self.observed:
            return self.observed[key](*args, **kwargs)
        else:
            raise KeyError(f'No observer found for key: {key}')

