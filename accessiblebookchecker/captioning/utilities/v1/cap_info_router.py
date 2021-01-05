import re
from urllib.parse import urlparse
from captioning.video_info import amara_api, vimeo_api, youtube_api
import time


video_service_regex = re.compile(r"(youtube.com|youtu.be.com|youtu.be)|(amara.org)|(vimeo.com|player.vimeo.com)")
##! needs to detect bad urls and inform user

def get_mainstream_video_info(url):

    video_service_location = urlparse(url)[1]
    video_service_location = r"{}".format(video_service_location)

    url_service_group = video_service_regex.search(video_service_location)


    if url_service_group:
        time.sleep(0.3)
        print(url_service_group.groups())
        if url_service_group.group(1):

            caption_state = youtube_api.get_youtube_caption_info(url)
            video_title = youtube_api.get_youtube_video_title(url)
            return {"cap-state": caption_state, "api-provided-title": video_title}

        elif url_service_group.group(2):
            caption_state = amara_api.get_amara_video_info(url)
            return {"cap-state": caption_state['amara-subtitled'], "api-provided-title": caption_state['amara-title']}
        # elif url_service_group.group(3):
        #     caption_state_and_title = vimeo_api.get_vimeo_video_info(url)
        #     print(caption_state_and_title)
        #     return {"cap-state": caption_state_and_title['vimeo-subtitled'], "api-provided-title": caption_state_and_title['amara-title']}
    else:
        return None



