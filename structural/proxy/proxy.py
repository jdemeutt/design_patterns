"""
Proxy pattern - standalone example
=====================================

Two proxies over the same Subject interface, both drop-in substitutes for
a RealImage:

1. VirtualProxyImage -- defers the (simulated) expensive loading of an
   image from disk until display() is actually called for the first time.
2. ProtectionProxyImage -- wraps a VirtualProxyImage and only allows
   display() if the caller has the right permission.

Run directly:
    python3 proxy.py
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional


# ---- Subject interface --------------------------------------------------

class Image(ABC):
    @abstractmethod
    def display(self) -> str:
        ...


# ---- Real subject (expensive to create) --------------------------------

class RealImage(Image):
    def __init__(self, filename: str) -> None:
        self.filename = filename
        self._load_from_disk()

    def _load_from_disk(self) -> None:
        print(f"  [RealImage] loading '{self.filename}' from disk (expensive!)")

    def display(self) -> str:
        return f"Displaying '{self.filename}'"


# ---- Virtual proxy: lazy loading ----------------------------------------

class VirtualProxyImage(Image):
    """Looks exactly like an Image to client code, but doesn't create the
    expensive RealImage until display() is actually called."""

    def __init__(self, filename: str) -> None:
        self.filename = filename
        self._real_image: Optional[RealImage] = None

    def display(self) -> str:
        if self._real_image is None:
            print(f"  [VirtualProxyImage] first access for '{self.filename}' "
                  f"-> creating the real image now")
            self._real_image = RealImage(self.filename)
        else:
            print(f"  [VirtualProxyImage] reusing already-loaded '{self.filename}'")
        return self._real_image.display()


# ---- Protection proxy: access control -----------------------------------

class ProtectionProxyImage(Image):
    """Wraps another Image (often a VirtualProxyImage) and only forwards
    display() calls if the caller is authorized."""

    def __init__(self, image: Image, user_role: str) -> None:
        self._image = image
        self._user_role = user_role

    def display(self) -> str:
        if self._user_role not in ("admin", "editor"):
            return (f"Access denied: role '{self._user_role}' may not view "
                    f"this image.")
        return self._image.display()


def main() -> None:
    print("=== Proxy demo ===\n")

    print("-- Virtual proxy: expensive load deferred until first display() --")
    gallery = [
        VirtualProxyImage("vacation.png"),
        VirtualProxyImage("wedding.png"),
    ]
    print("Gallery created (no images actually loaded yet).\n")

    print("Now displaying the first image (twice):")
    print(f"  -> {gallery[0].display()}")
    print(f"  -> {gallery[0].display()}  (cached, no reload)\n")

    print("-- Protection proxy: access control layered on top --")
    admin_view = ProtectionProxyImage(VirtualProxyImage("salary_data.png"), user_role="admin")
    guest_view = ProtectionProxyImage(VirtualProxyImage("salary_data.png"), user_role="guest")

    print(f"Admin: {admin_view.display()}")
    print(f"Guest: {guest_view.display()}")

    print("\n--- client code uses RealImage, VirtualProxyImage, and "
          "ProtectionProxyImage completely interchangeably ---")

    def render(image: Image) -> None:
        print(f"  render() -> {image.display()}")

    render(RealImage("direct.png"))
    render(VirtualProxyImage("lazy.png"))
    render(ProtectionProxyImage(VirtualProxyImage("secure.png"), user_role="editor"))


if __name__ == "__main__":
    main()
