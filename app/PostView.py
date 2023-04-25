from app import app
from app.customutils import Utils
from flask import request, render_template, redirect
import time
import uuid


@app.route('/addpost', methods=['GET', 'POST'])
def addUserPost():
    USER_ID = request.cookies.get('user_id')

    if request.method == 'GET':
        return render_template('addpost.html')

    if request.method == 'POST':

        # Generate a UUID and convert to string
        uuid_value = uuid.uuid4()
        uuid_string = str(uuid_value)

        # Get form data
        caption = request.form['caption']
        image = request.files['image']

        IMAGE_PATH = USER_ID + '/' + uuid_string + image.filename
        # Carry out app logic
        postId = Utils.createUserPost(
            userId=USER_ID, caption=caption, imagePath=IMAGE_PATH, createdTime=int(time.time()))
        print("POST ID ====>>>>>>", postId)
        Utils.addUserPostImage(file=image, imagePath=IMAGE_PATH)
        return redirect('/home')


@app.route('/post/comment/<postId>', methods=['POST'])
def addCommentToPost(postId):

    if request.method == 'POST':
        USERID = request.cookies.get('user_id')
        EMAIL = request.cookies.get('email')
        NAME = request.cookies.get('name')
        
        comment = request.form.get('comment')
        
        result = Utils.addCommentToPost(createdTime=int(
            time.time()), userId=USERID, postId=int(postId), comment=comment, email=EMAIL, name=NAME)
        print(result)
        return redirect('/home')
