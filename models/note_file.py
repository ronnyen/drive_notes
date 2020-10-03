from dataclasses import dataclass


@dataclass
class NoteFile:
    id: str
    content: str
    title: str
    created_date: str
    topic: str
    tags: str


