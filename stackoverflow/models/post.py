"""
models/post.py
--------------
Abstract Base Class for Question and Answer.
Handles shared behavior: content, comments, votes, and authors.
"""

from abc import ABC
from datetime import datetime
from typing import List

from models.user import User
from models.vote import Vote, VoteType
from models.comment import Comment

class Post(ABC):
    def __init__(self, post_id: str, user: User, content: str):
        if not content.strip():
            raise ValueError("Post content cannot be empty.")

        self.post_id = post_id
        self.user = user
        self.content = content
        self.votes: List[Vote] = []
        self.comments: List[Comment] = []
        self.created_date = datetime.now()

    def vote(self, user: User, vote_type: VoteType, apply_rep_fn, revert_rep_fn) -> str:
        """
        Business rules enforced here:
        1. A user cannot vote on their own post.
        2. A user can vote only once per post.
        3. If the same user votes again, we update the existing vote.
        4. Reputation of the post author changes based on the vote.
        """
        if user.get_id() == self.user.get_id():
            return "Users cannot vote on their own posts."

        for existing_vote in self.votes:
            if user.get_id() == existing_vote.get_voter().get_id():
                old_vote_type = existing_vote.vote_type
                if old_vote_type == vote_type:
                    return "User has already cast the same vote."

                # revert previous reputation effect
                revert_rep_fn(self.user, old_vote_type, type(self))

                # apply new vote
                existing_vote.vote_type = vote_type
                apply_rep_fn(self.user, vote_type, type(self))
                return "Vote Updated"

        new_vote = Vote(user=user, vote_type=vote_type)
        self.votes.append(new_vote)
        apply_rep_fn(self.user, vote_type, type(self))
        return "Vote Added"

    def add_comment(self, comment: Comment) -> None:
        self.comments.append(comment)

    def get_score(self) -> int:
        """
        Interview note:
        score = upvotes - downvotes
        NOT simply number of votes.
        """
        score = 0
        for vote in self.votes:
            if vote.vote_type == VoteType.UP_VOTE:
                score += 1
            else:
                score -= 1
        return score

    def get_content(self) -> str:
        return self.content
