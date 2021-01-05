import requests, json, re, master_config


amara_info = master_config.amara_credentials

amara_username = amara_info['amara_user_id']
amara_api_key = amara_info['amara_key']


auth_header = {'X-api-username': amara_username, 'X-api-key': amara_api_key}

##! regex is incomplete
amara_id_regex = re.compile(r".*./amara.org/en/videos/([0-9a-zA-Z]{12})") ##! amara regex incomplete

def get_amara_video_info(url):


    amara_id = amara_id_regex.match(url)

    amara_id.group(1)

    video_info = requests.get("https://amara.org/api/videos/{}/".format(amara_id), headers=auth_header)
    amara_request_dict = json.loads(video_info.content.decode('utf-8'))

    for subtitles in amara_request_dict['languages']:
        if subtitles['code'] == 'en' and subtitles['published'] is True:
            return {"amara-subtitled": True, "amara-title": amara_request_dict['title']}
        else:
            return {"amara-subtitled": False, "amara-title": amara_request_dict['title']}



def check_amara_version(url):

    video_info = requests.get("https://amara.org/api/videos/{}/".format(url), headers=auth_header)
    print(video_info.url)
    amara_request_dict = json.loads(video_info.content.decode('utf-8'))
    print(amara_request_dict)


