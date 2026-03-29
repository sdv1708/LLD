"""
models/user.py
--------------
User entity. Keeps track of an individual user's profile and reputation.
"""

class User:
    def __init__(self, id: str, name: str, email: str, reputation: int = 0):
        self.id = id
        self.name = name
        self.email = email
        self.reputation = reputation

    def get_id(self) -> str:
        return self.id

    def get_name(self) -> str:
        return self.name

    def get_reputation(self) -> int:
        return self.reputation

    def update_reputation(self, rep_change: int) -> None:
        self.reputation += rep_change

    def __repr__(self) -> str:
        return f"User(id={self.id}, name={self.name}, rep={self.reputation})"
