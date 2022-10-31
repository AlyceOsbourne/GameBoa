from collections import deque
from enum import IntFlag
from typing import Any, Callable, Hashable
from typing import Dict, List
from weakref import WeakValueDictionary
from enum import auto, Flag
from itertools import count
from .gb_logger import logger
from time import sleep

EVENT_IDS = count()


class Priority(IntFlag):
    LOW = auto()
    LOWEST = auto()
    MEDIUM = auto()
    URGENT = auto()
    CRITICAL = auto()


class Event(Flag):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return next(EVENT_IDS)

    @staticmethod
    def get_all_events():
        return {
            member.name: member
            for subcls in Event.__subclasses__()
            for member in subcls.__members__.values()
        }


class SystemEvents(Event):
    Log = auto()
    Quit = auto()
    ExceptionRaised = auto()
    SettingsUpdated = auto()


class GuiEvents(Event):
    Update = auto()
    OpenAboutDialog = auto()
    UpdateRomLibrary = auto()
    OpenLoadRomDialog = auto()
    LoadRomFromLibrary = auto()
    OpenSettingsDialog = auto()
    RequestMemoryStatus = auto()
    DeleteRomFromLibrary = auto()
    RequestRegistryStatus = auto()


class ComponentEvents(Event):
    RomLoaded = auto()
    RomUnloaded = auto()

    HeaderLoaded = auto()
    RequestReset = auto()

    RequestOpCode = auto()
    RequestDecode = auto()
    RequestExecute = auto()

    RequestMemoryRead = auto()
    RequestMemoryWrite = auto()

    RequestRegisterRead = auto()
    RequestRegisterWrite = auto()


Callback = Callable[..., Any]
CallbackList = List[Callback]
Callbacks = Dict[Hashable, dict[Priority, CallbackList]]

publisher_subscribers: Callbacks = dict()
observed_collection: WeakValueDictionary = WeakValueDictionary()

event_queue = deque()

def broadcast(event: Event, *args, **kwargs) -> None:
    for priority, callback_list in publisher_subscribers.get(event, {}).items():
        for callback in callback_list:
            event_queue.append((callback, args, kwargs))

def subscribe(
        event: Event, callback: Callback, priority: Priority = Priority.MEDIUM
) -> None:
    publisher_subscribers.setdefault(event, {}).setdefault(priority, []).append(callback)


def subscribes_to(event: Event, priority: Priority = Priority.MEDIUM) -> Callable:
    def decorator(func: Callable) -> Callable:
        subscribe(event, func, priority)
        return func

    return decorator

def allow_requests(observed_key: Hashable, observed_function: Callable) -> None:
    observed_collection[observed_key] = observed_function

def allows_requests(observable_key: Hashable) -> Callable:
    return lambda f: allow_requests(observable_key, f) or f

def request_data(requested_key: Hashable, *args, **kwargs) -> Any:
    if requested_key in observed_collection:
        return observed_collection[requested_key](*args, **kwargs)
    raise KeyError(f"No observer found for key {requested_key}.")

subscribe(SystemEvents.Log, logger.debug)
subscribe(SystemEvents.ExceptionRaised, logger.exception)

# we want a event loop that runs in the background in a separate thread
# this will allow us to run the gui in the main thread


def update():
    if event_queue:
        callback, args, kwargs = event_queue.popleft()
        callback(*args, **kwargs)



__all__ = [
    "Event", "SystemEvents", "GuiEvents", "ComponentEvents", "Priority",
    "broadcast", "subscribe", "subscribes_to", "allow_requests",
    "allows_requests", "request_data",
]
