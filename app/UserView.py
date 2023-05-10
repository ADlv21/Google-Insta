from app import app
from flask import render_template, request, redirect
from app.customutils import Utils
from google.cloud import datastore

datastore_client = datastore.Client()


@app.route('/home', methods=['GET', 'POST'])
def homepage():
    if request.method == 'GET':
        """
        Logged in user's user id
        """
        USERID = request.cookies.get('userId')

        """
        userInfo List to Display all users in searchbar
        """
        userInfo = Utils.allUsersInfo()

        """
        list of users, logged in user is following
        """
        allFollowingUsers = Utils.allFollowing(USERID)

        """
        Contains ID of all following users and logged in user
        """
        User_Id_List = []
        User_Id_List.append(USERID)
        for userFollowing in allFollowingUsers:
            User_Id_List.append(userFollowing['following'])

        """
        User Data fetched by ID used for displaying posts
        """
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

        sorted_data = sorted(followingUserPosts,key=lambda k: k['createdTime'], reverse=True)

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

        return render_template('homepage.html', userId=USERID, userData=userInfo, data=sorted_data)


@app.route('/user/<dynamicUserId>', methods=['GET', 'POST'])
def userProfilePage(dynamicUserId):
    USER_ID = request.cookies.get('userId')

    """
    Checks whether url user id in profile page matches with logged in user to decide to render follow/unfollow buttonn or not
    """
    isThisMyProfile = dynamicUserId == USER_ID

    """
    Checks wheter logged in user is following the user
    """
    amIFollowingThisUser = Utils.isUserFollowingTheUserId(userId=USER_ID, userIdToCheckForFollowing=dynamicUserId)

    if request.method == 'GET':
        userInfo = Utils.userInfoByID(dynamicUserId)

        totalNumberOfFollowers = len(Utils.allFollowers(userIdToCheckFollowersOf=dynamicUserId))

        totalNumberOfFollowing = len(Utils.allFollowing(userIdToCheckFollowingOf=dynamicUserId))

        postData = Utils.fetchPostsByUserId(userId=dynamicUserId)

        userImagesDict = Utils.getAllUserPostImages(dynamicUserId)
        for item in postData:
            image_path = item["imagePath"]
            if image_path in userImagesDict:
                item["image"] = userImagesDict[image_path]

        sorted_data = sorted(postData, key=lambda k: k['createdTime'], reverse=True)

        for item1 in sorted_data:
            if item1['userId'] == userInfo['userId']:
                item1['name'] = userInfo['name']
                item1['email'] = userInfo['email']

        #return {'d': postData}
        return render_template('profilepage.html',navbarData=USER_ID, data=sorted_data, userData=userInfo, myProfile=isThisMyProfile, amIFollowingThisUser=len(amIFollowingThisUser), totalNumberOfFollowers=totalNumberOfFollowers, totalNumberOfFollowing=totalNumberOfFollowing, totalPosts=len(sorted_data))


@app.route('/followuser/<userIdToFollow>', methods=['POST'])
def followUserById(userIdToFollow):
    """
    GETS USER ID FROM COOKIES
    """
    USER_ID = request.cookies.get('userId')

    """
    UNFOLLOW USER
    """
    if request.method == 'POST':
        result = Utils.followUserByUserId(userId=USER_ID, userIdToFollow=userIdToFollow)
        return redirect(f'/user/{userIdToFollow}')


@app.route('/unfollowuser/<userIdToUnFollow>', methods=['POST'])
def unFollowUserById(userIdToUnFollow):
    """
    GETS USER ID FROM COOKIES
    """
    USER_ID = request.cookies.get('userId')

    """
    UNFOLLOW USER
    """
    if request.method == 'POST':
        result = Utils.unFollowUserByUserId(userId=USER_ID, userIdToUnFollow=userIdToUnFollow)
        return redirect(f'/user/{userIdToUnFollow}')


@app.route('/user/<userIdToCheckFollowersOf>/followers')
def allFollowers(userIdToCheckFollowersOf):
    """
    Fetches all Followers users of current user
    """
    data = Utils.allFollowers(userIdToCheckFollowersOf=userIdToCheckFollowersOf)
    """
    Fetches every user's Data
    """
    users = Utils.allUsersInfo()

    """
    Matches User id in Follow Table's Followed_BY Column and UserId in UserProfile Table
    And appends data to get complete data on following user
    """
    for item in data:
        for item2 in users:
            if item["followed_by"] == item2["userId"]:
                item.update(item2)
                break
    return render_template('followers.html', data=data)


@app.route('/user/<userIdToCheckFollowingOf>/following')
def allFollowing(userIdToCheckFollowingOf):
    """
    Fetches all Following users of current user
    """
    data = Utils.allFollowing(userIdToCheckFollowingOf=userIdToCheckFollowingOf)
    """
    Fetches every user's Data
    """
    users = Utils.allUsersInfo()

    """
    Matches User id in Follow Table's Following Column and UserId in UserProfile Table
    And appends data to get complete data on following user
    """
    for item in data:
        for item2 in users:
            if item["following"] == item2["userId"]:
                item.update(item2)
                break
    return render_template('following.html', data=data)
