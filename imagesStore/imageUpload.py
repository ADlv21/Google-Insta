from google.cloud import storage
import pandas as pd
import io
from io import BytesIO

storage_client = storage.Client.from_service_account_json(
    'insta-cloud-384319-beb0cab41c26.json')

BUCKET_NAME = 'insta-cloud-384319.appspot.com'
bucket = storage_client.get_bucket(BUCKET_NAME)

filename = "%s/%s" % ('usrBATMAN', 'BAT-1')
blob = bucket.blob(filename)

with open('app/static/assets/batman.png', 'rb') as f:
    blob.upload_from_file(f)
