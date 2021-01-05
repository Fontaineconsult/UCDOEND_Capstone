from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import class_mapper
Base = declarative_base()
from datetime import datetime

class iLearn_Course(Base):

    __tablename__ = 'courses'
    course_id = Column(String, primary_key=True)
    course_name = Column(String)
    course_gen_id = Column(String)
    semester = Column(String)
    no_students_enrolled = Column(Boolean)
    date_added = Column(DateTime, default=datetime.utcnow)
    assigned_videos = relationship('iLearn_Video', backref='courses')



    def make_dict(self):

        columns = [c.key for c in class_mapper(self.__class__).columns]
        videos = [c.key for c in class_mapper(self.__class__).relationships]
        course_info = dict((c, getattr(self, c)) for c in columns)
        test = dict((c, getattr(self, c)) for c in videos)
        video_list = [video.dict() for video in test['assigned_videos']]

        return {'course_info': course_info, 'video_list': video_list}


class iLearn_Video(Base):

    __tablename__ = 'videos'

    id = Column(Integer, primary_key=True)
    resource_type = Column(String)
    resource_link = Column(String)
    title = Column(String)
    scan_date = Column(DateTime, default=datetime.utcnow)
    length = Column(String)
    captioned = Column(Boolean)
    indicated_due_date = Column(DateTime)
    captioned_version_url = Column(String)
    course_id = Column(String, ForeignKey('courses.course_id'))
    course = relationship(iLearn_Course)
    submitted_for_processing = Column(Boolean)
    submitted_for_processing_date = Column(DateTime)
    page_section = Column(String)

    def dict(self):

        columns = [c.key for c in class_mapper(self.__class__).columns]
        return dict((c, getattr(self, c)) for c in columns)




engine = create_engine("postgresql://dev_environ:dev_environ@54.203.102.241/video_link_repo")
Base.metadata.create_all(engine)
DBsession = sessionmaker(bind=engine)
session = DBsession()




def get_ilearnvids_session():
    engine = create_engine("postgresql://dev_environ:dev_environ@54.203.102.241/video_link_repo")
    Base.metadata.create_all(engine)
    DBsession = sessionmaker(bind=engine)
    session = DBsession()
    return session









