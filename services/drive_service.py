from googleapiclient.http import MediaFileUpload

from consts import NOTES_FOLDER_ID


def get_folder_docs(service):
    res = service.files().list(**{'q': f"'{NOTES_FOLDER_ID}' in parents and trashed = false", "fields": '*'}).execute()
    return [file for file in res.get('files') if 'document' in file['mimeType']]


def get_file_content(service, file_id):
    return service.files().export(**{'fileId': file_id, 'mimeType': 'text/plain'}).execute().decode('utf-8-sig')


def create_file_in_folder(service, file_path, file_name, folder_id):
    media = MediaFileUpload(file_path,
                            mimetype='text/html',
                            resumable=True)
    file_metadata = {
        'name': file_name,
        'parents': [folder_id],
        'mimeType': 'application/vnd.google-apps.document'
    }

    service.files().create(body=file_metadata, media_body=media).execute()
