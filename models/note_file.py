from dataclasses import dataclass
from datetime import datetime


@dataclass
class NoteFile:
    id: str
    title: str
    name: str
    # content: str
    created_date: datetime
    updated_date: datetime
    topic: str
    tags: list
    next_review: datetime


