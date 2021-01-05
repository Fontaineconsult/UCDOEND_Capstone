import requests
import base64
import json
import re
import master_config

vimeo_info = master_config.vimeo_credentials

vimeo_access_token = None


def get_vimeo_access_token():

    client_identifier = vimeo_info['client_identifier']
    client_secret = vimeo_info['client_secret']

    combined_ident_secret = "{}:{}".format(client_identifier, client_secret)
    str_encode_combined = str.encode(combined_ident_secret)
    base_64_str_encode = base64.b64encode(str_encode_combined)
    base_64_utf8_str_encode = base_64_str_encode.decode('utf-8')

    params = {'grant_type': "client_credentials"}
    header = {'Authorization': 'basic ' + base_64_utf8_str_encode}

    vimeo_authentication = requests.post("https://api.vimeo.com/oauth/authorize/client", params=params, headers=header, timeout=3)


    vimeo_auth_content = vimeo_authentication.content.decode('utf-8')

    vimeo_auth_content_json = json.loads(vimeo_auth_content)

    global vimeo_access_token
    print(vimeo_auth_content_json)

    try:
        vimeo_access_token = vimeo_auth_content_json['access_token']
    except KeyError:
        print("Something went wrong getting the vimeo key", vimeo_auth_content_json)


def get_vimeo_video_info(url):
    ##! Returns None for no identifiable reasone broken
    vimeo_id_search = re.compile(r"(?:vimeo.com)\/(?:channels\/|channels\/\w+\/|groups\/[^\/]*\/videos\/|album\/\d+\/video\/|video\/|)(\d+)(?:$|\/|\?)")
    vimeo_url_id = vimeo_id_search.search(url)
    global return_statement
    return_statement = None

    if vimeo_url_id:
        vimeo_resource_id = vimeo_url_id.group(1)


        api_endpoint = "https://api.vimeo.com/videos/"
        video_resource = "{}{}".format(api_endpoint, vimeo_resource_id)
        resource_get_header = {"Authorization": "Bearer {}".format(vimeo_access_token)}
        resource_get = requests.get(video_resource, headers=resource_get_header)

        if resource_get.status_code == 200:

            video_resource_content = json.loads(resource_get.content.decode('utf-8'))



            vimeo_cap_tracks = int(video_resource_content['metadata']['connections']['texttracks']['total'])
            vimeo_resource_title = video_resource_content['name']
            print(vimeo_cap_tracks)

            if vimeo_cap_tracks > 0:

                return_statement = {"vimeo-subtitled": True, "amara-title": vimeo_resource_title}

                return return_statement
            if vimeo_cap_tracks == 0:

                return {"vimeo-subtitled": False, "amara-title": vimeo_resource_title}




        elif resource_get.status_code == 401:
            ##! needs to be checked. Could result in infinte loop
            get_vimeo_access_token()
            get_vimeo_video_info(url)


        else:
            return {"vimeo-subtitled": None, "amara-title": None}
    else:
        return {"vimeo-subtitled": None, "amara-title": None}
