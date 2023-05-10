from google.cloud import storage
from google.cloud import datastore
import base64
from datetime import datetime
from PIL import Image
from io import BytesIO
from app.local_constants import PROJECT_STORAGE_BUCKET, SERVICE_ACCOUNT_JSON

BUCKET_NAME = PROJECT_STORAGE_BUCKET
client = datastore.Client()


class Utils:

    def fetchPostsByUserId(userId):
        query = client.query(kind='UserPosts')
        query.add_filter('userId', '=', userId)
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
        return data

    def addUserPostImage(file, imagePath: str):
        # Connect to Google Cloud Storage
        client = storage.Client.from_service_account_json(SERVICE_ACCOUNT_JSON)
        bucket = client.bucket(BUCKET_NAME)

        # Create new blob and upload file to blob
        blob = bucket.blob(imagePath)
        blob.upload_from_string(file.read(), content_type=file.content_type)


    def createUserPost(createdTime, userId, caption, imagePath):
        entity = datastore.Entity(key=client.key('UserPosts'))
        entity.update(
            {
                'userId': userId,
                'caption': caption,
                'imagePath': imagePath,
                'createdTime': createdTime
            }
        )
        client.put(entity)
        return entity.key.id

    def fetchPostComments():
        query = client.query(kind='Comments')
        query.order = ['-createdTime']
        results = list(query.fetch())
        commentData = []
        for result in results:
            commentData.append({
                'userId': result['userId'],
                'name': result['name'],
                'email': result['email'],
                'comment': result['comment'],
                'postId': result['postId'],
                'createdTime': result['createdTime']
            })
        return commentData

    """
    IMAGES
    """

    def getAllUserPostImages(username):
        storage_client = storage.Client().from_service_account_json(SERVICE_ACCOUNT_JSON)

        bucket = storage_client.get_bucket(BUCKET_NAME)
        files = list(bucket.list_blobs(prefix=username))

        image_bytes = []

        fileNames = []

        for f in files:
            fileNames.append(f.name)
            blob_content = f.download_as_bytes()
            image_bytes.append(Image.open(
                BytesIO(blob_content)).convert('RGB'))

        # Convert the list of PIL images to base64-encoded strings
        encoded_images = []
        for image in image_bytes:
            buffered = BytesIO()
            image.save(buffered, format='JPEG')
            encoded_image = base64.b64encode(
                buffered.getvalue()).decode('utf-8')
            encoded_images.append(encoded_image)

        result_dict = {fileNames[i]: encoded_images[i]
                       for i in range(len(fileNames))}

        return result_dict

    def allUsersInfo():
        query = client.query(kind='UserProfile')
        results = list(query.fetch())
        userInfo = []
        for result in results:
            userInfo.append({
                "id": result.key.id_or_name,
                "email": result['email'],
                "userId": result['userId'],
                "name": result['name']
            })
        return userInfo

    def userInfoByID(userId):
        query = client.query(kind='UserProfile')
        query.add_filter('userId', '=', userId)
        results = list(query.fetch())
        userInfo = []
        for result in results:
            userInfo.append({
                "id": result.key.id_or_name,
                "email": result['email'],
                "userId": result['userId'],
                "name": result['name']
            })
        return userInfo[0]

    """
    FOLLOW USER BY ID
    """
    def followUserByUserId(userId, userIdToFollow):
        entity = datastore.Entity(key=client.key('FollowTable'))
        entity.update(
            {
                'following': userIdToFollow,
                'followed_by': userId,
            }
        )
        client.put(entity)
        return {
            'following': userIdToFollow,
            'followed_by': userId,
        }

    """
    UNFOLLOW USER BY ID
    """
    def unFollowUserByUserId(userId, userIdToUnFollow):

        query = client.query(kind='FollowTable')
        query.add_filter('followed_by', '=', userId)
        query.add_filter('following', '=', userIdToUnFollow)
        results = list(query.fetch())
        followingInfo = []
        for result in results:
            followingInfo.append({
                "id": result.key.id_or_name,
                "followed_by": result['followed_by'],
                "following": result['following'],
            })

        entity = client.key('FollowTable', followingInfo[0]['id'])
        client.delete(entity)
        return {'Data': followingInfo[0]['id']}

    def isUserFollowingTheUserId(userId, userIdToCheckForFollowing):
        query = client.query(kind='FollowTable')
        query.add_filter('followed_by', '=', userId)
        query.add_filter('following', '=', userIdToCheckForFollowing)
        results = list(query.fetch())
        userInfo = []
        for result in results:
            userInfo.append({
                "id": result.key.id_or_name,
                "followed_by": result['followed_by'],
                "following": result['following']
            })

        return userInfo

    def allFollowers(userIdToCheckFollowersOf):
        query = client.query(kind='FollowTable')
        query.add_filter('following', '=', userIdToCheckFollowersOf)
        query.order = ['-following']
        results = list(query.fetch())
        userInfo = []
        for result in results:
            userInfo.append({
                "id": result.key.id_or_name,
                "followed_by": result['followed_by'],
                "following": result['following']
            })

        return results

    def allFollowing(userIdToCheckFollowingOf):
        query = client.query(kind='FollowTable')
        query.add_filter('followed_by', '=', userIdToCheckFollowingOf)
        query.order = ['-followed_by']
        results = list(query.fetch())
        userInfo = []
        for result in results:
            userInfo.append({
                "id": result.key.id_or_name,
                "followed_by": result['followed_by'],
                "following": result['following']
            })

        return results

    def addCommentToPost(createdTime, userId, postId, comment, name, email):
        entity = datastore.Entity(key=client.key('UserComments'))
        entity.update(
            {
                'userId': userId,
                'name': name,
                'email': email,
                'comment': comment,
                'postId': postId,
                'createdTime': createdTime
            }
        )
        client.put(entity)
        return entity.key.id
