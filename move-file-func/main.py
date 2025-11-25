from google.cloud import storage

def move_file(event, context):
    client = storage.Client()

    src_bucket = client.bucket("public-upload-bucket")
    dest_bucket = client.bucket("secured-storage-bucket")

    blob = src_bucket.blob(event['name'])
    new_blob = dest_bucket.blob(event['name'])

    new_blob.rewrite(blob)
    blob.delete()
