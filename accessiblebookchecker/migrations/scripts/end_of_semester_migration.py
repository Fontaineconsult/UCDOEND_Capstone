from sqlalchemy import create_engine
from sqlalchemy.sql import text
import psycopg2.errors
import os
import sqlalchemy.exc
from master_config import database_config


schema = database_config['schema']
user = database_config['user']
password = database_config['password']
server = database_config['server']
database = database_config['database']

connection = "{}://{}:{}@{}/{}".format(schema, user, password, server, database)

term_code = '2213'
semester_code = 'sp21'

def drop_all_connections(conn):
    print("Dropping Active Connections to {}".format(database))
    engine = create_engine(conn, echo=True)
    db_connection = engine.connect()
    file = open("../sql/terminate_backend_connections.sql")
    query = text(file.read().format(database))
    try:
        db_connection.execute(query)
    except (psycopg2.errors.AdminShutdown, sqlalchemy.exc.OperationalError):
        pass

def create_new_database(target, conn=connection, source=database):
    print("Creating New Database Based on {}".format(database))
    engine = create_engine(conn, echo=True)
    db_connection = engine.connect()
    file = open("../sql/end_of_semester_migration.sql")
    query = text(file.read().format(target, source))
    db_connection.connection.connection.set_isolation_level(0)
    db_connection.execute(query)
    db_connection.connection.connection.set_isolation_level(1)

def dump_db(source=database):
    print("Dumping {} to Local".format(source))
    source_conn = "{}://{}:{}@{}/{}".format(schema, user, password, server, source)
    pg_dump_process = r"pg_dump --dbname={} > C:\Users\DanielPC\Desktop\Servers\alt_media_services\accessiblebookchecker\migrations\temp\cap_temp.sql".format(source_conn)
    os.system(pg_dump_process)

def restore_db(target):
    print("Restoring Dumped .SQL to New Database, {}".format(target))
    target_conn = "{}://{}:{}@{}/{}".format(schema, user, password, server, target)
    pg_restore_process = r"pg_restore --exit-on-error -v --dbname={} > C:\Users\DanielPC\Desktop\Servers\alt_media_services\accessiblebookchecker\migrations\temp\cap_temp.sql".format(target_conn)
    os.system(pg_restore_process)


def update_views(term_code, semester_code, target):
    print("Updating Views")
    target_conn = "{}://{}:{}@{}/{}".format(schema, user, password, server, target)
    engine = create_engine(target_conn, echo=True)
    db_connection = engine.connect()
    current_enrollement_sql_file = open("../sql/current_enrollement_def.sql")
    current_enrollement_query = text(current_enrollement_sql_file.read().format(term_code))
    db_connection.execute(current_enrollement_query)
    current_enrollement_sql_file.close()
    current_student_courses_sql_file = open("../sql/current_student_courses_def.sql")
    current_student_courses_query = text(current_student_courses_sql_file.read().format(semester_code))
    db_connection.execute(current_student_courses_query)
    current_student_courses_sql_file.close()


def migrate_db(target):
    input("WARNING: running this process will disconnect all active connections. Press Key to Continue")
    dump_db()
    drop_all_connections(connection)
    create_new_database(target, connection)
    restore_db(target)
    update_views(term_code, semester_code, target)
    print("Migration Complete")


if __name__ == '__main__':
    migrate_db("captioning_v2_live_spring2021")


