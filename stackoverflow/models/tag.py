"""
models/tag.py
-------------
Tag assigned to a Question for categorization and search.
"""

class Tag:
    def __init__(self, tag_id: str, topic_name: str):
        self.tag_id = tag_id
        self.topic_name = topic_name

    def get_id(self) -> str:
        return self.tag_id

    def get_topic(self) -> str:
        return self.topic_name

    def __repr__(self) -> str:
        return f"Tag({self.topic_name})"
