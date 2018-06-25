import threading
import time
from collections import deque


class Event:
    def __init__(self, command: str, **params):
        self.command = command
        self.params = params
        self.is_global = params.get('is_global', True)

    def __eq__(self, other):
        if isinstance(other, Event):
            return self.command == other.command

        return self.command == other

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return self.command

    def __repr__(self):
        return 'Event:[{}, p={}]'.format(self.command, self.params)


class EventQueue:
    def __init__(self, name=None):
        self._queue = deque([])
        self.name = name

    def __iter__(self):
        return iter(self._queue)

    def __len__(self):
        return len(self._queue)

    def __getitem__(self, item):
        return self._queue[item]

    def register(self, event: Event):
        if isinstance(event, str):
            event = Event(event)
        self._queue.append(event)

    def __bool__(self):
        return bool(self._queue)

    def available(self):
        return bool(self._queue)

    def pop(self) -> Event:
        return self._queue.popleft()


threads = []
event_queues = []


def thread(func):
    """Decorator to register functions as threads with event queues

    """
    eq = EventQueue(name=func.__name__)  # local event queue

    def decorator(*args, **kwargs):
        func(eq, *args, **kwargs)

    t = threading.Thread(target=decorator, name=func.__name__)
    threads.append(t)
    event_queues.append(eq)

    return decorator


def get_thread(name: str) -> threading.Thread:
    matches = [x for x in threads if x.name == name]
    if matches:
        return matches[0]


def get_event_queue(name: str) -> EventQueue:
    matches = [x for x in event_queues if x.name == name]
    if matches:
        return matches[0]


def start(name: str):
    t = get_thread(name)
    if t:
        t.start()
    else:
        raise ValueError('No thread named `{}` exists!'.format(name))


def start_all():
    for t in threads:
        try:
            t.start()
        except:
            pass


def event(thread_name: str, command: str, **params):
    thread_eq = get_event_queue(thread_name)
    if thread_eq:
        thread_eq.register(Event(command, **params))
    else:
        raise ValueError('No thread named `{}` exists!'.format(thread_name))


def event_all(command, **params):
    params['is_global'] = True
    for eq in event_queues:
        eq.register(Event(command, **params))


def stop(thread_name: str):
    thread_eq = get_event_queue(thread_name)
    if thread_eq:
        thread_eq.register(Event('STOP'))
    else:
        raise ValueError('No thread named `{}` exists!'.format(thread_name))


def stop_all():
    for eq in event_queues:
        eq.register('STOP')


def clear():
    threads.clear()
    event_queues.clear()


class TimerException(Exception):
    pass


def sleep(eq: EventQueue, limit, step_size: float = 1.0):
    i = 0
    while i < limit:
        if eq.available() and eq.pop() == 'STOP':
            raise TimerException
        i += step_size
        time.sleep(step_size)
