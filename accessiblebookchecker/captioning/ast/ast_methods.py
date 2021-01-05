from captioning.captioning_database.sf_cap_database.sf_cap_db_v2 import AstJob,\
    CaptioningJob, get_dbase_session, AstAuth, CaptioningMedia, S3FileStorage, MediaObjectAssignments
from master_config import ast_default, ast_credentials as creds
import requests, json, datetime, html, os
from captioning.app_file_manager.file_actions import download_video
from sqlalchemy import func

def get_ast_auth_token():

    def get_new_creds():

        customer_id = creds['customer_id']
        partner_type = creds['partner_type']
        customers_secret = creds['customer_secret']
        authenticate = creds['authentication_url']
        payload = {"method": "authenticate", "params": { "PartnerType": partner_type,
                                                         "CustomerID": customer_id,
                                                         "CustomerSecret": customers_secret}
                   }
        print(payload, authenticate)
        auth_request = requests.post(authenticate, data=json.dumps(payload))
        if auth_request.status_code == 401:
            print(auth_request.content, auth_request.status_code)
            return False
        print(auth_request.content)
        auth_token = json.loads(auth_request.content.decode('utf-8'))['access_token']

        return auth_token

    session = get_dbase_session("create_ast_job")
    current_token = session.query(AstAuth).filter_by(id=1).first()

    if current_token is None:
        new_creds = get_new_creds()
        new_auth = AstAuth(
            active_bearer_token=new_creds,
            set_date=datetime.datetime.now()
        )
        session.add(new_auth)
        session.commit()
        session.close()
        return new_creds
    else:
        if datetime.datetime.now().replace(tzinfo=None) - datetime.timedelta(hours=24) <= current_token.set_date <= datetime.datetime.now():
            new_creds = get_new_creds()
            current_token.active_bearer_token = new_creds
            current_token.set_date = datetime.datetime.now()
            session.commit()
            session.close()
            return new_creds
        else:
            return current_token.active_bearer_token


def pre_create_ast_job(job_id, media_file_id, ast_notes, rate=None):
    session = get_dbase_session("pre_create_ast_job")

    cap_job = session.query(CaptioningJob).filter_by(id=job_id).first()
    if cap_job is None:
        return False

    media = session.query(CaptioningMedia).filter_by(id=cap_job.media_id).first()
    next_ast_id = session.query(func.max(AstJob.id)).scalar() + 1

    ast_callback = "{}{}{}".format(ast_default['ast_callback'], "?media_id=", cap_job.media_id)
    ast_status_url = "{}{}{}".format(ast_default['ast_status'], "?jobid=", next_ast_id)



    ast_job_dict = {

        'next_ast_id': next_ast_id,
        'data_to_commit': {
            'id': next_ast_id,
            'caption_job_id': cap_job.id,
            'ast_description': ast_default['ast_description'],
            'ast_language': ast_default['ast_language'],
            'ast_rush': rate if rate is not None else ast_default['ast_rush'],
            'ast_have_trans': ast_default['ast_have_trans'],
            'ast_notes': ast_notes if ast_notes is not None else ast_default['ast_notes'],
            'ast_basename': media.title,
            'ast_purchase_order': ast_default['ast_purchase_order'],
            'ast_callback': ast_callback,
            'ast_status_url': ast_status_url,
            'media_file_id': media_file_id


    }}
    session.close()
    return ast_job_dict

def create_ast_job(job_id):
    session = get_dbase_session("create_ast_job")

    cap_job = session.query(CaptioningJob).filter_by(id=job_id).first()
    if cap_job is None:
        return False

    media = session.query(CaptioningMedia).filter_by(id=cap_job.media_id).first()
    ast_callback = "{}{}{}".format(ast_default['ast_callback'], "?type=srt&media_id=", cap_job.media_id)

    new_ast_job = AstJob(

        caption_job_id=cap_job.id,
        ast_description=ast_default['ast_description'],
        ast_language=ast_default['ast_language'],
        ast_rush=ast_default['ast_rush'],
        ast_have_trans=ast_default['ast_have_trans'],
        ast_notes=ast_default['ast_notes'],
        ast_basename=media.title,
        ast_purchase_order=ast_default['ast_purchase_order'],
        ast_callback=ast_callback,
        ast_status_url="None" #assigned after caption_job_id is created

    )

    session.add(new_ast_job)
    session.flush()
    ast_job_id = new_ast_job.id

    ast_status_url = "{}{}{}".format(ast_default['ast_status'],"?jobid=", ast_job_id)
    new_ast_job.ast_status_url = ast_status_url

    session.commit()
    session.close()

    return ast_job_id


def submit_ast_job(ast_job_id):

    session = get_dbase_session("submit_ast_job")
    ast_cap_job = session.query(AstJob).filter_by(id=ast_job_id).first()
    if not ast_cap_job:
        return False, 404

    submit_url = creds['submissions_url']

    header = {"Authorization": "Bearer " + get_ast_auth_token()}

    params = {"method":"create",
              "params": {"App": creds['app'],
                         "Description": ast_cap_job.ast_description,
                         "Language":ast_cap_job.ast_language,
                         "Notes":ast_cap_job.ast_notes,
                         "Rush":ast_cap_job.ast_rush,
                         "HaveTrans": ast_cap_job.ast_have_trans,
                         "CallBack": html.escape(ast_cap_job.ast_callback),
                         "StatusURL": html.escape(ast_cap_job.ast_status_url)
                         }
              }




    submit_job = requests.post(submit_url, data=json.dumps(params), headers=header)

    if submit_job.status_code == 201:
        new_id = json.loads(submit_job.content.decode('utf-8'))["new_id"]
        session.close()
        return new_id
    else:
        session.close()
        return False, submit_job.status_code

def submit_ast_job_update_job(ast_job_id):

    session = get_dbase_session("submit_ast_job")
    ast_cap_job = session.query(AstJob).filter_by(id=ast_job_id).first()
    print("JOBID", ast_cap_job)
    if not ast_cap_job:
        return False
    submit_url = creds['submissions_url']

    header = {"Authorization": "Bearer " + get_ast_auth_token()}
    params = {"method": "create",
              "params": {"App": creds['app'],
                         "Description": ast_cap_job.ast_description,
                         "Language":ast_cap_job.ast_language,
                         "Notes":ast_cap_job.ast_notes,
                         "Rush":ast_cap_job.ast_rush,
                         "HaveTrans": ast_cap_job.ast_have_trans,
                         "CallBack": html.escape(ast_cap_job.ast_callback),
                         "StatusURL": html.escape(ast_cap_job.ast_status_url)
                         }
              }
    print('PARAMS', json.dumps(params))
    submit_job = requests.post(submit_url, data=json.dumps(params), headers=header)
    print(submit_job.status_code, submit_job.content)
    if submit_job.status_code == 201:
        new_id = json.loads(submit_job.content.decode('utf-8'))["new_id"]
        ast_cap_job.ast_id = new_id
        session.commit()
        session.close()
        return new_id
    else:
        session.close()
        return False




def get_details(ast_id):

    submit_url = creds['submissions_url']
    header = {"Authorization": "Bearer " + get_ast_auth_token()}
    params = {"method": "get_details",
              "params": {"ASTid": ast_id}
              }

    get_details = requests.post(submit_url, data=json.dumps(params), headers=header)
    return True
# get_details('1589418828sfsudev')



def upload_media_to_ast(ast_id):

    session = get_dbase_session("submit_file_to_ast")

    ast_job = session.query(AstJob).filter_by(ast_id=ast_id).first()
    file_record = session.query(S3FileStorage).filter_by(id=ast_job.media_file_id).first()

    downloaded_video = os.path.normpath(download_video(file_record.key, file_record.file_name))
    submit_url = creds['submissions_url']
    files = {'file': open(downloaded_video, 'rb')}

    content = {
        'X-ASTid': ast_id,
        'filename': file_record.file_name,
    }

    header = {
        'Authorization': "Bearer " + get_ast_auth_token(),
        'X-ASTid': ast_id,
        'filename': file_record.file_name,
        'method': 'add_media'

    }
    send_file = requests.post(url=submit_url, files=files, headers=header, data=content)
    print("SEND FILE", send_file.content, send_file.status_code)

    if send_file.ok:
        return True
    else:
        return False


def cancel_ast_job(ast_id):
    pass


