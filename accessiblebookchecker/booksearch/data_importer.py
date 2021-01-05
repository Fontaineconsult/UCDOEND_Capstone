from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from booksearch.local_holdings import Base, Textbooks
import csv, os
import traceback


engine = create_engine("postgresql://accessdb:accessdb@54.203.102.241/accessiblebooks")
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()



current_dir = os.getcwd()
print(current_dir)
csv_file = os.path.join(current_dir, "C:\\Users\\913678186\\Box\\Servers\\accessiblebookchecker\\booksearch\\data\\textbook.csv")

def open_reader():
    with open(csv_file, "r", encoding="ISO-8859-1") as f:

        reader = csv.reader(f)

        for row in reader:

            print(row[4], row[5], row[6], row[7], row[8], row[14], row[15], row[16], row[17], row[18])
            textbook = Textbooks(isbn=row[16],
                                 title=row[15],
                                 section=row[4],
                                 subject=row[5],
                                 catalog=row[6],
                                 instructor=row[8],
                                 publisher=row[18],
                                 author=row[17],
                                 edition=row[20],
                                 status=row[14],
                                 course_name=row[5].replace(" ", "_") + "_" + row[6].replace(" ", "") + "." + row[4])

            session.add(textbook)
            session.commit()





def update_records():
    try:
        print("UPDATING")
        rows_to_delete = session.query(Textbooks).delete()
        session.commit()
        open_reader()
    except:
        print("ROLLBACK", traceback.print_exc())
        session.rollback()
    session.close()





update_records()

        

