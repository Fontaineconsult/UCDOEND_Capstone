from flask import Blueprint, request, make_response, send_file
from captioning.app_file_manager.file_actions import upload_srt, download_srt, upload_video, save_file_locally,\
    download_video,clear_temp_folder, upload_extracted_video
import json
from captioning.aws.s3_file_exchange import make_file_public
from captioning.captioning_database.sf_cap_database.sf_cap_db_v2 import get_dbase_session, MediaObjectAssignments, \
    CaptioningMedia, S3CaptionStorage, AstStatus, AstJob, S3FileStorage, AmaraResources, CaptionedResources
from master_config import file_config
import xml.etree.ElementTree as ET
from captioning.amara import amara_methods
from captioning.video_extractor.extractor_tools import extract_video_audio, extract_video_video
import hashlib
import mimetypes


srt_dir = ".." + file_config['temp_text_files']
captioning_service_routes_v1 = Blueprint('captioning_service_v1', __name__)

def _clean_filename(title):

    new_title = title.replace('/', '') \
        .replace('.', '-') \
        .replace(':','-') \
        .replace('?','-') \
        .replace("'",'') \
        .replace('"','') \
        .replace(',','') \
        .replace(' ','-') \
        .replace('|', ' ')

    return new_title


@captioning_service_routes_v1.route("/upload/file",  methods=['POST'])
def upload_file_endpoint():

    if request.method == 'POST':
        print(request.headers)
        headers = request.headers
        accept_headers = ["video/mp4",
                          "audio/m4a",
                          "audio/mpeg",
                          "audio/x-m4a"]
        print(mimetypes.guess_extension(headers["Content-Type"]))

        if headers["Content-Type"] not in  accept_headers:
            return make_response("Invalid Content Type", 400)

        if "Media-Id" not in headers:

            return make_response("Invalid Args", 405)

        session = get_dbase_session('file_upload')
        media_record = session.query(CaptioningMedia).filter_by(id=headers['media_id']).first()


        if media_record is None:
            return make_response("Not Found", 404)

        file_name = "{}{}".format(_clean_filename(media_record.title), mimetypes.guess_extension(headers["Content-Type"]))
        file_location = save_file_locally(request.data, file_name)
        new_file_id = upload_video(file_location, file_name, media_record.sha_256_hash)

        media_object_assignment = MediaObjectAssignments(media_id=media_record.id,
                                                         s3_file_key=new_file_id)
        session.add(media_object_assignment)
        session.commit()
        session.close()

    return make_response("Success", 201)

@captioning_service_routes_v1.route("/upload/caption",  methods=['POST'])
def upload_srt_endpoint():

    if request.method == 'POST':
        print("SDGSDG", request.headers)

        accept_headers = ["text/plain",
                          "text/html",
                          "text/x-subrip",
                          "text/html; charset=utf-8",
                          "application/x-subrip"]

        headers = request.headers

        if headers["Content-Type"] not in accept_headers:
            return make_response("Invalid Content Type", 400)

        if "media_id" not in request.args or request.args['media_id'] == 'undefined':
            return make_response("Invalid Args", 400)

        session = get_dbase_session('caption_uploader')
        media_record = session.query(CaptioningMedia).filter_by(id=request.args['media_id']).first()

        if media_record is None:
            return make_response("Not Found", 404)

        key, object_url, object_uuid = upload_srt(request.data.decode('utf-8'),
                                                  "{}{}".format(media_record.title, ".srt"))

        s3_object = S3CaptionStorage(
                                  key=key,
                                  object_url=object_url,
                                  object_uuid=object_uuid,
                                  file_name="{}{}".format(_clean_filename(media_record.title), ".srt"),
                                  mime_type='text/plain')
        session.add(s3_object)
        session.flush()
        new_srt_id = s3_object.id

        media_object_assignment = MediaObjectAssignments(media_id=media_record.id,
                                                         s3_caption_key=new_srt_id)
        session.add(media_object_assignment)
        session.commit()
        session.close()




        return make_response("Success", 201)


@captioning_service_routes_v1.route("/download/caption",  methods=['GET'])
def upload_caption():

    if request.method == 'GET':

        session = get_dbase_session('caption_downloader')

        query = session.query(CaptioningMedia, S3CaptionStorage).select_from(CaptioningMedia)\
            .join(MediaObjectAssignments)\
            .join(S3CaptionStorage).filter(CaptioningMedia.id==request.args['media_id']).all()

        if len(query) == 0:
            return make_response("Not Found", 404)

        file = [element for element in query if (str(element[1].id) == request.args['item_id'])]

        if len(file) == 0:
            return make_response("Not Found", 404)

        file_name = file[0][1].file_name
        object_key = file[0][1].key
        file_out = download_srt(object_key, file_name)

        session.close()
        response = make_response(send_file(file_out,
                                           mimetype="text/plain",
                                           attachment_filename=file_name,
                                           as_attachment=True))
        response.headers['Access-Control-Expose-Headers'] = 'content-disposition'
        return response

@captioning_service_routes_v1.route("/download/file",  methods=['GET'])
def upload_file():

    if request.method == 'GET':

        session = get_dbase_session('file_downloader')
        print(request.args['media_id'])
        query = session.query(CaptioningMedia, S3FileStorage).select_from(CaptioningMedia) \
            .join(MediaObjectAssignments) \
            .join(S3FileStorage).filter(CaptioningMedia.id==request.args['media_id'],
                                        S3FileStorage.id==request.args['item_id']).all()



        if len(query) == 0:
            return make_response("Not Found", 404)

        file_name = query[0][1].file_name
        object_key = query[0][1].key
        file = download_video(object_key, file_name)
        session.close()
        return send_file(file,
                         attachment_filename=file_name,
                         as_attachment=True)

@captioning_service_routes_v1.route("/status",  methods=['POST'])
def ast_cap_status():

    if request.method == 'POST':
        session = get_dbase_session('status_update')
        # jobid refers to ast job id
        job_id = session.query(AstJob).filter_by(id=request.args['jobid']).first()
        if job_id is None:
            return make_response("No Id Found", 404)

        tree = (ET.fromstring(request.data))

        status_type = tree.find('Type').text if tree.find('Type') is not None else None
        result = tree.find('Result').text if tree.find('Result') is not None else None
        ast_id = tree.find('ASTid').text if tree.find('ASTid') is not None else None
        ast_status = tree.find('ASTstatus').text if tree.find('ASTstatus') is not None else None
        ast_err_details = tree.find('ErrDetail').text if tree.find('ErrDetail') is not None else None

        status_update = AstStatus(

            job_id=request.args['jobid'],
            ast_id=ast_id,
            ast_type=status_type,
            ast_result=result,
            ast_status=ast_status,
            ast_error_detail=ast_err_details

        )

        session.add(status_update)
        session.commit()
        session.close()

    return make_response("Success", 201)

@captioning_service_routes_v1.route("/amara", methods=['GET', 'POST'])
def amara_endpoint():

    if request.method == 'GET':
        pass

    if request.method == 'POST':

        # {"action": "create-amara-resource", "media_id": 888, [optional] file_id:26} # defaults url, file_id for file
        # {"action": "attach-amara-caption", "caption_id": 20, "amara_id": vYlVnBUmBDyC}

        data = json.loads(request.data.decode('utf-8'))

        if data['action'] == "create-amara-resource":
            session = get_dbase_session('amara_service_add_video')
            media_record = session.query(CaptioningMedia).filter_by(id=data['media_id']).first()
            source_url=media_record.source_url

            if 'file_id' in data:
                file = session.query(S3FileStorage).filter_by(id=data['file_id']).first()
                make_file_public(file.key)
                source_url = file.object_url

            check_amara = amara_methods.check_source_video(source_url)

            if not check_amara:
                add_video_to_amara = amara_methods.post_video(source_url, media_record.title)
                amara_video = AmaraResources(
                    url="https://amara.org/en/videos/{}".format(add_video_to_amara['id']),
                    title=media_record.title,
                    video_id=add_video_to_amara['id']  # the new amara id
                )
                session.add(amara_video)
                session.flush()
                resource = CaptionedResources(
                    media_id=media_record.id,
                    amara_id=amara_video.id
                )
                session.add(resource)
                session.commit()
                session.close()
                return make_response("Success", 201)

            else:
                print("ZZprrss", check_amara)
                amara_id = check_amara['id']
                amara_exists = session.query(AmaraResources).filter_by(video_id=amara_id).first()
                if amara_exists:
                    return make_response("Amara Resource Already Exists in DB {}".format(check_amara), 200)
                else:
                    add_existing_amara = AmaraResources(
                        url="https://amara.org/en/videos/{}".format(amara_id),
                        title=check_amara["title"],
                        video_id=amara_id  # the new amara id
                    )
                    session.add(add_existing_amara)
                    session.flush()
                    resource = CaptionedResources(
                        media_id=media_record.id,
                        amara_id=add_existing_amara.id
                    )
                    session.add(resource)
                    session.commit()
                    session.close()
                    return make_response("Amara Resource Already Exists in Amara. Added to DB {}".format(check_amara),
                                         201)


        if data['action'] == "attach-amara-caption":

            session = get_dbase_session('amara_service_add_caption')
            caption = session.query(S3CaptionStorage).filter_by(id=data['caption_id']).first()
            file = download_srt(caption.key, caption.file_name)
            upload = amara_methods.upload_subtitle(file, data['amara_id'])
            clear_temp_folder("text_temp")

            if upload:
                amara_resource = session.query(AmaraResources).filter_by(video_id=data['amara_id']).first()
                amara_resource.captions_complete = True
                amara_resource.captions_uploaded = True
                session.commit()
                session.close()
                return ("Success", 200)
            else:
                session.close()
                return ("{}{}".format("Failed - ", upload.content), 400)

@captioning_service_routes_v1.route("/extract", methods=['POST'])
def extract_video():

    # {"media_id": "827",
    #  "url": "https://www.youtube.com/watch?v=U5o9b2RVC2E"}

    if request.method == 'POST':

        hasher = hashlib.sha256()
        data = json.loads(request.data.decode('utf-8'))

        if "media_id" not in data and "url" not in data and "format" not in data:
            return make_response("Invalid Args", 405)

        session = get_dbase_session('file_upload')
        media_record = session.query(CaptioningMedia).filter_by(id=data['media_id']).first()

        if media_record is None:
            return make_response("Not Found", 404)

        if data['format'] == 'm4a':

            check_file = session.query(S3FileStorage).filter_by(source_url=data['url'], mime_type='(audio/mpeg,)').scalar() is not None
            if check_file:
                return make_response("Already Exists", 200)
            file_location = extract_video_audio(data['url'])

        if data['format'] == 'mp4':

            check_file = session.query(S3FileStorage).filter_by(source_url=data['url'], mime_type='(video/mpeg,)').scalar() is not None
            if check_file:
                return make_response("Already Exists", 200)
            file_location = extract_video_video(data['url'])

        with open(file_location, 'rb') as afile:
            buf = afile.read(1024)
            hasher.update(buf)
            file_hash = hasher.hexdigest()

        media_record.sha_256_hash = file_hash
        new_file_id = upload_extracted_video(file_location, media_record.title, file_hash, data['url'])

        media_object_assignment = MediaObjectAssignments(media_id=media_record.id,
                                                         s3_file_key=new_file_id)
        session.add(media_object_assignment)
        session.commit()
        session.close()

        return make_response("Success", 201)
