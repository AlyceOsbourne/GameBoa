from enum import IntFlag
from enum import auto, Flag
from itertools import count
from types import FunctionType, MethodType
from typing import Any, Callable, Hashable
from typing import Dict, List


Callback = Callable[..., Any]
CallbackList = List[Callback]
Callbacks = Dict[Hashable, Dict["Priority", CallbackList]]

_event_id_generator = count()

_broadcasts: Callbacks = dict()
_allowed_requests: Dict[Hashable, Callable] = dict()


class Priority(IntFlag):
    CRITICAL = auto()
    URGENT = auto()
    MEDIUM = auto()
    LOWEST = auto()
    LOW = auto()


class Event(Flag):
    @staticmethod
    def _generate_next_value_(*_):
        return next(_event_id_generator)

    def subscribe(self, callback: Callback, priority: Priority = Priority.MEDIUM) -> None:
        subscribe(self, callback, priority)

    def subscribe_to(self, priority: Priority = Priority.MEDIUM):
        return lambda f: self.subscribe(f, priority)

    def emit(self, *args, **kwargs) -> None:
        emit(self, *args, **kwargs)

    def subscribers(self) -> list:
        return _broadcasts.get(self, [])

    def request_data(self, *args, **kwargs) -> Any:
        return request_data(self, *args, **kwargs)

    def allow_requests(self, f: Callable) -> None:
        _allowed_requests.setdefault(self, f)

    def __or__(self, other: object) -> object:
        return self, other

    def __ror__(self, other: object) -> object:
        return other, self

    def __call__(self, v=None, *a, **k):
        if v:
            if isinstance(v, FunctionType) or isinstance(v, MethodType):
                self.subscribe(v)
                return v
            self.emit(v, *a, **k)
        else:
            self.emit(*a, **k)

    @staticmethod
    def get_all_events():
        return {member.name: member for subclass in Event.__subclasses__() for member in subclass.__members__.values()}


class EventGroup(tuple[Event, ...], Flag):
    def subscribe(self, callback, priority=Priority.MEDIUM) -> None:
        for event in self:
            event.subscribe(callback, priority)

    def subscribe_to(self, priority: Priority = Priority.MEDIUM):
        def decorator(f):
            for event in self:
                event.subscribe(f, priority)
            return f

        return decorator

    def emit(self, *args, **kwargs) -> None:
        for event in self:
            event.emit(*args, **kwargs)

    def request_data(self, *args, **kwargs):
        return [event.request_data(*args, **kwargs) for event in self]

    def __call__(self, v, *a, **k):
        if isinstance(v, FunctionType):
            self.subscribe(v)
            return v
        self.emit(v, *a, **k)


def emit(event: Hashable, *args, **kwargs):
    for priority in _broadcasts.get(event, {}).values():
        for callback in priority:
            callback(*args, **kwargs)


def subscribe(event: Hashable, callback: Callback, priority: Priority = Priority.MEDIUM):
    _broadcasts.setdefault(event, {}).setdefault(priority, []).append(callback)


def subscribes_to(event: Hashable, priority: Priority = Priority.MEDIUM) -> Callable:
    def decorator(f):
        subscribe(event, f, priority)
        return f

    return decorator


def allow_requests(observed_key: Hashable, observed_function: Callable) -> None:
    _allowed_requests[observed_key] = observed_function


def allows_requests(observable_key: Hashable) -> Callable:
    return lambda f: allow_requests(observable_key, f) or f


def request_data(event: Hashable, *args, **kwargs) -> Any:
    if event in _allowed_requests:
        return _allowed_requests[event](*args, **kwargs)
    else:
        raise ValueError(f"Event {event} not allowed to be requested")


__all__ = [
    "Event",
    "Priority",
    "emit",
    "subscribe",
    "subscribes_to",
    "allow_requests",
    "allows_requests",
    "request_data",
]
