from master_config import amara_credentials
import requests, json

auth_header = {'X-api-username': amara_credentials['amara_user_id'], 'X-api-key': amara_credentials['amara_key']}
videos_endpoint = "https://amara.org/api/videos/"

def check_source_video(video_url):
    """
    :param video_url: third party link. See if it exists in amara
    :return: False or Amara ID object ID
    """

    vid_check = requests.get(videos_endpoint, params = {"video_url": video_url})
    metadata = json.loads(vid_check.content.decode('utf-8'))
    if len(metadata['objects']) == 0:
        return False
    else:
        return metadata['objects'][0]


def get_amara_resource_by_id(video_id):
    """
    :param video_url: amara video id
    :return: False or Amara Objects
    """

    vid_check = requests.get("{}{}/".format(videos_endpoint, video_id))
    metadata = json.loads(vid_check.content.decode('utf-8'))
    if 'id' not in metadata.keys():
        return False
    else:
        return metadata


def post_video(video_url, title):

    post_data = {
        "video_url": video_url,
        "title": title,
        "description": "Captioning provided by SF State DPRC. https://access.sfsu.edu/",
        "primary_audio_language_code": "en-US"
    }

    post_video = requests.post(videos_endpoint, headers=auth_header, data=post_data)
    metadata = json.loads(post_video.content.decode('utf-8'))
    print("SDGSDGSDGSDG", metadata)
    return metadata




def upload_subtitle(file, video_id, complete=True):

    with open(file, encoding='utf8') as srt:
        srt_string = srt.read()


    sub_post_data = {

        "subtitles": srt_string,
        "sub_format": "srt",
        "is_complete": complete
    }

    post_subtitles = requests.post("https://amara.org/api/videos/{}/languages/en-US/subtitles/".format(video_id),
                                   headers=auth_header,
                                   data=sub_post_data)
    print("Subtitles Posted", post_subtitles.content)

    if post_subtitles.ok:
        return True
    else:
        return False

