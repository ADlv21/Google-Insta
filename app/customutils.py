from google.cloud import storage
from google.cloud import datastore
import base64
from PIL import Image
from io import BytesIO

BUCKET_NAME = 'insta-cloud-384319.appspot.com'
datastore_client = datastore.Client()


class Utils:
    def __init__(self, user_id):
        self.user_id = user_id

    def addUserPostImage(file, imagePath: str):
        # Connect to Google Cloud Storage
        client = storage.Client.from_service_account_json(
            'insta-cloud-384319-beb0cab41c26.json')
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

    def getAllUserPostImages(username):
        storage_client = storage.Client().from_service_account_json(
            'insta-cloud-384319-beb0cab41c26.json')

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
