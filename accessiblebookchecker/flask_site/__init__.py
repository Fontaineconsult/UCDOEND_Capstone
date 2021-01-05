

import sys
import os

sys.path.insert(0, "/vagrant/accessiblebookchecker")
sys.path.insert(0, "/vagrant/accessiblebookchecker/venv35/lib/python3.5/site-packages")
sys.path.append("/var/www/alt_media_services/site")
sys.path.append("C:\\Users\\DanielPC\\Desktop\\Servers\\alt_media_services\\accessiblebookchecker")
sys.path.append("/var/www/alt_media_services/lib/python3.6/site-packages")

current_dir = os.getcwd()
print(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))


from flask_site.application import app


if __name__ == '__main__':

    app.secret_key = "Super Secret Key"
    app.debug = False
    TEMPLATES_AUTO_RELOAD = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # app.config['LOGIN_DISABLED'] = True
    app.run(host='0.0.0.0', port=5000)
