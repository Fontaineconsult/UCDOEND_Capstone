"""
Need to remove this

"""



from captioning_database.sf_cap_db import CaptioningMedia,\
    CourseCaptioningJob, Course, get_dbase_session
from captioning_database.ilearn_scaped_videos_db import get_ilearnvids_session, iLearn_Course
from sqlalchemy.orm.exc import NoResultFound

cap_session = get_dbase_session()
ilearn_session = get_ilearnvids_session()


class CapInitializer:

    def __init__(self, iLearn_Video_Class):

        self.show_date = iLearn_Video_Class.indicated_due_date
        self.title = iLearn_Video_Class.title
        self.content_url = iLearn_Video_Class.resource_link
        self.ilearn_page_id = iLearn_Video_Class.course_id
        self.course_gen_id = iLearn_Video_Class.course.course_gen_id

        self.course_info = cap_session.query(Course).filter_by(course_gen_id=self.course_gen_id).first()


    def check_for_media(self):

        media_check = cap_session.query(CaptioningMedia).filter_by(source_url=self.content_url).first()
        if media_check:
            return media_check.id
        else:
            return False

    def check_for_job(self):
        media_id = self.check_for_media()

        if media_id:

            try:
                query = cap_session.query(CourseCaptioningJob).filter_by(media_id=media_id).all()
                return True
            except NoResultFound:
                return False
        else:
            return False

    def commit_captioning_job(self):


        job_check = self.check_for_job()

        if not job_check:

            captioning_media = CaptioningMedia(title=self.title,
                                               source_url=self.content_url,
                                               )
            cap_session.add(captioning_media)
            cap_session.flush()

            new_media_id = captioning_media.id

            cap_job = CourseCaptioningJob(media_id=new_media_id,
                                          show_date=self.show_date,
                                          course_id=self.course_info.course_gen_id)

            cap_session.add(cap_job)
            cap_session.commit()
        else:
            return False



class CourseVideos:

    def __init__(self, course_id):

        self.course_id = course_id
        self.course_query = ilearn_session.query(iLearn_Course).filter_by(course_id=self.course_id).first()
        self.initialized_videos = []
        self.initialize_videos()


    def initialize_videos(self):
        for iLearn_video in self.course_query.assigned_videos:
            self.initialized_videos.append(CapInitializer(iLearn_video))



course = CourseVideos("2564")


print(course.initialized_videos)