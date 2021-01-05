import requests
import json
import re
from master_config import youtube

youtube_api_key = youtube["api_key_backup"]


def get_youtube_video_title(link):

    youtube_regex = re.compile(r'((?<=(v|V)/)|(?<=be/)|(?<=(\?|\&)v=)|(?<=embed/))([\w-]+)')
    youtube_id_search = youtube_regex.search(link)

    if youtube_id_search:

        youtube_id = youtube_id_search.group(4)

        payload = {
            'part':'snippet',
            'id': youtube_id,
            'key': youtube_api_key
        }

        youtube_search = requests.get("https://www.googleapis.com/youtube/v3/videos?", params=payload)
        content = json.loads(youtube_search.content.decode('utf-8'))


        try:
            video_title = content['items'][0]['snippet']['title']

            return video_title
        except IndexError:
            return None
        except KeyError:
            print(youtube_search.content, youtube_search.status_code)
            return None
    else:
        return None


def get_youtube_caption_info(link):

    youtube_regex = re.compile(r'((?<=(v|V)/)|(?<=be/)|(?<=(\?|\&)v=)|(?<=embed/))([\w-]+)')
    youtube_id_search = youtube_regex.search(link)

    if youtube_id_search:

        youtube_id = youtube_id_search.group(4)

        payload = {
            'part':'snippet',
            'videoId': youtube_id,
            'key': youtube_api_key
        }

        youtube_search = requests.get("https://www.googleapis.com/youtube/v3/captions?", params=payload)
        content = json.loads(youtube_search.content.decode('utf-8'))

        try:

            for each in content['items']:

                if each['snippet']['trackKind'] == "standard":
                    captioned = True
                    return captioned
                else:
                    continue
            return False

        except (IndexError, KeyError):

            return False
    else:
        return None
