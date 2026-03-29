"""
services/reputation.py
----------------------
Constants and simple helper functions for reputation rules.
"""

from models.vote import VoteType

QUESTION_UPVOTE_REP = 5
ANSWER_UPVOTE_REP = 10
DOWNVOTE_REP = -2
ACCEPTED_ANSWER_REP = 15

def get_reputation_change(vote_type: VoteType, post_type: type) -> int:
    from models.question import Question
    
    if vote_type == VoteType.DOWN_VOTE:
        return DOWNVOTE_REP

    if post_type is Question:
        return QUESTION_UPVOTE_REP
    return ANSWER_UPVOTE_REP

def apply_reputation_for_vote(user, vote_type: VoteType, post_type: type) -> None:
    rep_change = get_reputation_change(vote_type, post_type)
    user.update_reputation(rep_change)

def revert_reputation_for_vote(user, vote_type: VoteType, post_type: type) -> None:
    rep_change = get_reputation_change(vote_type, post_type)
    user.update_reputation(-rep_change)
