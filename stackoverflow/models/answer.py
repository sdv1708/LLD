"""
models/answer.py
----------------
Represents an Answer to a specific Question.
Inherits from Post.
"""

from models.post import Post
from models.user import User
from models.question import Question
from models.vote import VoteType
from services.reputation import apply_reputation_for_vote, revert_reputation_for_vote

class Answer(Post):
    def __init__(self, a_id: str, user: User, content: str, question: Question):
        super().__init__(a_id, user, content)
        self.a_id = a_id
        self.question = question
        self.is_accepted = False

    def accept(self) -> None:
        self.is_accepted = True

    def unaccept(self) -> None:
        self.is_accepted = False

    def vote(self, user: User, vote_type: VoteType) -> str:
        return super().vote(user, vote_type, apply_reputation_for_vote, revert_reputation_for_vote)
