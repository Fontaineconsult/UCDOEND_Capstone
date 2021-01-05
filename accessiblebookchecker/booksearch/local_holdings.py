from sqlalchemy import Column,Integer,String, ForeignKey, DateTime, orm
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker, exc


Base = declarative_base()



class LocalHolding(Base):

    __tablename__ = 'holding'
    id = Column(Integer, primary_key=True)
    isbn = Column(String(15), unique=True)
    title = Column(String)
    author = Column(String)
    edition = Column(String)


class Textbooks(Base):

    __tablename__ = 'textbooks'
    id = Column(Integer, primary_key=True)
    isbn = Column(String(13))
    title = Column(String)
    section = Column(String)
    subject = Column(String)
    catalog = Column(String)
    instructor = Column(String)
    publisher = Column(String)
    author = Column(String)
    edition = Column(String)
    status = Column(String)
    course_name = Column(String)




#
# engine = create_engine("postgresql://accessdb:accessdb@localhost/accessiblebooks")
# Base.metadata.create_all(engine)
# DBSession = sessionmaker(bind=engine)
# search_session = DBSession()


def get_book(isbn):

    try:
        search = search_session.query(LocalHolding).filter_by(isbn=isbn).first()
        search_session.commit()
        return search
    except exc.NoResultFound:

        return False


def textbook_query(isbn):

    try:
        textbook_query = search_session.query(Textbooks).filter(Textbooks.isbn.ilike(isbn + '%')).order_by(asc(Textbooks.isbn)).limit(20)
        search_session.commit()
        return textbook_query
    except exc.NoResultFound:
        return False

def coure_name_query(course_name):

    try:
        course_name_query = search_session.query(Textbooks).filter(Textbooks.course_name.ilike(course_name + '%')).order_by(asc(Textbooks.course_name)).limit(20)
        search_session.commit()
        return course_name_query
    except exc.NoResultFound:
        return False

