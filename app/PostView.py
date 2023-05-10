from app import app
from app.customutils import Utils
from flask import request, render_template, redirect
import time
import uuid


@app.route('/addpost', methods=['GET', 'POST'])
def addUserPost():
    USER_ID = request.cookies.get('userId')

    if request.method == 'GET':
        return render_template('addpost.html')

    if request.method == 'POST':

        """
        Generate a UUID and convert to string
        """
        uuid_value = uuid.uuid4()
        uuid_string = str(uuid_value)

        """
        Get Form data from HTML
        """
        caption = request.form['caption']
        image = request.files['image']

        IMAGE_PATH = USER_ID + '/' + uuid_string + image.filename
        postId = Utils.createUserPost(userId=USER_ID, caption=caption, imagePath=IMAGE_PATH, createdTime=int(time.time()))
        Utils.addUserPostImage(file=image, imagePath=IMAGE_PATH)
        return redirect('/home')


@app.route('/post/comment/<postId>', methods=['POST'])
def addCommentToPost(postId):

    if request.method == 'POST':
        USER_ID = request.cookies.get('userId')
        EMAIL = request.cookies.get('email')
        NAME = request.cookies.get('name')
        
        comment = request.form.get('comment')
        
        result = Utils.addCommentToPost(createdTime=int(time.time()), userId=USER_ID, postId=int(postId), comment=comment, email=EMAIL, name=NAME)
        print(result)
        return redirect('/home')
