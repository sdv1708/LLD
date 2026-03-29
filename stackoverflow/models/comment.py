"""
models/comment.py
-----------------
Comment entity allowing users to comment on any Post.
"""

from datetime import datetime
from models.user import User


class Comment:
    def __init__(self, comment_id: str, content: str, user: User):
        if not content.strip():
            raise ValueError("Comment content cannot be empty.")

        self.comment_id = comment_id
        self.content = content
        self.user = user
        self.created_date = datetime.now()

    def get_content(self) -> str:
        return self.content

    def get_author(self) -> User:
        return self.user
