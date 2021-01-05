from captioning.captioning_database.sf_cap_database.sf_cap_db_v2 import get_dbase_session, ScrapediLearnVideos
from captioning.utilities.v1 import cap_info_router
import time

def fix_youtube_titles(semester):

    session = get_dbase_session("YouTube Title Fixer")

    videos = session.query(ScrapediLearnVideos).filter_by(semester=semester).all()

    for each in videos:
        print(each.title, each.resource_link)
        if each.captioned != True:

            youTubeInfo = cap_info_router.get_mainstream_video_info(each.resource_link)
            print(youTubeInfo)

            if youTubeInfo is not None:
                print(each.captioned)
                if each.title is None:
                    time.sleep(0.8)
                    each.title = youTubeInfo['api-provided-title']
                if each.captioned is None or each.captioned is False:
                    each.captioned = youTubeInfo['cap-state']

    session.commit()


# youTubeInfo = cap_info_router.get_mainstream_video_info('https://www.youtube.com/watch?v=yJE9bkjSoS8')
# print(youTubeInfo)

fix_youtube_titles('fa20')


# def update_cap_status(semester):
#
#     session = get_dbase_session("YouTube Title Fixer")
#     videos = session.query(ScrapediLearnVideos).filter_by(semester=semester).all()







