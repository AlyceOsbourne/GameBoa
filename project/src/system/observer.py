from functools import wraps
from weakref import WeakValueDictionary
from typing import Any, Callable, Hashable


class Observer:
    observed_collection: WeakValueDictionary = WeakValueDictionary()

    @classmethod
    def observe(cls, observed_key: Hashable, observed_function: Callable) -> None:
        cls.observed_collection[observed_key] = observed_function

    @classmethod
    def observable(cls, observable_key: Hashable) -> Callable:
        @wraps
        def decorator(observable_function: Callable) -> Callable:
            cls.observe(observable_key, observable_function)
            return observable_function

        return decorator

    def request_observation(self, requested_key: str, *args, **kwargs) -> Any:
        if requested_key in self.observed_collection:
            return self.observed_collection[requested_key](*args, **kwargs)

        raise KeyError(f"No observer found for key {requested_key}.")
