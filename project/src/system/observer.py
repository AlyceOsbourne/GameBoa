from weakref import WeakValueDictionary
from functools import wraps
from typing import Any, Callable, Hashable


class Observer:
    observed_collection: WeakValueDictionary = WeakValueDictionary()

    @classmethod
    def observe(cls, observed_key: Hashable, observed_function: Callable) -> None:
        cls.observed_collection[observed_key] = observed_function

    @classmethod
    def observable(cls, observable_key: Hashable) -> Callable:
        def decorator(func: Callable) -> Callable:
            cls.observe(observable_key, func)
            return func
        return decorator

    @classmethod
    def peep(cls, requested_key: Hashable, *args, **kwargs) -> Any:
        if requested_key in cls.observed_collection:
            return cls.observed_collection[requested_key](*args, **kwargs)
        raise KeyError(f"No observer found for key {requested_key}.")

