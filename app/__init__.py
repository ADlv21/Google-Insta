from flask import Flask

app = Flask(__name__)

from app import Models
from app import LoginView
from app import UserView
from app import ProfileView
from app import customutils