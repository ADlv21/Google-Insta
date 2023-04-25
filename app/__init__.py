from flask import Flask
from jinja2 import Environment, PackageLoader


app = Flask(__name__)
env = Environment(loader=PackageLoader(__name__, 'templates'))
env.filters['length'] = len
app.jinja_env = env

from app import Models
from app import LoginView
from app import UserView
from app import PostView
from app import customutils