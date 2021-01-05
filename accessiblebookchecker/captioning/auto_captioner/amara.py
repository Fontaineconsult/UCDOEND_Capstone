import requests
import json
import os
from captioning.auto_captioner.config import Config

app_config = Config()


class Amara(object):

    def __init__(self, video_url, title):


        self.auth_header = {'X-api-username': app_config.amara_user_id, 'X-api-key': app_config.amara_key}
        self.video_url = video_url
        self.title = title
        self.metadata = None
        self.video_id = None


    def check_video(self):

        vid_check = requests.get("https://amara.org/api/videos/", params = {"video_url": self.video_url})

        self.metadata = json.loads(vid_check.content)
        if len(self.metadata['objects']) == 0:
            return False
        else:
            self.video_id = self.metadata['objects'][0]['id']
            return True

    def post_video(self):
        post_data = {
            "video_url": self.video_url,
            "title": self.title,
            "description": self.title,
            "primary_audio_language_code": "en-US"
        }

        if not self.check_video():

            post_video = requests.post("https://amara.org/api/videos/", headers=self.auth_header, data=post_data)
            print(post_video.content)

            self.metadata = json.loads(post_video.content)
            self.video_id = self.metadata['id']
            print("Amara Video Located Here: amara.org/en/videos/{}".format(self.video_id))
            return self.video_id

        else:
            print("URL already exists as another Amara resource. Using instead: amara.org/en/videos/{}".format(self.video_id))
            return self.video_id


    def post_subtitle(self):

        with open(os.getcwd() + "\\srt_temp\\{}.srt".format(self.title), 'r') as srt:
            srt_string = srt.read()


        sub_post_data = {
            "subtitles": srt_string,
            "sub_format": "srt",
            "title": self.title,
            "is_complete": False
        }



        post_subtitles = requests.post("https://amara.org/api/videos/{}/languages/en-US/subtitles/".format(self.video_id),
                                       headers=self.auth_header,
                                       data=sub_post_data)
        print("Subtitles Posted", post_subtitles)
