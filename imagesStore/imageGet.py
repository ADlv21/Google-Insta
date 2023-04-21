from google.cloud import storage
import pandas as pd
import io
from io import BytesIO

storage_client = storage.Client.from_service_account_json(
    'insta-cloud-384319-beb0cab41c26.json')

BUCKET_NAME = 'insta-cloud-384319.appspot.com'
bucket = storage_client.get_bucket(BUCKET_NAME)

filename = list(bucket.list_blobs(prefix=''))

for name in filename:
    print(name.name)
