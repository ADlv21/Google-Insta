from app import app
from app.Models import User
from app.customutils import Utils
from flask import render_template


@app.route('/profile')
def userProfilePage():
    user = User(1, 'ad', 'ad@gmail.com', 'Hello Hi Im AD')
    print(user)
    return render_template('profilepage.html')
