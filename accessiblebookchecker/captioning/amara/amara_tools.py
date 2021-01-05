from captioning.captioning_database.sf_cap_database.sf_cap_db_v2 import get_dbase_session, AmaraResources,\
    CaptioningMedia, CaptionedResources
from captioning.amara.amara_methods import check_source_video
import re, time


def _check_record_amara(url):

    session = get_dbase_session("Amara Updater")
    media = session.query(CaptioningMedia).filter_by(source_url=url).all()

    for each in media:

        # first check if media ID is in CapReources
        if not session.query(CaptionedResources).filter(CaptionedResources.media_id==each.id,
                                                        CaptionedResources.amara_id != None).scalar():
            # see if record exists in amara
            amara_check = check_source_video(each.source_url)
            if amara_check:

                # if it has published captions
                if len(amara_check['languages']) > 0:
                    expected_result = [d for d in amara_check['languages'] if d['code'] == 'en' and d['published'] == True]
                    if len(expected_result) > 0:
                        new_amara = AmaraResources(
                            url="https://amara.org/en/videos/{}".format(amara_check['id']),
                            title=amara_check['title'],
                            video_id=amara_check['id'],
                            captions_complete=True,
                            captions_uploaded=True
                        )
                        session.add(new_amara)
                        session.flush()
                        new_amara_record_id = new_amara.id

                        new_cap_resource = CaptionedResources(
                            media_id=each.id,
                            amara_id=new_amara_record_id
                        )

                        session.add(new_cap_resource)
                        session.commit()
                        session.close()
                        return True
                else:
                    return False
            return False
        return False


def check_record_for_amara_resource(url):
    youtube_regex = re.compile(r"^(http:\/\/|https:\/\/)(vimeo\.com|youtu\.be|www\.youtube\.com)\/([\w\/]+)([\?].*)?$")
    you_tube_check = youtube_regex.match(url)
    if you_tube_check is not None:
        return _check_record_amara(url)


