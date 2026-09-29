"""
Mediator pattern - standalone example
========================================

Scenario: a simplified chat room. Users (colleagues) never reference each
other directly -- they only know about the ChatRoom (mediator). When a
user sends a message, the mediator decides how to distribute it to the
other participants. This keeps User objects simple and decoupled: adding,
removing, or muting a participant only requires changes in the mediator.

Run directly:
    python3 mediator.py
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, List


# ---- Mediator interface --------------------------------------------------

class ChatMediator(ABC):
    @abstractmethod
    def send(self, message: str, sender: "User") -> None:
        ...

    @abstractmethod
    def register(self, user: "User") -> None:
        ...


# ---- Colleague ------------------------------------------------------------

class User:
    """Colleagues only ever talk to the mediator, never to each other
    directly."""

    def __init__(self, name: str, mediator: ChatMediator) -> None:
        self.name = name
        self._mediator = mediator
        self._mediator.register(self)
        self.inbox: List[str] = []

    def send(self, message: str) -> None:
        print(f"  {self.name} sends: \"{message}\"")
        self._mediator.send(message, self)

    def receive(self, message: str, sender_name: str) -> None:
        formatted = f"[{self.name} received] {sender_name}: \"{message}\""
        self.inbox.append(formatted)
        print(f"    -> {formatted}")


# ---- Concrete mediator -------------------------------------------------

class ChatRoom(ChatMediator):
    """Centralizes coordination: knows about every user and decides how
    a message gets distributed (here: broadcast to everyone except the
    sender, skipping muted users)."""

    def __init__(self) -> None:
        self._users: Dict[str, User] = {}
        self._muted: set = set()

    def register(self, user: "User") -> None:
        self._users[user.name] = user

    def mute(self, name: str) -> None:
        self._muted.add(name)

    def send(self, message: str, sender: "User") -> None:
        for name, user in self._users.items():
            if user is sender:
                continue
            if name in self._muted:
                continue  # coordination logic lives HERE, not in User
            user.receive(message, sender.name)


def main() -> None:
    print("=== Mediator demo ===\n")

    chat_room = ChatRoom()

    alice = User("Alice", chat_room)
    bob = User("Bob", chat_room)
    carol = User("Carol", chat_room)

    print("-- Alice sends a message; Bob and Carol both receive it --")
    alice.send("Hey everyone, meeting at 3pm!")

    print("\n-- Muting Carol via the mediator (User objects are untouched) --")
    chat_room.mute("Carol")

    print("\n-- Bob sends a message; only Alice receives it now --")
    bob.send("Sounds good, see you then.")

    print("\n--- users never hold references to each other, only to the mediator ---")
    print(f"Alice's inbox: {alice.inbox}")
    print(f"Bob's inbox:   {bob.inbox}")
    print(f"Carol's inbox: {carol.inbox}  (only has Alice's message; "
          f"muted before Bob's message, so it never reached her)")


if __name__ == "__main__":
    main()
