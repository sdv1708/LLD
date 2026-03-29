"""
models/vote.py
--------------
Vote and VoteType representing an upvote or downvote cast by a user.
"""

from enum import Enum
from models.user import User


class VoteType(Enum):
    UP_VOTE = "upvote"
    DOWN_VOTE = "downvote"


class Vote:
    def __init__(self, user: User, vote_type: VoteType):
        self.user = user
        self.vote_type = vote_type

    def get_voter(self) -> User:
        return self.user

    def get_type(self) -> str:
        return self.vote_type.value
