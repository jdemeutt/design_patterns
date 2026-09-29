"""
Abstract Factory pattern - standalone example
================================================

Scenario: a cross-platform-style UI toolkit that must render a consistent
family of widgets (Button + Checkbox) for either a "Light" theme or a
"Dark" theme. Client code (`Application`) never references a concrete
widget class -- it only talks to the abstract factory and abstract
products, so switching themes never risks mixing mismatched widgets.

Run directly:
    python3 abstract_factory.py
"""

from __future__ import annotations

from abc import ABC, abstractmethod


# ---- Abstract products --------------------------------------------------

class Button(ABC):
    @abstractmethod
    def render(self) -> str:
        ...


class Checkbox(ABC):
    @abstractmethod
    def render(self) -> str:
        ...


# ---- Concrete products: Light family -------------------------------

class LightButton(Button):
    def render(self) -> str:
        return "[ Light Button: white background, black text ]"


class LightCheckbox(Checkbox):
    def render(self) -> str:
        return "[ Light Checkbox: white box, grey border ]"


# ---- Concrete products: Dark family ---------------------------------

class DarkButton(Button):
    def render(self) -> str:
        return "[ Dark Button: black background, white text ]"


class DarkCheckbox(Checkbox):
    def render(self) -> str:
        return "[ Dark Checkbox: dark grey box, white border ]"


# ---- Abstract factory ------------------------------------------------

class WidgetFactory(ABC):
    @abstractmethod
    def create_button(self) -> Button:
        ...

    @abstractmethod
    def create_checkbox(self) -> Checkbox:
        ...


class LightThemeFactory(WidgetFactory):
    def create_button(self) -> Button:
        return LightButton()

    def create_checkbox(self) -> Checkbox:
        return LightCheckbox()


class DarkThemeFactory(WidgetFactory):
    def create_button(self) -> Button:
        return DarkButton()

    def create_checkbox(self) -> Checkbox:
        return DarkCheckbox()


# ---- Client code -------------------------------------------------------

class Application:
    """Client code depends only on the abstract factory / products, so it
    has no idea whether it's running Light or Dark widgets."""

    def __init__(self, factory: WidgetFactory) -> None:
        self._button = factory.create_button()
        self._checkbox = factory.create_checkbox()

    def render_ui(self) -> None:
        print(self._button.render())
        print(self._checkbox.render())


def main() -> None:
    print("=== Abstract Factory demo ===\n")

    print("Rendering with the Light theme family:")
    Application(LightThemeFactory()).render_ui()

    print("\nRendering with the Dark theme family:")
    Application(DarkThemeFactory()).render_ui()

    print("\n--- choosing the family at runtime, e.g. from user settings ---")
    user_prefers_dark_mode = True
    factory: WidgetFactory = DarkThemeFactory() if user_prefers_dark_mode else LightThemeFactory()
    print(f"Selected factory: {factory.__class__.__name__}")
    Application(factory).render_ui()


if __name__ == "__main__":
    main()
