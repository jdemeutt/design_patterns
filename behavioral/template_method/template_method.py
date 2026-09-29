"""
Template Method pattern - standalone example
===============================================

Scenario: a data-import pipeline. Every importer follows the exact same
fixed sequence -- open source, parse records, validate, save, close
source -- but HOW parsing and validation work differs between a CSV-style
importer and a JSON-style importer. The overall sequence lives in exactly
one place (DataImporter.run()), which subclasses cannot reorder or skip;
they only override the specific steps that vary. An optional "hook" step
(after_save) has a default no-op implementation that subclasses may
override if they need it.

Run directly:
    python3 template_method.py
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List


class DataImporter(ABC):
    """AbstractClass: defines the algorithm's fixed skeleton."""

    def run(self, source_name: str) -> None:
        """The template method. Not meant to be overridden -- it fixes
        the order of steps for every subclass."""
        print(f"\n--- Running {self.__class__.__name__} on '{source_name}' ---")
        raw_data = self.open_source(source_name)
        records = self.parse(raw_data)
        valid_records = self.validate(records)
        self.save(valid_records)
        self.after_save(valid_records)  # optional hook
        print(f"--- Import finished: {len(valid_records)} record(s) saved ---")

    def open_source(self, source_name: str) -> str:
        # A step with a sensible default -- subclasses MAY override,
        # but most won't need to.
        print(f"  [open_source] opening '{source_name}'")
        return f"<raw contents of {source_name}>"

    @abstractmethod
    def parse(self, raw_data: str) -> List[dict]:
        """Abstract step: subclasses MUST implement this."""
        ...

    @abstractmethod
    def validate(self, records: List[dict]) -> List[dict]:
        """Abstract step: subclasses MUST implement this."""
        ...

    def save(self, records: List[dict]) -> None:
        # Shared, non-varying step: every importer saves the same way.
        print(f"  [save] writing {len(records)} record(s) to the database")

    def after_save(self, records: List[dict]) -> None:
        """Hook: optional extension point with a no-op default.
        Subclasses may override this if they need extra behavior, but
        don't have to."""
        pass


class CsvImporter(DataImporter):
    def parse(self, raw_data: str) -> List[dict]:
        print("  [parse] splitting rows by comma (CSV-style)")
        return [{"id": 1, "name": "Alice"}, {"id": 2, "name": ""}, {"id": 3, "name": "Bob"}]

    def validate(self, records: List[dict]) -> List[dict]:
        print("  [validate] dropping rows with an empty 'name' field")
        return [r for r in records if r.get("name")]


class JsonImporter(DataImporter):
    def parse(self, raw_data: str) -> List[dict]:
        print("  [parse] decoding as JSON array of objects")
        return [{"id": 10, "email": "a@example.com"},
                {"id": 11, "email": "not-an-email"},
                {"id": 12, "email": "b@example.com"}]

    def validate(self, records: List[dict]) -> List[dict]:
        print("  [validate] keeping only records with a valid-looking email")
        return [r for r in records if "@" in r.get("email", "") and "." in r.get("email", "")]

    def after_save(self, records: List[dict]) -> None:
        # This importer DOES use the optional hook.
        print(f"  [after_save] sending a notification: {len(records)} JSON "
              f"record(s) imported")


def main() -> None:
    print("=== Template Method demo ===")

    CsvImporter().run("customers.csv")
    JsonImporter().run("customers.json")

    print("\n--- both importers followed the EXACT SAME step order ---")
    print("(open_source -> parse -> validate -> save -> after_save), "
          "defined once in DataImporter.run()")


if __name__ == "__main__":
    main()
