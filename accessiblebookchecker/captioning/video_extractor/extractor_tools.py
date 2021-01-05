from captioning.video_extractor.extractor_core import VideoDownload
from captioning.app_file_manager.file_actions import upload_video
import os

def extract_video_video(video_url):

    download = VideoDownload(video_url, 'mp4')
    download.download()
    return download.saved_location



def extract_video_audio(video_url):
    download = VideoDownload(video_url, 'm4a')
    download.download()
    return download.saved_location
