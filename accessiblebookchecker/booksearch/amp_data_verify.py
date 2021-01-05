import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, exc
from booksearch.local_holdings import LocalHolding, Base
from time import sleep
'''
current_dir = os.getcwd()


engine = create_engine("postgresql://accessdb:accessdb@localhost/accessiblebooks")
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


def build_isbn_list():


    total_folders_parsed = 0
    with open(current_dir + "/Import Tools/textfile.txt", 'r') as isbn:
        for isbn_line in isbn:
            isbn_line = isbn_line.rstrip('\n')

            try:
                check_if_exists = session.query(LocalHolding).filter_by(isbn=isbn_line).one()
                print(check_if_exists.isbn, " already exists")
            except exc.NoResultFound:
                save_holding = LocalHolding(isbn=isbn_line)
                session.add(save_holding)
                session.commit()
                session.close()
                print("Success ", isbn_line)

    print('total folders parsed', total_folders_parsed)

def build_isbn_text_list():
    total_folders_parsed = 0
    path = "Z:\\Edit Files\\books"
    text_file_location = "C:\\Users\\913678186\\Box Sync\\SF State Python Projects\\Accessible Book Researcher\\Import Tools\\textfile.txt"


    for isbnfolder in os.listdir(path):
        total_folders_parsed += 1
        count = 0
        if len(isbnfolder) == 13:
            if os.path.isdir(os.path.join(path, isbnfolder)):
                for file in os.listdir(os.path.join(path, isbnfolder)):
                    count += 1
        if count > 0:
            sleep(0.005)
            with open(text_file_location, 'a') as new_line:
                new_line.write(str(isbnfolder + "\n"))
                print('writing ', isbnfolder)



    print('total folders parsed', total_folders_parsed)


def isbn_text():
    text_file_location = "C:\\Users\\913678186\\Box Sync\\SF State Python Projects\\Accessible Book Researcher\\Import Tools\\textfile.txt"
    with open(text_file_location, 'r') as isbn:
        for line in isbn:
            print(line.rstrip('\n'))
            
'''

