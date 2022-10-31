import inspect
from collections import deque
from enum import IntFlag
from enum import auto, Flag
from itertools import count
from typing import Any, Callable, Hashable
from typing import Dict, List
from weakref import WeakValueDictionary

event_ids = count()


class Priority(IntFlag):
    CRITICAL = auto()
    URGENT = auto()
    MEDIUM = auto()
    LOWEST = auto()
    LOW = auto()


class Event(Flag):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return next(event_ids)

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

broadcasts: Callbacks = dict()
allowed_requests: WeakValueDictionary = WeakValueDictionary()

event_queue = deque()

def update():
    if event_queue:
        callback, args, kwargs = event_queue.popleft()
        callback(*args, **kwargs)

def broadcast(event: Hashable, *args, **kwargs):
    for priority in Priority:
        for func in broadcasts.get(event, {}).get(priority, []):
            func(*args, **kwargs)

def subscribe(event: Hashable, callback: Callback, priority: Priority = Priority.MEDIUM):
    broadcasts.setdefault(event, {}).setdefault(priority, []).append(callback)

def subscribes_to(event: Hashable, priority: Priority = Priority.MEDIUM) -> Callable:
    def decorator(f):
        subscribe(event, f, priority)
        return f
    return decorator

def allow_requests(observed_key: Hashable, observed_function: Callable) -> None:
    allowed_requests[observed_key] = observed_function

def allows_requests(observable_key: Hashable) -> Callable:
    return lambda f: allow_requests(observable_key, f) or f

def request_data(event: Hashable, *args, **kwargs) -> Any:
    if event in allowed_requests:
        return allowed_requests[event](*args, **kwargs)
    else:
        raise ValueError(f"Event {event} not allowed to be requested")

__all__ = [
    "Event", "SystemEvents", "GuiEvents", "ComponentEvents", "Priority",
    "broadcast", "subscribe", "subscribes_to", "allow_requests",
    "allows_requests", "request_data",
]
