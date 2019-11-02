import boto3
from flask_bcrypt import Bcrypt
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_dance.contrib.google import make_google_blueprint, google

app = Flask(__name__) # Flask app init
s3 = boto3.resource('s3') # S3 bucket resource
buckets = s3.buckets.all() # List all the buckets. I don't think I need this here.
my_bucket = s3.Bucket('whybucket1') # Put this as an environment variable later
app.config['SECRET_KEY'] = 'asecretkey' # Put this as an environment variable later
bcrypt = Bcrypt() # Hash stuff. I don't think I need this here.
login_manager = LoginManager() # Login manager.
file_storage = my_bucket.objects.all() # All the objects in my bucket.

"""
blueprint = make_google_blueprint(
    client_id="######.apps.googleusercontent.com",
    client_secret="####",
    # reprompt_consent=True,
    offline=True,
    scope=["profile", "email"]
)
app.register_blueprint(blueprint, url_prefix="/login")
"""
DB_CONSTANT = None
app.config['SQLALCHEMY_DATABASE_URI'] = DB_CONSTANT # Database endpoint. Put the endpoint in an env variable.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

login_manager.init_app(app)
login_manager.login_view = 'login'
