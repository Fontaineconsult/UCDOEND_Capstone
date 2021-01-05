from flask import Blueprint, redirect
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_site.application import app
from flask_sqlalchemy import SQLAlchemy
from master_config import database_config, server_config

schema = database_config['schema']
user = database_config['user']
password = database_config['password']
server = database_config['server']
database = database_config['database']

connection = "{}://{}:{}@{}/{}".format(schema, user, password, server, database)

print(connection)

app.config['SQLALCHEMY_DATABASE_URI'] = connection
app.config['SECRET_KEY'] = "Super Secret Key"
app.config['LOGIN_DISABLED'] = server_config['login_disabled']
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 280, 'pool_timeout': 100, 'pool_pre_ping': True}


login_manager = LoginManager()
login_manager.init_app(app)
db = SQLAlchemy(app)





login_routes = Blueprint('login_routes', __name__)


class Users(UserMixin, db.Model):

    __table_args__ = {"schema":"main_1"}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, unique=True)



@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


@login_routes.route('/login')
def login():
    user = Users.query.filter_by(user_id='913678186').first()
    login_user(user)
    return redirect('/captioning/job-manager?id=913678186')




@login_routes.route('/logout')
@login_required
def logout():
    logout_user()
    return "You Are Logged out"


@login_routes.route("/home")
@login_required
def home():
    return "The current user is " + current_user.user_id
