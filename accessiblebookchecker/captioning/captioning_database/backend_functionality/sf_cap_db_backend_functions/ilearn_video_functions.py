from captioning.captioning_database.sf_cap_database.sf_cap_db_v2 import ScrapediLearnVideos, get_dbase_session

# sf_cap_db_session = get_dbase_session()

##! refactor to use template method

# def get_videos_by_course_id(semester, course_id):
#
#     course_id = str(course_id)
#
#     video_query = sf_cap_db_session.query(ScrapediLearnVideos).filter_by(semester=semester).filter_by(course_id=course_id).all()
#     sf_cap_db_session.commit()
#
#     if video_query:
#
#         return video_query
#     else:
#         return None
#
# def add_user_submitted_link(title,
#                             course_id,
#                             link,
#                             caption_state,
#                             show_date,
#                             resource_type):
#
#     resource_check = sf_cap_db_session.query(ScrapediLearnVideos).filter_by(resource_link=link).filter_by(course_id=course_id).first()
#
#     if not resource_check:
#
#         video_resource = ScrapediLearnVideos(resource_link=link,
#                                       title=title,
#                                       course_gen_id=course_id,
#                                       captioned=caption_state,
#                                       indicated_due_date=show_date,
#                                       resource_type=resource_type)
#
#
#         sf_cap_db_session.add(video_resource)
#         sf_cap_db_session.commit()
#         return True
#     else:
#         return False
#
#
#
# def commit_ilearn_video_content(title, link, course_id, scan_date, caption_state):
#
#     resource_check = sf_cap_db_session.query(ScrapediLearnVideos).filter_by(resource_link=link).filter_by(course_id=course_id).first()
#
#     if not resource_check:
#
#         video_resource = ScrapediLearnVideos(resource_link=link,
#                                       title=title,
#                                       course_gen_id=course_id,
#                                       scan_date=scan_date,
#                                       captioned=caption_state)
#
#         sf_cap_db_session.add(video_resource)
#         sf_cap_db_session.commit()
#
#     else:
#         print(resource_check.title, resource_check.captioned, title, caption_state)
#         if resource_check.title is None:
#             resource_check.title = title
#         if resource_check.captioned is None or resource_check.captioned is False:
#             resource_check.captioned = caption_state
#         else:
#             print("already exists")
#
#         sf_cap_db_session.commit()
#
#
# def check_or_commit_course(course_id,
#                            semester):
#     print(course_id)
#
#     course_to_check = sf_cap_db_session.query(ScrapediLearnVideos).filter_by(course_id=course_id).all()
#
#     if course_to_check:
#         return True
#     else:
#         course_to_commit = ScrapediLearnVideos(course_gen_id=course_id,
#                                                semester=semester)
#         sf_cap_db_session.add(course_to_commit)
#         sf_cap_db_session.commit()
#         return False
#
#
# def get_all_videos_from_db_by_course(semester):
#
#
#     grouped_by_course_videos = sf_cap_db_session.query(ScrapediLearnVideos).filter_by(semester=semester).all()
#
#     if grouped_by_course_videos:
#         return grouped_by_course_videos
#     else:
#         return None
#
#
# def flush_all_video_records():
#     try:
#         sf_cap_db_session.query(ScrapediLearnVideos).delete()
#         sf_cap_db_session.commit()
#         print("Deleted All Records")
#     except:
#         print("Something went wrong, rolling back")
#         sf_cap_db_session.rollback()
#
#
# def write_update_caption_status(link, status):
#
#     video_query = sf_cap_db_session.query(ScrapediLearnVideos).filter_by(resource_link=link).all()
#
#     if video_query:
#         for video in video_query:
#             print(video_query)
#             print("request to save", video.resource_link, status)
#             video.captioned = status
#         sf_cap_db_session.commit()
#
#         return True
#
#     else:
#         return False
#
#
# def write_submit_status(link, status, date):
#
#     video_query = sf_cap_db_session.query(ScrapediLearnVideos).filter_by(resource_link=link).all()
#
#     if video_query:
#
#         for video in video_query:
#
#             video.submitted_for_processing = status
#             video.submitted_for_processing_date = date
#         sf_cap_db_session.commit()
#         ##! incomplete solution
#         return True
#     else:
#         return False
#
#
#
# def write_update_showdate(link, showdate, course_id):
#
#     update_showdate = sf_cap_db_session.query(ScrapediLearnVideos).filter_by(resource_link=link, course_id=course_id).all()
#
#     if update_showdate:
#         for video in update_showdate:
#             video.indicated_due_date = showdate
#         sf_cap_db_session.commit()
#         return True
#     else:
#         return False
#
#
#
# def get_all_videos(semester):
#     all_videos = []
#     grouped_by_course_videos = sf_cap_db_session.query(ScrapediLearnVideos).filter_by(semester=semester).all()
#
#     for each_course in grouped_by_course_videos:
#         for each_video in each_course.assigned_videos:
#             all_videos.append(each_video)
#
#     return all_videos
#
#
# def update_video_title(url, title):
#
#     titles_to_update = sf_cap_db_session.query(ScrapediLearnVideos).filter_by(resource_link=url).all()
#
#     for each_video in titles_to_update:
#         each_video.title = title
#         sf_cap_db_session.commit()