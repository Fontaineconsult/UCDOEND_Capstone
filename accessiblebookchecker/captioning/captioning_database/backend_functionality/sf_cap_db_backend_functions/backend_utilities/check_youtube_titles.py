import captioning.utilities.v1.cap_info_router as check_videos
from captioning.captioning_database.sf_cap_database.sf_cap_db_v2 import ScrapediLearnVideos, get_dbase_session


def update_video_titles():

    session = get_dbase_session('youTube Titles')


    all_videos = session.query(ScrapediLearnVideos).filter_by(title=None).all()



    for each_video in all_videos:

        print(each_video.title, each_video.resource_link)

        if each_video.title is None:

            video_info = check_videos.get_mainstream_video_info(each_video.resource_link)

            print(video_info)
            if video_info is not None:
                print("updating title", each_video.resource_link, video_info["api-provided-title"])
                each_video.title  = video_info["api-provided-title"]

    session.commit()
    session.close()


update_video_titles()