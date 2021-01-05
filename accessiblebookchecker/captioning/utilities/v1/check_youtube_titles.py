import captioning.captioning_database.backend_functionality.ilearn_scraped_db_functions as db
import captioning.utilities.v1.cap_info_router as check_videos


def update_video_titles(semester):

    all_videos = db.get_all_videos(semester)
    print(all_videos)
    for each_video in all_videos:

        print(each_video.title, each_video.resource_link)

        if each_video.title is None:

            video_info = check_videos.get_mainstream_video_info(each_video.resource_link)

            print(video_info)
            if video_info is not None:
                print("updating title", each_video.resource_link, video_info["api-provided-title"])
                db.update_video_title(each_video.resource_link, video_info["api-provided-title"])







if __name__ == '__main__':
    update_video_titles("su20")