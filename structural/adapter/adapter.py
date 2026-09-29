"""
Adapter pattern - standalone example
=======================================

Scenario: our application's reporting code expects any "renderer" to
expose a `render(data: dict) -> str` method. We want to integrate a
third-party XML rendering library whose API is completely different
(`ThirdPartyXmlLibrary.to_xml_document(...)`) and which we are not allowed
to modify. An Adapter bridges the gap.

Run directly:
    python3 adapter.py
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict


# ---- Target interface (what our client code expects) -----------------

class Renderer(ABC):
    @abstractmethod
    def render(self, data: Dict[str, str]) -> str:
        ...


class JsonRenderer(Renderer):
    """A renderer that already matches our expected interface natively."""

    def render(self, data: Dict[str, str]) -> str:
        import json
        return json.dumps(data)


# ---- Adaptee: third-party code we cannot modify ------------------------

class ThirdPartyXmlLibrary:
    """Imagine this ships in a pip package we don't control. Its interface
    has nothing to do with our Renderer.render(data) signature."""

    def to_xml_document(self, tag_name: str, entries: Dict[str, str]) -> str:
        inner = "".join(f"<{k}>{v}</{k}>" for k, v in entries.items())
        return f"<{tag_name}>{inner}</{tag_name}>"


# ---- Adapter -------------------------------------------------------------

class XmlRendererAdapter(Renderer):
    """Adapts ThirdPartyXmlLibrary to the Renderer interface our
    application expects, via composition (the 'object adapter' style)."""

    def __init__(self, xml_library: ThirdPartyXmlLibrary, root_tag: str = "report") -> None:
        self._xml_library = xml_library
        self._root_tag = root_tag

    def render(self, data: Dict[str, str]) -> str:
        # Translate the call into whatever the adaptee actually needs.
        return self._xml_library.to_xml_document(self._root_tag, data)


# ---- Client code ---------------------------------------------------------

def generate_report(renderer: Renderer, data: Dict[str, str]) -> None:
    """Client code only ever depends on the Renderer interface -- it has
    no idea (and doesn't need to know) whether it's talking to a native
    renderer or an adapted third-party library."""
    print(renderer.render(data))


def main() -> None:
    print("=== Adapter demo ===\n")

    data = {"status": "OK", "processed": "42", "errors": "0"}

    print("Using a renderer that already matches our interface:")
    generate_report(JsonRenderer(), data)

    print("\nUsing the incompatible third-party library directly (doesn't fit):")
    third_party = ThirdPartyXmlLibrary()
    print(f"  third_party.to_xml_document('report', data) -> "
          f"{third_party.to_xml_document('report', data)}")
    print("  (Renderer.render(data) is NOT how this library is called)")

    print("\nUsing the same third-party library through an Adapter:")
    adapted_renderer: Renderer = XmlRendererAdapter(third_party, root_tag="report")
    generate_report(adapted_renderer, data)  # exact same call as JsonRenderer!

    print("\n--- client code (generate_report) never changed between the three cases ---")


if __name__ == "__main__":
    main()
