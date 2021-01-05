from captioning.captioning_database.ilearn_scaped_videos_db import iLearn_Video, iLearn_Course
from captioning.captioning_database.ilearn_scaped_videos_db import session as aws_session

# All the things you can do to the aws-dbase

def get_videos_by_course_id(semester, course_id):

    course_id = str(course_id)

    video_query = aws_session.query(iLearn_Course).filter_by(semester=semester).filter_by(course_id=course_id).all()
    aws_session.commit()

    if video_query:

        return video_query
    else:
        return None

def add_user_submitted_link(title,
                            course_id,
                            link,
                            caption_state,
                            show_date,
                            resource_type):

    resource_check = aws_session.query(iLearn_Video).filter_by(resource_link=link).filter_by(course_id=course_id).first()

    if not resource_check:

        video_resource = iLearn_Video(resource_link=link,
                                      title=title,
                                      course_id=course_id,
                                      captioned=caption_state,
                                      indicated_due_date=show_date,
                                      resource_type=resource_type)


        aws_session.add(video_resource)
        aws_session.commit()
        return True
    else:
        return False



def commit_ilearn_video_content(title, link, course_id, scan_date, caption_state):

    resource_check = aws_session.query(iLearn_Video).filter_by(resource_link=link).filter_by(course_id=course_id).first()

    if not resource_check:

        video_resource = iLearn_Video(resource_link=link,
                                      title=title,
                                      course_id=course_id,
                                      scan_date=scan_date,
                                      captioned=caption_state)

        aws_session.add(video_resource)
        aws_session.commit()

    else:
        print(resource_check.title, resource_check.captioned, title, caption_state)
        if resource_check.title is None:
            resource_check.title = title
        if resource_check.captioned is None or resource_check.captioned is False:
            resource_check.captioned = caption_state
        else:
            print("already exists")

        aws_session.commit()


def check_or_commit_course(course_id,
                           course_name,
                           semester):
    print(course_id)

    course_to_check = aws_session.query(iLearn_Course).filter_by(course_id=course_id).all()

    if course_to_check:
        return True
    else:
        course_to_commit = iLearn_Course(course_id=course_id,
                                         course_name=course_name,
                                         semester=semester)
        aws_session.add(course_to_commit)
        aws_session.commit()
        return False


def get_all_videos_from_db_by_course(semester):


    grouped_by_course_videos = aws_session.query(iLearn_Course).filter_by(semester=semester).all()

    if grouped_by_course_videos:
        return grouped_by_course_videos
    else:
        return None


def flush_all_video_records():
    try:
        aws_session.query(iLearn_Video).delete()
        aws_session.commit()
        print("Deleted All Records")
    except:
        print("Something went wrong, rolling back")
        aws_session.rollback()


def write_update_caption_status(link, status):

    video_query = aws_session.query(iLearn_Video).filter_by(resource_link=link).all()

    if video_query:
        for video in video_query:
            print(video_query)
            print("request to save", video.resource_link, status)
            video.captioned = status
        aws_session.commit()

        return True

    else:
        return False


def write_submit_status(link, status, date):

    video_query = aws_session.query(iLearn_Video).filter_by(resource_link=link).all()

    if video_query:

        for video in video_query:

            video.submitted_for_processing = status
            video.submitted_for_processing_date = date
        aws_session.commit()
        ##! incomplete solution
        return True
    else:
        return False



def write_update_showdate(link, showdate, course_id):

    update_showdate = aws_session.query(iLearn_Video).filter_by(resource_link=link, course_id=course_id).all()

    if update_showdate:
        for video in update_showdate:
            video.indicated_due_date = showdate
        aws_session.commit()
        return True
    else:
        return False



def get_all_videos(semester):
    all_videos = []
    grouped_by_course_videos = aws_session.query(iLearn_Course).filter_by(semester=semester).all()

    for each_course in grouped_by_course_videos:
        for each_video in each_course.assigned_videos:
            all_videos.append(each_video)

    return all_videos


def update_video_title(url, title):

    titles_to_update = aws_session.query(iLearn_Video).filter_by(resource_link=url).all()

    for each_video in titles_to_update:
        each_video.title = title
        aws_session.commit()