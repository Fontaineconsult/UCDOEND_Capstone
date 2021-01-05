import captioning.aws.s3_file_exchange as s3
import captioning.app_file_manager.aws_amp_database_functions as aws_amp
import uuid, glob, os
import pathlib
from master_config import file_config
import mimetypes
import ntpath

temp_video_folder = file_config['temp_upload_files']
temp_text_folder = file_config['temp_text_files']
root = file_config['root']



def _clean_filename(title):

    new_title = title.replace('/', '') \
        .replace('.', ' ') \
        .replace(':','') \
        .replace('?','') \
        .replace("'",'') \
        .replace('"','') \
        .replace(',','') \
        .replace(' ','-') \
        .replace('|', '')

    return new_title



def clear_temp_folder(folder=None):
    if folder == "text_temp":
        folder = temp_text_folder
    if folder == "video_temp":
        folder = temp_video_folder

    text_files = glob.glob(root + folder + "*")
    for f in text_files:
        if os.path.basename(f) == 'null.py':
            continue
        else:
            try:
                os.remove(f)
            except OSError:
                continue

def _upload_video_to_s3(file_name, file_extension):

    uuid_name = uuid.uuid1()
    file_location = "{}{}{}".format(root, temp_video_folder, file_name)
    s3_attemp = s3.upload_file_to_s3_base(file_location, 's3_video_storage_folder', file_extension, uuid_name, "video/mp4")
    return s3_attemp[0], s3_attemp[1], uuid_name


def _upload_srt_to_s3(file_name, file_extension):
    uuid_name = uuid.uuid1()
    file_location = "{}{}{}".format(root, temp_text_folder, file_name)
    s3_attemp = s3.upload_file_to_s3_base(file_location, 's3_srt_storage_bucket', file_extension, uuid_name, "text/srt")
    return s3_attemp[0], s3_attemp[1], uuid_name




def _get_video(filename=None, object_uuid=None, source_url=None):

    if filename:
        return aws_amp.query_filename(filename)
    if object_uuid:
        return aws_amp.query_object_uuid(object_uuid)
    if source_url:
        return aws_amp.query_source_url(source_url)


def _get_srt(filename=None, object_uuid=None, source_url=None):

    if filename:
        return aws_amp.query_filename(filename)
    if object_uuid:
        return aws_amp.query_object_uuid(object_uuid)
    if source_url:
        return aws_amp.query_source_url(source_url)


def _write_srt(data, file_name):

    file_location = "{}{}{}".format(root, temp_text_folder, file_name)

    with open(file_location, 'a', encoding='utf8') as file:
        file.write(data)
        file.close()
    return file_location


### Public Functions ###


def save_file_locally(data, file_name):

    file_location = "{}{}{}".format(root, temp_video_folder, file_name)

    with open(file_location, 'wb') as file:
        file.write(data)
        file.close()

    return file_location





def upload_video(source_url, file_name, sha_256_hash):

    file_extension = pathlib.Path(file_name).suffix
    upload_attempt = _upload_video_to_s3(file_name, file_extension)
    new_file_id = aws_amp.add_file_to_db(source_url,
                           upload_attempt[0],
                           upload_attempt[1],
                           upload_attempt[2],
                           file_name,
                           sha_256_hash,
                           mimetypes.guess_type(file_name))

    clear_temp_folder('video_temp')
    return new_file_id


def upload_extracted_video(file_location, file_name, file_hash, source_url):
    file_extension = pathlib.Path(file_location).suffix
    file_name = ntpath.basename(file_location)
    upload_attempt = _upload_video_to_s3(file_name, file_extension)
    new_file_id = aws_amp.add_file_to_db(source_url,
                                         upload_attempt[0],
                                         upload_attempt[1],
                                         upload_attempt[2],
                                         file_name,
                                         file_hash,
                                         mimetypes.guess_type(file_name))

    clear_temp_folder('video_temp')

    return new_file_id



def upload_srt(data, file_name, commit=False):



    file_extension = pathlib.Path(file_name).suffix

    sanitized_file_name = _clean_filename(file_name)
    _write_srt(data, sanitized_file_name)
    upload_attempt = _upload_srt_to_s3(sanitized_file_name, file_extension)

    if not commit:
        clear_temp_folder('text_temp')
        return upload_attempt



def download_srt(object_name, file_name):

    # empty migrations.temp folder to keep it clean
    clear_temp_folder('text_temp')

    file_location = "{}{}{}".format(root, temp_text_folder, file_name)
    s3.download_file_from_s3_base(object_name, file_location)
    return file_location



def download_video(object_name, file_name):

    # empty migrations.temp folder to keep it clean
    clear_temp_folder('video_temp')

    file_location = "{}{}{}".format(root, temp_video_folder, file_name)
    s3.download_file_from_s3_base(object_name, file_location)
    return file_location





# def upload_transcript(source_url, file_name):
#
#     file_extension = pathlib.Path(file_name).suffix
#     upload_attempt = _upload_video_to_s3(file_name, file_extension)
#     aws_amp.add_file_to_db(source_url,
#                            upload_attempt[0],
#                            upload_attempt[1],
#                            upload_attempt[2],
#                            file_name,
#                            mimetypes.guess_type(file_name))
#
#     video_files = glob.glob(root + temp_video_folder + "*")
#     for f in video_files:
#         os.remove(f)
#
#
#
#
#
#
# def download_video(query_param):
#
#     get_record = _get_video(None, None, query_param)
#     s3.download_file_from_s3_base(get_record[0].key, get_record[0].file_name)
#     return get_record
