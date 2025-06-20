import threading
from contextlib import contextmanager


class KeyedMemoryLockManager:
    def __init__(self) -> None:
        self.locks: dict[str, threading.Lock] = {}
        self.global_lock = threading.Lock()

    def _get_lock(self, key: str):
        with self.global_lock:
            if key not in self.locks:
                self.locks[key] = threading.Lock()
            return self.locks[key]

    @contextmanager
    def lock(self, key: str):
        lock = self._get_lock(key)
        lock.acquire()
        try:
            yield
        finally:
            lock.release()
