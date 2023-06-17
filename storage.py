from google.cloud import storage
import google.auth
import datetime
import random
import string

def upload_blob(userID, filename, file):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    # The path to your file to upload
    # The ID of your GCS object
    destination_blob_name = f"{userID}/{filename}"

    storage_client = storage.Client()
    bucket = storage_client.bucket("purchaseorders-urp")
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_file(file)  # upload file object directly to GCS
    credentials, project = google.auth.default()
    credentials.refresh(google.auth.transport.requests.Request())

    expiration_timedelta = datetime.timedelta(days=10)

    storage_client = storage.Client(credentials=credentials)
    bucket = storage_client.get_bucket("purchaseorders-urp")
    blob = bucket.get_blob(destination_blob_name)
    url = f"https://storage.googleapis.com/purchaseorders-urp/{userID}/{filename}"
    return url



def generate_session_id(length):
    return ''.join(random.choice('0123456789') for _ in range(length))
