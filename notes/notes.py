from datetime import datetime

from models.note_file import NoteFile
from services.drive_service import get_folder_docs
from spaced_repetition_system.srs import get_next_review


def get_notes(service):
    folder_docs_metadata = get_folder_docs(service)
    return [create_note_file(file) for file in folder_docs_metadata]


def create_note_file(doc_metadata):
    name, topic, tags = extract_metadata_from_title(doc_metadata['name'])
    created_date = convert_string_to_date(doc_metadata['createdTime'])
    updated_date = convert_string_to_date(doc_metadata['modifiedTime'])
    return NoteFile(doc_metadata['id'],
                    title=doc_metadata['name'],
                    name=name,
                    created_date=created_date,
                    updated_date=updated_date,
                    topic=topic,
                    tags=tags,
                    next_review=get_next_review(updated_date))


def extract_metadata_from_title(file_title):
    title_parts = file_title.split(' ')
    topic = title_parts[0].replace('@', '').replace(':', '') if title_parts[0].startswith('@') else None
    tags = [x.replace('#', '') for x in title_parts if x.startswith('#')]
    name = ' '.join([x for x in title_parts if not x.startswith('#') and not x.startswith('@')])
    return name, topic, tags


def convert_string_to_date(string):
    return datetime.strptime(string, '%Y-%m-%dT%H:%M:%S.%fZ')