from .gb_logger import logger
from enum import IntFlag
from typing import Callable, Any, List, Tuple, Dict
Event = Any
Callback = Callable[..., Any]
CallbackList = List[Tuple[int, Callback]]
Callbacks = Dict[Any, CallbackList]

class Priority(IntFlag):
    LOWEST = 0
    LOW = 1
    MEDIUM = 2
    URGENT = 3
    CRITICAL = 4

class EventHandler:
    publisher_subscribers: Callbacks = dict()

    @classmethod
    def register(cls, event: Event):
        logger.debug(f"Registering event {event}")
        return cls.publisher_subscribers.setdefault(event, [])

    @classmethod
    def subscribe(cls, event: Event, callback: Callback, priority: Priority = Priority.MEDIUM) -> None:
        subs = cls.register(event)
        subs.append((priority, callback))
        subs.sort(key=lambda x: x[0], reverse=True)

    @classmethod
    def publish(cls, event: Event, *args, **kwargs) -> None:
        logger.debug(f"Publishing event {event}")
        if event in cls.publisher_subscribers:
            subs = cls.publisher_subscribers[event]
            for _, callback in subs:
                callback(*args, **kwargs)


    @classmethod
    def unsubscribe(cls, event: Event, callback: Callback) -> None:
        logger.debug(f"Unsubscribing event {event}")
        if event in cls.publisher_subscribers:
            cls.publisher_subscribers[event] = [x for x in cls.publisher_subscribers[event] if x[1] != callback]

    @classmethod
    def subscriber(cls, event: Event, priority: Priority = Priority.MEDIUM) -> Callable:
        def decorator(func: Callable) -> Callable:
            cls.subscribe(event, func, priority)
            return func
        return decorator

