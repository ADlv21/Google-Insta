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

    def getAllUserPostImages(self, user_id):

        self.user_id = user_id

        storage_client = storage.Client().from_service_account_json(
            'insta-cloud-384319-beb0cab41c26.json')

        bucket = storage_client.get_bucket(BUCKET_NAME)
        filename = list(bucket.list_blobs(prefix=user_id))

        image_bytes = []

        for f in filename:
            blob_content = f.download_as_bytes()
            image_bytes.append(Image.open(
                BytesIO(blob_content)).convert('RGB'))
            print(image_bytes)
            print(type(image_bytes))

        # Convert the list of PIL images to base64-encoded strings
        encoded_images = []
        for image in image_bytes:
            buffered = BytesIO()
            image.save(buffered, format='JPEG')
            encoded_image = base64.b64encode(
                buffered.getvalue()).decode('utf-8')
            encoded_images.append(encoded_image)

        return encoded_images
        # return render_template('renderImage.html', encoded_images=encoded_images)

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
