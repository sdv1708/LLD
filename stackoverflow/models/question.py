"""
models/question.py
------------------
Represents a Question in the StackOverflow system.
Inherits from Post and holds answers and tags.
"""

from typing import List, Optional

from models.post import Post
from models.user import User
from models.tag import Tag
from models.vote import VoteType
from services.reputation import apply_reputation_for_vote, revert_reputation_for_vote

# Late import for Answer to avoid circular dependency
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.answer import Answer


class Question(Post):
    def __init__(self, q_id: str, title: str, user: User, content: str, tags: Optional[List[Tag]] = None):
        if not title.strip():
            raise ValueError("Question title cannot be empty.")

        super().__init__(q_id, user, content)
        self.q_id = q_id
        self.title = title
        self.tags: List[Tag] = tags if tags else []
        self.answers: List['Answer'] = []
        self.accepted_answer: Optional['Answer'] = None

    def add_tag(self, tag: Tag) -> None:
        # Prevent duplicate tags by topic name
        for existing_tag in self.tags:
            if existing_tag.get_topic().lower() == tag.get_topic().lower():
                return
        self.tags.append(tag)

    def add_answer(self, answer: 'Answer') -> None:
        if answer.question != self:
            raise ValueError("Answer does not belong to this question.")
        self.answers.append(answer)

    def accept_answer(self, user: User, answer: 'Answer') -> str:
        """
        Business rules:
        1. Only the question author can accept an answer.
        2. The answer must belong to this question.
        3. Only one accepted answer can exist at a time.
        4. Accepted answer gives reputation to answer author.
        """
        from services.reputation import ACCEPTED_ANSWER_REP

        if user.get_id() != self.user.get_id():
            return "Only the question author can accept an answer."

        if answer.question != self:
            return "Cannot accept an answer from another question."

        if answer not in self.answers:
            return "Answer must be added to the question before accepting."

        if self.accepted_answer == answer:
            return "Answer is already accepted."

        # If another answer was already accepted, unaccept it first
        if self.accepted_answer is not None:
            self.accepted_answer.unaccept()
            self.accepted_answer.user.update_reputation(-ACCEPTED_ANSWER_REP)

        self.accepted_answer = answer
        answer.accept()
        answer.user.update_reputation(ACCEPTED_ANSWER_REP)
        return "Answer accepted."

    def vote(self, user: User, vote_type: VoteType) -> str:
        return super().vote(user, vote_type, apply_reputation_for_vote, revert_reputation_for_vote)

