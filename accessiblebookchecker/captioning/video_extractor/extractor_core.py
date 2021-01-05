
from __future__ import unicode_literals
import os
import youtube_dl
from master_config import file_config
from unidecode import unidecode


extension = "{}{}".format(file_config['temp_upload_files'], "%(title)s")

root = file_config['root']
current_dir = os.getcwd()

##! make sure file name fits in windows limit

class VideoDownload(object):

    def __init__(self, url, format):
        self.url = url
        self.format = format
        self.video_info = self._get_info()
        self.fixed_title = self.clean_filename(self.video_info['title'])
        self.extension = '{}.%(ext)s'.format(self.fixed_title)
        self.file_location = root + file_config['temp_upload_files'] + self.extension
        self.file_name = self.fixed_title + "." + format
        self.saved_location = os.path.normpath(root + file_config['temp_upload_files'] + self.file_name)
        self.options = {'outtmpl': self.file_location,
                        'forcefilename': False,
                        'format': format,
                        'progress_hooks': [self.hook],
                        }


    def _get_info(self):

        with youtube_dl.YoutubeDL() as ydl:
            test = ydl.extract_info(self.url, download=False)
            return ydl.extract_info(self.url, download=False)


    def download(self):

        with youtube_dl.YoutubeDL(self.options) as ydl:

            ydl.download([self.url])

    def clean_filename(self, title):
        decoded_title = unidecode(title)
        new_title = decoded_title.replace('/', '-') \
            .replace('.', '-') \
            .replace(':','') \
            .replace('?','') \
            .replace("'",'') \
            .replace('"','') \
            .replace(',','') \
            .replace(' ','-') \
            .replace('|', '-') \
            .replace(';', '')\
            .replace("'", '')

        return new_title


    def hook(self, d):
        pass

