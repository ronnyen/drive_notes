from index.index import create_index
from notes.notes import get_notes
from services.google_service import create_service


if __name__ == '__main__':
    service = create_service('drive', 'v3')
    notes = get_notes(service)
    create_index(service, notes)