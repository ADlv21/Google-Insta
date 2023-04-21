from app import app
from flask import render_template, request
from app.customutils import Utils
import uuid
from datetime import datetime
import time
from google.cloud import datastore

BUCKET_NAME = 'insta-cloud-384319.appspot.com'
datastore_client = datastore.Client()


@app.route('/home')
def homepage():
    return render_template('homepage.html')


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
        return render_template('homepage.html')


@app.route('/profile', methods=['GET'])
def userProfilePage():
    USER_ID = request.cookies.get('user_id')

    if request.method == 'GET':
        USER_NAME = request.cookies.get('name')
        EMAIL = request.cookies.get('email')

        query = datastore_client.query(kind='Posts')
        query.add_filter('userId', '=', USER_ID)
        results = list(query.fetch())

        data = []
        for result in results:
            data.append({
                "postId": result.key.id_or_name,
                "userId": result['userId'],
                "imagePath": result['imagePath'],
                "caption": result['caption'],
                "createdTime": datetime.fromtimestamp(result['createdTime']).strftime("%Y-%m-%d %H:%M")
            })

        userImagesDict = Utils.getAllUserPostImages(USER_ID)
        for item in data:
            image_path = item["imagePath"]
            if image_path in userImagesDict:
                item["image"] = userImagesDict[image_path]

        # return data
        return render_template('profilepage.html', data=data, name=USER_NAME, email=EMAIL)
