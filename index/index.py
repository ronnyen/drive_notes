from datetime import datetime

from consts import DOC_LINK_TEMPLATE, INDEX_FOLDER_ID
from services.drive_service import create_file_in_folder


def create_index(service, note_files):
    create_html_index(note_files)
    create_file_in_folder(service, 'output/index.html', 'index_test', INDEX_FOLDER_ID)


def create_html_index(note_files):
    index_rows = ['<meta http-equiv="Content-type" content="text/html; charset=utf-8" />']
    index_rows.append('<h3 style="padding:30px;color:white;background-color:#4a6aed;font-family:verdana">For Review Today</h3>')
    index_rows.extend([_generate_file_line(x) for x in note_files if x.next_review.date() == datetime.now().date()])

    index_rows.append('<h3 style="padding:30px;color:white;background-color:#4a6aed;font-family:verdana">Last Created</h3>')
    note_files.sort(key=lambda x: x.created_date, reverse=True)
    index_rows.extend([_generate_file_line(x) for x in note_files[:10]])

    index_rows.append('<h3 style="padding:30px;color:white;background-color:#4a6aed;font-family:verdana">Last Updated</h3>')
    note_files.sort(key=lambda x: x.updated_date, reverse=True)
    index_rows.extend([_generate_file_line(x) for x in note_files[:10]])

    index_rows.append('<h1 style="padding:30px;color:white;background-color:SlateBlue;font-family:verdana">By Topic</h1>')
    topics = list(set([file.topic for file in note_files]))
    for topic in topics:
        index_rows.append(f'<h3 style="padding:10px;color:white;background-color:#4a6aed;font-family:verdana">{topic}</h3>')
        topic_files = [file for file in note_files if file.topic == topic]
        index_rows.extend([_generate_file_line(x) for x in topic_files])

    with open("output/index.html", "w", encoding='utf-8') as file:
        file.write('\n'.join(index_rows))


def _generate_file_line(file):
    return f'<div><a style="text-decoration: none;font-size:20px" target="_blank" href = "{DOC_LINK_TEMPLATE.format(doc_id=file.id)}" >{file.name} </a> <span style="color:#AEB6BF;float:right;">{file.updated_date.date() or file.created_date.date()}</span></div>'