from app import app
from flask import render_template, request, redirect
from app.customutils import Utils
from datetime import datetime
from google.cloud import datastore

datastore_client = datastore.Client()


@app.route('/home', methods=['GET', 'POST'])
def homepage():
    if request.method == 'GET':

        # Logged in user's user id
        USERID = request.cookies.get('user_id')

        # userInfo List to Display all users in searchbar
        userInfo = Utils.allUsersInfo()

        # list of users, logged in user is following
        allFollowingUsers = Utils.allFollowing(USERID)

        # Contains ID of all following users and logged in user
        User_Id_List = []
        User_Id_List.append(USERID)
        for userFollowing in allFollowingUsers:
            User_Id_List.append(userFollowing['following'])

        # This is correct
        print(User_Id_List)

        # User Data fetched by ID used for displaying posts
        followingUsersData = []
        for user in User_Id_List:
            followingUsersData.append(Utils.userInfoByID(userId=user))

        followingUserPosts = []
        for user in User_Id_List:
            followingUserPosts.extend(Utils.fetchPostsByUserId(userId=user))

        userImagesDict = Utils.getAllUserPostImages('')
        for item in followingUserPosts:
            image_path = item["imagePath"]
            if image_path in userImagesDict:
                item["image"] = userImagesDict[image_path]

        sorted_data = sorted(followingUserPosts,
                             key=lambda k: k['createdTime'], reverse=True)

        for item1 in sorted_data:
            for item2 in followingUsersData:
                if item1['userId'] == item2['userId']:
                    item1['name'] = item2['name']
                    item1['email'] = item2['email']

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
        # return {'data': allFollowingUsers}
        # return {'Posts': followingUserPosts}
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

        postData = Utils.fetchPostsByUserId(userId=urlID)

        userImagesDict = Utils.getAllUserPostImages(urlID)
        for item in postData:
            image_path = item["imagePath"]
            if image_path in userImagesDict:
                item["image"] = userImagesDict[image_path]

        sorted_data = sorted(
            postData, key=lambda k: k['createdTime'], reverse=True)

        for item1 in sorted_data:
            if item1['userId'] == userInfo['userId']:
                item1['name'] = userInfo['name']
                item1['email'] = userInfo['email']

        # return {'data': len(amIFollowingThisUser)}
        # return {"data": sorted_data, 'user': userInfo}
        return render_template('profilepage.html', data=sorted_data, userData=userInfo, myProfile=isThisMyProfile, amIFollowingThisUser=len(amIFollowingThisUser), totalNumberOfFollowers=totalNumberOfFollowers, totalNumberOfFollowing=totalNumberOfFollowing, totalPosts=len(sorted_data))


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
            if item["following"] == item2["userId"]:
                item.update(item2)
                break
    # return {'data': data}
    return render_template('following.html', data=data)
