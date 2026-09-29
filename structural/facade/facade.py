"""
Facade pattern - standalone example
======================================

Scenario: a "home theater" subsystem made of several independent
components (Amplifier, Projector, StreamingPlayer, Lights) that each have
their own, fairly detailed APIs. Watching a movie normally requires
calling several of them in the right order. HomeTheaterFacade exposes one
simple method, watch_movie(), that coordinates all of that -- while the
individual subsystem classes remain fully usable on their own for anyone
who needs finer control.

Run directly:
    python3 facade.py
"""

from __future__ import annotations


# ---- Subsystem classes (each fairly complex/detailed on its own) --------

class Amplifier:
    def on(self) -> None:
        print("  Amplifier: powering on")

    def set_volume(self, level: int) -> None:
        print(f"  Amplifier: setting volume to {level}")

    def off(self) -> None:
        print("  Amplifier: powering off")


class Projector:
    def on(self) -> None:
        print("  Projector: powering on")

    def set_input(self, source: str) -> None:
        print(f"  Projector: switching input to '{source}'")

    def off(self) -> None:
        print("  Projector: powering off")


class StreamingPlayer:
    def on(self) -> None:
        print("  StreamingPlayer: powering on")

    def play(self, title: str) -> None:
        print(f"  StreamingPlayer: now playing '{title}'")

    def stop(self) -> None:
        print("  StreamingPlayer: stopped")

    def off(self) -> None:
        print("  StreamingPlayer: powering off")


class Lights:
    def dim(self, level: int) -> None:
        print(f"  Lights: dimming to {level}%")

    def on(self) -> None:
        print("  Lights: full brightness")


# ---- Facade ------------------------------------------------------------

class HomeTheaterFacade:
    """Coordinates the whole subsystem behind two simple methods."""

    def __init__(
        self,
        amplifier: Amplifier,
        projector: Projector,
        player: StreamingPlayer,
        lights: Lights,
    ) -> None:
        self._amplifier = amplifier
        self._projector = projector
        self._player = player
        self._lights = lights

    def watch_movie(self, title: str) -> None:
        print(f"Getting ready to watch '{title}'...")
        self._lights.dim(10)
        self._projector.on()
        self._projector.set_input("streaming")
        self._amplifier.on()
        self._amplifier.set_volume(15)
        self._player.on()
        self._player.play(title)
        print("Enjoy the movie!\n")

    def end_movie(self) -> None:
        print("Shutting down the home theater...")
        self._player.stop()
        self._player.off()
        self._amplifier.off()
        self._projector.off()
        self._lights.on()
        print("All devices powered down.\n")


def main() -> None:
    print("=== Facade demo ===\n")

    theater = HomeTheaterFacade(
        amplifier=Amplifier(),
        projector=Projector(),
        player=StreamingPlayer(),
        lights=Lights(),
    )

    print("-- Client code using the simplified facade --")
    theater.watch_movie("The Matrix")
    theater.end_movie()

    print("-- Power users can still bypass the facade for fine control --")
    amp = Amplifier()
    amp.on()
    amp.set_volume(25)  # a custom volume the facade's defaults don't offer
    amp.off()


if __name__ == "__main__":
    main()
