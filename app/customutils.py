from google.cloud import storage
from google.cloud import datastore
import base64
from PIL import Image
from io import BytesIO
from app.local_constants import PROJECT_STORAGE_BUCKET, SERVICE_ACCOUNT_JSON

BUCKET_NAME = PROJECT_STORAGE_BUCKET

datastore_client = datastore.Client()


class Utils:
    def __init__(self, user_id):
        self.user_id = user_id

    def addUserPostImage(file, imagePath: str):
        # Connect to Google Cloud Storage
        client = storage.Client.from_service_account_json(SERVICE_ACCOUNT_JSON)
        bucket = client.bucket(BUCKET_NAME)

        # Create new blob and upload file to blob
        blob = bucket.blob(imagePath)
        blob.upload_from_string(file.read(), content_type=file.content_type)

    def createUserPost(createdTime, userId, caption, imagePath):
        entity = datastore.Entity(key=datastore_client.key('Posts'))
        entity.update(
            {
                'userId': userId,
                'caption': caption,
                'imagePath': imagePath,
                'createdTime': createdTime
            }
        )
        datastore_client.put(entity)
        return entity.key.id

    def fetchPostComments():
        query = datastore_client.query(kind='Comment')
        results = list(query.fetch())
        commentInfo = []
        for result in results:
            commentInfo.append({
                'userId': result['userId'],
                'name': result['name'],
                'email': result['email'],
                'comment': result['comment'],
                'postId': result['postId'],
                'createdTime': result['createdTime']
            })
        return commentInfo

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
        query = datastore_client.query(kind='Users')
        results = list(query.fetch())
        userInfo = []
        for result in results:
            userInfo.append({
                "id": result.key.id_or_name,
                "email": result['email'],
                "userId": result['user_id'],
                "name": result['name']
            })
        return userInfo

    def userInfoByID(userId):
        query = datastore_client.query(kind='Users')
        query.add_filter('user_id', '=', userId)
        results = list(query.fetch())
        userInfo = []
        for result in results:
            userInfo.append({
                "id": result.key.id_or_name,
                "email": result['email'],
                "userId": result['user_id'],
                "name": result['name']
            })
        return userInfo

    """
    FOLLOW USER BY ID
    """
    def followUserByUserId(userId, userIdToFollow):
        entity = datastore.Entity(key=datastore_client.key('Follow'))
        entity.update(
            {
                'following': userIdToFollow,
                'followed_by': userId,
            }
        )
        datastore_client.put(entity)
        return {
            'following': userIdToFollow,
            'followed_by': userId,
        }

    """
    UNFOLLOW USER BY ID
    """
    def unFollowUserByUserId(userId, userIdToUnFollow):

        query = datastore_client.query(kind='Follow')
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

        entity = datastore_client.key('Follow', followingInfo[0]['id'])
        datastore_client.delete(entity)
        return {'Data': followingInfo[0]['id']}

    def isUserFollowingTheUserId(userId, userIdToCheckForFollowing):
        query = datastore_client.query(kind='Follow')
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
        query = datastore_client.query(kind='Follow')
        query.add_filter('following', '=', userIdToCheckFollowersOf)
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
        query = datastore_client.query(kind='Follow')
        query.add_filter('followed_by', '=', userIdToCheckFollowingOf)
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
        entity = datastore.Entity(key=datastore_client.key('Comment'))
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
        datastore_client.put(entity)
        return entity.key.id
