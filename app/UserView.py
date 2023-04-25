from app import app
from flask import render_template, request, redirect
from app.customutils import Utils
from datetime import datetime
from google.cloud import datastore

datastore_client = datastore.Client()


@app.route('/home', methods=['GET', 'POST'])
def homepage():
    if request.method == 'GET':

        USERID = request.cookies.get('user_id')

        # userInfo List to Display all users in searchbar
        userInfo = Utils.allUsersInfo()

        # Contains ID of all users in DB
        USER_ID_LIST = []
        for i in userInfo:
            USER_ID_LIST.append(i['id'])

        # User Data fetched by ID used for displaying posts
        USERIDLISTDATA = []
        for user in USER_ID_LIST:
            query = datastore_client.query(kind='Users')
            query.add_filter('user_id', '=', user)
            USERIDLISTDATA.append(list(query.fetch()))

        query = datastore_client.query(kind='Posts')
        results = list(query.fetch())

        data = []
        for result in results:
            data.append({
                "postId": result.key.id_or_name,
                "userId": result['userId'],
                "caption": result['caption'],
                "createdTime": datetime.fromtimestamp(result['createdTime']).strftime("%d/%m/%y %H:%M"),
                "imagePath": result['imagePath']
            })

        userImagesDict = Utils.getAllUserPostImages('')
        for item in data:
            image_path = item["imagePath"]
            if image_path in userImagesDict:
                item["image"] = userImagesDict[image_path]

        sorted_data = sorted(
            data, key=lambda k: k['createdTime'], reverse=True)

        for user in USERIDLISTDATA:
            for data in user:
                for post in sorted_data:
                    if data["user_id"] == post["userId"]:
                        post["email"] = data["email"]
                        post["name"] = data["name"]

        """
        FETCH COMMENTS
        """
        comm = Utils.fetchPostComments()
        comments = sorted(comm, key=lambda x: x['createdTime'], reverse=True)

        for post2 in sorted_data:
            for post1 in comments:
                if post1["postId"] == post2["postId"]:
                    if "comments" not in post2:
                        post2["comments"] = []
                    post2["comments"].append(post1)
        # print(sorted_data)
        # return {'sorted_data': sorted_data, 'comments': comm}
        # return {'data': userInfo}
        return render_template('homepage.html', userId=USERID, userData=userInfo, data=sorted_data)


@app.route('/user/<urlID>', methods=['GET', 'POST'])
def userProfilePage(urlID):
    USER_ID = request.cookies.get('user_id')

    isThisMyProfile = urlID == USER_ID
    print("This is my profile ? ", isThisMyProfile)

    amIFollowingThisUser = Utils.isUserFollowingTheUserId(
        userId=USER_ID, userIdToCheckForFollowing=urlID)

    if request.method == 'GET':
        # userInfo List to Display all users in searchbar
        userInfo = Utils.userInfoByID(urlID)

        totalNumberOfFollowers = len(
            Utils.allFollowers(userIdToCheckFollowersOf=urlID))

        totalNumberOfFollowing = len(
            Utils.allFollowing(userIdToCheckFollowingOf=urlID))

        # Contains ID of all users in DB
        USER_ID_LIST = []
        for i in userInfo:
            USER_ID_LIST.append(i['id'])

        # User Data fetched by ID used for displaying posts
        USERIDLISTDATA = []
        for user in USER_ID_LIST:
            query = datastore_client.query(kind='Users')
            query.add_filter('user_id', '=', user)
            USERIDLISTDATA.append(list(query.fetch()))

        query = datastore_client.query(kind='Posts')
        query.add_filter('userId', '=', urlID)
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

        userImagesDict = Utils.getAllUserPostImages(urlID)
        for item in data:
            image_path = item["imagePath"]
            if image_path in userImagesDict:
                item["image"] = userImagesDict[image_path]

        sorted_data = sorted(
            data, key=lambda k: k['createdTime'], reverse=True)

        for user in USERIDLISTDATA:
            for data in user:
                for post in sorted_data:
                    if data["user_id"] == post["userId"]:
                        post["email"] = data["email"]
                        post["name"] = data["name"]

        # return {'data': len(amIFollowingThisUser)}
        # return {"data": userInfo}
        return render_template('profilepage.html', data=sorted_data, userData=userInfo[0], myProfile=isThisMyProfile, amIFollowingThisUser=len(amIFollowingThisUser), totalNumberOfFollowers=totalNumberOfFollowers, totalNumberOfFollowing=totalNumberOfFollowing, totalPosts=len(sorted_data))

    if request.method == 'POST':
        return render_template()


@app.route('/followuser/<userIdToFollow>', methods=['POST'])
def followUserById(userIdToFollow):
    USER_ID = request.cookies.get('user_id')

    if request.method == 'POST':
        result = Utils.followUserByUserId(
            userId=USER_ID, userIdToFollow=userIdToFollow)
        return redirect(f'/user/{userIdToFollow}')


@app.route('/unfollowuser/<userIdToUnFollow>', methods=['POST'])
def unFollowUserById(userIdToUnFollow):
    USER_ID = request.cookies.get('user_id')

    if request.method == 'POST':
        result = Utils.unFollowUserByUserId(
            userId=USER_ID, userIdToUnFollow=userIdToUnFollow)
        return redirect(f'/user/{userIdToUnFollow}')


@app.route('/user/<userIdToCheckFollowersOf>/followers')
def allFollowers(userIdToCheckFollowersOf):

    data = Utils.allFollowers(
        userIdToCheckFollowersOf=userIdToCheckFollowersOf)
    users = Utils.allUsersInfo()

    for item in data:
        for item2 in users:
            if item["followed_by"] == item2["userId"]:
                item.update(item2)
                break
    # return {'data': data}
    return render_template('followers.html', data=data)


@app.route('/user/<userIdToCheckFollowingOf>/following')
def allFollowing(userIdToCheckFollowingOf):

    data = Utils.allFollowing(
        userIdToCheckFollowingOf=userIdToCheckFollowingOf)
    users = Utils.allUsersInfo()

    for item in data:
        for item2 in users:
            if item["followed_by"] == item2["userId"]:
                item.update(item2)
                break
    # return {'data': data}
    return render_template('following.html', data=data)
