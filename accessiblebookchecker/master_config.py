import os
import configparser
from pathlib import Path

path = Path(os.path.dirname(__file__))

local_config = configparser.ConfigParser()
local_config.sections()
local_config.read(os.path.join(str(path.parent), 'local.cfg'))

deployed = local_config['env']['environment'] != 'development'


server_config = {
    'dev_server_port': '5000',
    'local_server': local_config['server']['server'],
    'dev_server': 'http://localhost:5000',
    'deployment_server': 'https://www.amp-dev.sfsu.edu',
    'login_disabled': local_config.getboolean('login','login_disabled')
}


database_config = {
    'schema': 'postgresql',
    'user': 'daniel',
    'password': 'accessiblevids',
    'server': '130.212.104.17',
    'database': local_config['database']['database'],

}


file_config = {
    'root': os.path.abspath(os.path.dirname(__file__)),  # location of this config file
    'temp_upload_files': "/captioning/app_file_manager/video_temp/",
    'temp_text_files': "/captioning/app_file_manager/text_temp/"

    }

aws_config = {

    'access_key_ID': "AKIATVWJFSM5S5NVQJXE",
    'secret_access_key': "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",
    's3_service_url': "https://amp-video-storage.s3-us-west-2.amazonaws.com",
    's3_storage_bucket': "amp-video-storage",
    's3_srt_storage_bucket': "srt-storage",
    's3_transcript_storage_bucket': "transcript-storage",
    's3_video_storage_folder': "video-storage",

}


ast_endpoints = {
    'sandbox_authentication_url': 'https://sandboxapi.automaticsync.com/v1/authenticate',
    'sandbox_submissions_url':  'https://sandboxapi.automaticsync.com/v1/submissions',
    'sandbox_lists_url': 'https://sandboxapi.automaticsync.com/v1/lists',

    'live_authentication_url': 'https://api.automaticsync.com/v1/authenticate',
    'live_submissions_url': 'https://api.automaticsync.com/v1/submissions',
    'live_lists_url': 'https://api.automaticsync.com/v1/lists'


}

ast_account_credentials = {

    'live_customer_id': 'dfontaine',
    'live_partner_type': 'dprcCaptioningManager',
    'live_customer_secret': '227a15fb60130652e81578a931000467f5d26060870b69c93a5405bc8d338d47',

    'sandbox_customer_id': 'sfsudev',
    'sandbox_partner_type': 'dprcCaptioningManagerTest',
    'sandbox_customer_secret': '37533m4AC-1088b9F50BF-1671w3-78B12e3',
}


ast_credentials = {

    'token': "Bearer 7048d1179fecde472a6ce01145b92699f09a729762894de6620acb1bdfc7049b55a65b735f9d8c2ca1224742a85a48c5-13e864bf-f1b3-11e8-ab84-00505602114a",
    'app': 'Captioning',

    'sandbox_customer_id': 'sfsudev',
    'sandbox_partner_type': 'dprcCaptioningManagerTest',
    'sandbox_customer_secret': '37533m4AC-1088b9F50BF-1671w3-78B12e3',

    # 'sandbox_authentication_url': 'https://sandboxapi.automaticsync.com/v1/authenticate',
    # 'sandbox_submissions_url':  'https://sandboxapi.automaticsync.com/v1/submissions',
    # 'sandbox_lists_url': 'https://sandboxapi.automaticsync.com/v1/lists',

    'live_customer_id': 'dfontaine',
    'live_partner_type': 'dprcCaptioningManager',
    'live_customer_secret': '227a15fb60130652e81578a931000467f5d26060870b69c93a5405bc8d338d47',

    'customer_id': ast_account_credentials['sandbox_customer_id'] if not deployed else ast_account_credentials['live_customer_id'],
    'partner_type': ast_account_credentials['sandbox_partner_type'] if not deployed else ast_account_credentials['live_partner_type'],
    'customer_secret': ast_account_credentials['sandbox_customer_secret'] if not deployed else ast_account_credentials['live_customer_secret'],

    'authentication_url': ast_endpoints['sandbox_authentication_url'] if not deployed else ast_endpoints['live_authentication_url'],
    'submissions_url': ast_endpoints['sandbox_submissions_url'] if not deployed else ast_endpoints['live_submissions_url'],
    'lists_url': ast_endpoints['sandbox_lists_url'] if not deployed else ast_endpoints['live_lists_url'],

}



ast_default = {

    'ast_description': 'DPRC AMP Submission',
    'ast_language': 'English',
    'ast_rush': 'T',
    'ast_have_trans': False,
    'ast_notes': '',
    'ast_persistent_note': '',
    'ast_purchase_order': '',
    'ast_callback': "{}{}".format(server_config['local_server'], "/api/v2/captioning/services/upload/caption"),
    'ast_status': "{}{}".format(server_config['local_server'], "/api/v2/captioning/services/status")

}


sfsu_ops_postgres = {
    'server': '130.212.104.17',
    'user': 'daniel',
    'password': 'accessiblevids',
    'dev_database': 'captioning_v2_dev'

}


sfsu_box_credentials = {
    "boxAppSettings": {
        "clientID": "zamp86vr1wge5m2p5txtmwiyv0sfwtes",
        "clientSecret": "clypFeeezcp48KDE8rUEuLtaSzjHDqTd",
        "appAuth": {
            "publicKeyID": "t3glgw3g",
            "privateKey": "-----BEGIN ENCRYPTED PRIVATE KEY-----\nMIIFDjBABgkqhkiG9w0BBQ0wMzAbBgkqhkiG9w0BBQwwDgQIIUUuheyb/CsCAggA\nMBQGCCqGSIb3DQMHBAgfj62B+phBzQSCBMiQhqnJpvX4RKD6csPnoHAzp3nhOUCX\nqaeVjJnYN6KLjSO8k4v7hktvKbNqyh/X+yfoqJrGeHfZDA+IFjhN/if4stjxtH5N\nvGG5mlyX9/G19WnFgTkEA5e08QT4M4Q8HKRBeKW6pltTJIsMYWAiGgCBXhI5oMU5\nfLiWfC+ez8awnXOoc1oXBz/YsdYyUmnU7jA60Y+GSVB3YWNF/57q/u8bcWcS8btW\nq4zUyv5A1JuMQEq45EtrqK/meS3jhSIx6TM/foLdGuVQ3Dgqac9QUh1ceDoxnH3z\ntCqM+6iFkIhFMnNkXTUFps8Ik+HPYa1B4n8zW+cf8i35K2PNdAidzHjwoxrU9ziP\nMIYgG89ElChdQJvE/QusfDhbxCyXgK0ApgK5Skoc04eQ4EzClBt7HaXGL4gR5/oj\nWAlqVWmYxBRbFLTJKNouhOgx2fVJSIVzn2PqGwZMD22J80B39/09L79BCbpFZPQz\n8fmW9h1Uvmm846l0nGV3wXODEqAcgYq8cGSYheF1nXfnvuIOuRxbbJmBVw6meimU\nLo+VWZs4WM+XSjBf3Oy+/Syropw/iCar6FaFs/+ppMHXNBvqsUbQe5r9gBGSyxLh\nKnH4zDnoQ+rDvXKxy7w3Q+VtjEr3QRcMkAAWxhicjud1IRJTjVQryoPSYXseqT3r\nZcfvKlZj7zO69BS6E8rSgMArZ3BavMYRzK8rJ9y97AWv9V+YHEZEOb/3EgLYjEbt\n3uoYSwJPzthUGLn4WMi6ixsQCQXwgxyVbDyRmsCOdjlsALxfcmmGb+hZb9wC4Rmq\n1Ur1lIHVnYRSf8TFgTx87DZfv1FP3mFoVVn3FnjbITn8bHamhMvYPsa5iqeLkKFc\nXPH+XSkCJahFTtC5uWzF/i0G1j/icN8fm+13OMbeC6WblyegPv5rBvWn2bM6CmUq\ndx/jtYMGcqEZiZjuSKyz/qs2lVTnKa4nfJxZAKBglfcUaMM8kQ2/m3yfr79+KqxQ\nR/XY2ar8ZZreHi7AXJg8viA2IknbSC/z77Yr5GxGCtwqpxvJaYEtltEgV6Y4X5oN\nx19QuldstkWH5CivkFTdDkHlN527hYxp7rFNpZk/x8bTCtA3NBPNKZP3IeBWamih\nxmZGqwfmW4VmXRESvZucn4yj3RZ3eMODcfOaBPDbK1PIv2GoZjcI2iBwogwHIGL6\nmtFpHKGlnTVwoLVrJUnRHwMNw9ddQCZ1T66FDOf41I8gL/PuAEHyaSW7Q7gbKlQc\njWy/YpfvcA3m3H0ZBw0ry9ZfcxoPIobNpk/JEcyBczRa2xGKgOLq0bi5KkJOGfUM\nicvw25CQ7W6yxrjavOsx/c2U1QF9NHsKPNu9zv7Dts3Bm7IyHnabITL1yz3EshOB\n3TC3ekDHeu1aGJr+NDsXzWvDYjKDC92ysR0IEoR0MirOOb+0nw1mpi/CQoSUbmpn\nSkmnk6JuyOkWkKpKHdi2j36piFeUHJO4WsLBgYDIeucPAO+dNFal00ojYKnX8O9V\nhgCbwjLH7txQZVvVdNPeooYnSyzqC5z2EwCMwDrza5m35H35Yb46x19u0wduMs6Y\nLmQARO37LjpTXfL0v7QSuiP+143H7t6iznzbaRMHPbXQs3cmmNmwih0W2yTP/Lr8\nNcw=\n-----END ENCRYPTED PRIVATE KEY-----\n",
            "passphrase": "fe0533503e95636e5c4567bd23dbd4fa"
        }
    },
    "enterpriseID": "281439"
}

amara_credentials = {

    "amara_user_id": 'captions2',
    "amara_key": "c639e50c5ac807d3dd828396ce23b08c1143bf80",
    "amara_api": "https://amara.org/api/videos/"


}

youtube = {

    "api_key": "AIzaSyBadsh-FNX__wwDc4p1rVUQG-8qKgNHcrs",
    "api_key_backup": "AIzaSyD5wYmKq-d7Mq_pcqHx47sLe5dW4FTud6Q"
}

vimeo_credentials = {

    'client_identifier': "923611fe4bc05060cbe0496f5a4ce50b6b27c8f9",
    'client_secret': "ffB+H74wxDWECvm41WhQmYcc8O+rmlIhR4dQMCaeGKXiD7yjMO9vgyC6E6nY0kqJXGEZ0WTIUpF2STQaon/cuBiGlGgQLbJErUyyyPwi9qG52Ug7ZWjQPMt1mBPgvHHP",


}