
import logging
import sys
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/capstone/site/')
from accessiblebookchecker.flask_site import app as application
application.secret_key = 'Super Secret Key'