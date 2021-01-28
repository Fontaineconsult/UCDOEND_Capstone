import sys

sys.path.append('/usr/local/lib/python3.7/site-packages')

from flask import Flask
from flask_cors import CORS



app = Flask(__name__)

CORS(app, expose_headers='Content-Disposition') ##! Disable for production

# app.config.update({
#     'SECRET_KEY': 'SUPER_SECRET_KEY',
#     'SAML_METADATA_URL': 'https://dprc-amp-dev-ed.my.salesforce.com/.well-known/samlidp/Captioning_Verification.xml'
#
# })
#
# flask_saml.FlaskSAML(app)


# # from flask_site.captioning_api.api_routes import captioning_api_routes
# from flask_site.captioning_api.captioning_api_v1_routes import captioning_api_routes_v1
# from flask_site.captioning_api.captioning_api_v2_routes import captioning_api_routes_v2
# from flask_site.captioning_api.captioning_services_api_v1_routes import captioning_service_routes_v1
# from flask_site.pages.login_routes import login_routes
# from flask_site.pages.page_routes import page_routes
# # from flask_site.booksearch_api.book_search_api_routes import booksearch_api_routes
#
#
# app.register_blueprint(login_routes, url_prefix='/authentication')
# # app.register_blueprint(captioning_api_routes, url_prefix='/api/captioning')
# # app.register_blueprint(booksearch_api_routes, url_prefix='/api/booksearch')
# app.register_blueprint(captioning_api_routes_v1, url_prefix='/api/v1/captioning')
# app.register_blueprint(captioning_api_routes_v2, url_prefix='/api/v2/captioning')
# app.register_blueprint(captioning_service_routes_v1, url_prefix='/api/v2/captioning/services')
# app.register_blueprint(page_routes)


@app.route('/')
def index():
    return "One more test for good measure UDACITY CAPSTONE"
