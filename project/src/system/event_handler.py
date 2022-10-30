from enum import auto, IntFlag
from queue import Queue
from typing import Any, Callable, Dict, List, Tuple, Hashable


Event = Any
Callback = Callable[..., Any]
CallbackList = List[Tuple[int, Callback]]
Callbacks = Dict[Hashable, CallbackList]


class Priority(IntFlag):
    LOW = auto()
    LOWEST = auto()
    MEDIUM = auto()
    URGENT = auto()
    CRITICAL = auto()


class EventHandler:
    publisher_subscribers: Callbacks = dict()

    @classmethod
    def register(cls, event: Event):
        return cls.publisher_subscribers.setdefault(event, [])

    @classmethod
    def subscribe(
        cls, event: Event, callback: Callback, priority: Priority = Priority.MEDIUM
    ) -> None:
        subs = cls.register(event)
        subs.append((priority, callback))
        subs.sort(key=lambda x: x[0], reverse=True)

    @classmethod
    def publish(cls, event: Event, *args, **kwargs) -> None:
        if event in cls.publisher_subscribers:
            subs = cls.publisher_subscribers[event]
            for _, callback in subs:
                callback(*args, **kwargs)

    @classmethod
    def unsubscribe(cls, event: Event, callback: Callback) -> None:
        if event in cls.publisher_subscribers:
            cls.publisher_subscribers[event] = [
                x for x in cls.publisher_subscribers[event] if x[1] != callback
            ]

    @classmethod
    def subscriber(cls, event: Event, priority: Priority = Priority.MEDIUM) -> Callable:
        def decorator(func: Callable) -> Callable:
            cls.subscribe(event, func, priority)
            return func

        return decorator







