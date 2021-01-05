from captioning.captioning_database.sf_cap_database.sf_cap_db_v2 import get_dbase_session, S3FileStorage



# session = get_dbase_session('aws_amp')

def add_file_to_db(source_url, key, url, object_uuid, file_name, sha_256_hash, mime_type):
    session = get_dbase_session('aws_amp')
    print(sha_256_hash)
    s3_object = S3FileStorage(source_url=source_url,
                              key=key,
                              object_url=url,
                              object_uuid=object_uuid,
                              file_name=file_name,
                              sha_256_hash=sha_256_hash,
                              mime_type=mime_type)

    session.add(s3_object)
    session.flush()
    new_id = s3_object.id
    session.commit()
    session.close()
    return new_id


def query_filename(filename):

    query = session.query(S3FileStorage).filter_by(file_name=filename).all()
    return query


def query_object_uuid(uuid):

    query = session.query(S3FileStorage).filter_by(object_uuid=uuid).all()
    return query


def query_source_url(source_url):
    query = session.query(S3FileStorage).filter_by(source_url=source_url).all()
    return query

