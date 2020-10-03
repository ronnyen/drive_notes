from consts import HORIZONTAL_LINE, INDEX_FOLDER_ID, DOC_LINK_TEMPLATE
from models.note_file import NoteFile
from services.drive_service import get_folder_files_ids, create_file_in_folder, get_file_content
from services.google_service import create_service


def extract_metadata_from_file(file_content):
    raw_metadata = file_content.split(HORIZONTAL_LINE)[0]
    return {att.split(': ')[0]: att.split(': ')[1] for att in raw_metadata.split('\r\n') if att}


def create_note_file(service, file_id):
    file_content = get_file_content(service, file_id)
    file_metadata = extract_metadata_from_file(file_content)
    return NoteFile(file_id, file_content, title=file_metadata.get('Title'),
                                            created_date=file_metadata.get('Created date'),
                                            topic=file_metadata.get('Topic'),
                                            tags=file_metadata.get('Tags'))


def get_files(service):
    files = []
    files_ids = get_folder_files_ids(service)
    for file_id in files_ids:
        file = create_note_file(service, file_id)
        files.append(file)
    return sorted(files, key=lambda x: (x.topic, x.tags))


def create_html_index(note_files):
    index = '\n'.join([f'<div> {file.topic} - {file.tags} - <a href="{DOC_LINK_TEMPLATE.format(doc_id=file.id)}"> {file.title} </a> </div>'
                          for file in note_files])

    with open("output/index.html", "w") as file:
        file.write(index)


def create_index(service, note_files):
    index = '\n'.join([f'<div> {file.topic} - {file.tags} - {file.title} - {file.id} </div>' for file in note_files])
    with open("output/index.html", "w") as file:
        file.write(index)
    create_file_in_folder(service, 'output/index.html', 'index_test', INDEX_FOLDER_ID)


if __name__ == '__main__':
    service = create_service('drive', 'v3')
    files = get_files(service)
    create_html_index(files)
    # create_index(service, files)