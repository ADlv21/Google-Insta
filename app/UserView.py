from app import app
from flask import render_template, request
from app.customutils import Utils
import uuid
from datetime import datetime
import time


@app.route('/home')
def homepage():
    return render_template('homepage.html')


@app.route('/addpost', methods=['GET', 'POST'])
def addUserPost():
    if request.method == 'GET':
        name = request.cookies.get('name')

        return render_template('addpost.html')

    if request.method == 'POST':

        # Generate a UUID and convert to string
        uuid_value = uuid.uuid4()
        uuid_string = str(uuid_value)

        # Get user id from cookies
        user_id = request.cookies.get('user_id')
        print(user_id)

        # Get form data
        caption = request.form['caption']
        image = request.files['image']

        IMAGE_PATH = user_id + '/' + uuid_string + image.filename
        # Carry out app logic
        postId = Utils.createUserPost(
            userId=user_id, caption=caption, imagePath=IMAGE_PATH, createdTime=int(time.time()))
        print("POST ID ====>>>>>>", postId)
        Utils.addUserPostImage(file=image, imagePath=IMAGE_PATH)
        return render_template('homepage.html')
