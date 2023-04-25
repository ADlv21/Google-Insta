from google.cloud import storage
from flask import Flask, render_template, request
import base64
from io import BytesIO
from PIL import Image

BUCKET_NAME = 'insta-cloud-99d25.appspot.com'

# Create a Flask application instance
app = Flask(__name__)


@app.route('/img')
def getAllUserPostImages():
    USERNAME = request.cookies.get('user_id')
    storage_client = storage.Client().from_service_account_json(
        'insta-cloud-99d25-df80f88aaf72.json')

    bucket = storage_client.get_bucket(BUCKET_NAME)
    filename = list(bucket.list_blobs(prefix=''))

    image_bytes = []

    for f in filename:
        blob_content = f.download_as_bytes()
        image_bytes.append(Image.open(BytesIO(blob_content)).convert('RGB'))
        print(image_bytes)
        print(type(image_bytes))

    # Convert the list of PIL images to base64-encoded strings
    encoded_images = []
    for image in image_bytes:
        buffered = BytesIO()
        image.save(buffered, format='JPEG')
        encoded_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
        encoded_images.append(encoded_image)

    print(encoded_images)
    return render_template('renderImage.html', encoded_images=encoded_images)


if __name__ == '__main__':
    app.run(debug=True, port=3000)
