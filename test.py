from google.cloud import storage
from google.cloud import datastore
import base64
from datetime import datetime
from PIL import Image
from io import BytesIO
from app.local_constants import PROJECT_STORAGE_BUCKET, SERVICE_ACCOUNT_JSON

BUCKET_NAME = PROJECT_STORAGE_BUCKET

datastore_client = datastore.Client()
storage_client = storage.Client().from_service_account_json(SERVICE_ACCOUNT_JSON)
bucket = storage_client.get_bucket(BUCKET_NAME)
files = list(bucket.list_blobs(prefix=''))
image_bytes = []
fileNames = []
for f in files:
    fileNames.append(f.name)
    blob_content = f.download_as_bytes()
    image_bytes.append(Image.open(BytesIO(blob_content)).convert('RGB'))

# Convert the list of PIL images to base64-encoded strings
encoded_images = []
for image in image_bytes:
    buffered = BytesIO()
    image.save(buffered, format='JPEG')
    encoded_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
    encoded_images.append(encoded_image)

result_dict = {fileNames[i]: encoded_images[i] for i in range(len(fileNames))}
