"""
Singleton pattern - standalone example
========================================

Scenario: an application-wide configuration manager. No matter where in
the code we ask for the configuration, we must get back the exact same
object, and the (expensive) act of "loading" the configuration should only
happen once.

Run directly:
    python3 singleton.py
"""

from __future__ import annotations

import threading
from typing import Any, Dict, Optional


class ConfigManager:
    """A thread-safe Singleton implemented via __new__.

    The first call to ConfigManager() creates the instance and loads the
    configuration. Every subsequent call returns that same instance
    without re-running the (simulated) expensive load.
    """

    _instance: Optional["ConfigManager"] = None
    _lock: threading.Lock = threading.Lock()

    def __new__(cls, *args: Any, **kwargs: Any) -> "ConfigManager":
        # Double-checked locking: avoid grabbing the lock on the common
        # path where the instance already exists.
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:  # check again inside the lock
                    instance = super().__new__(cls)
                    instance._initialized = False
                    cls._instance = instance
        return cls._instance

    def __init__(self, source: str = "default.cfg") -> None:
        # __init__ runs every time ConfigManager(...) is called, even
        # though __new__ returns the same object, so we guard against
        # re-initializing an already-configured instance.
        if self._initialized:
            return
        print(f"[ConfigManager] loading configuration from '{source}' "
              f"(this should only print once)")
        self._settings: Dict[str, Any] = {
            "source": source,
            "debug": False,
            "max_connections": 10,
        }
        self._initialized = True

    def get(self, key: str) -> Any:
        return self._settings.get(key)

    def set(self, key: str, value: Any) -> None:
        self._settings[key] = value

    def __repr__(self) -> str:
        return f"ConfigManager(id={id(self)}, settings={self._settings})"


def worker(name: str, results: Dict[str, int]) -> None:
    """Simulate several parts of an application asking for the config."""
    config = ConfigManager(source="ignored_after_first_call.cfg")
    results[name] = id(config)


def main() -> None:
    print("=== Singleton demo ===\n")

    # Even though we pass a different "source" the second time, the
    # constructor logic that actually loads data only runs once.
    config_a = ConfigManager(source="app.cfg")
    config_b = ConfigManager(source="this_argument_is_ignored.cfg")

    print(f"\nconfig_a is config_b: {config_a is config_b}")
    print(f"id(config_a) == id(config_b): {id(config_a) == id(config_b)}")

    config_a.set("debug", True)
    print(f"\nconfig_b.get('debug') -> {config_b.get('debug')}  "
          f"(changed through config_a, visible through config_b)")

    # Demonstrate the singleton holds up across threads too.
    print("\n--- verifying the same instance is returned across threads ---")
    results: Dict[str, int] = {}
    threads = [
        threading.Thread(target=worker, args=(f"thread-{i}", results))
        for i in range(5)
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    unique_ids = set(results.values())
    print(f"Object ids seen from {len(threads)} threads: {results}")
    assert len(unique_ids) == 1, "Multiple instances were created!"
    print("All threads received the exact same ConfigManager instance.")


if __name__ == "__main__":
    main()
