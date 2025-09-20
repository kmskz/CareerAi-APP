from google.cloud import storage
client=storage.Client()

def upload_to_gcs(bucket_name, file, destination_blob_name):
    """Upload file-like object (from Streamlit uploader) to Google Cloud Storage"""
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Directly from file-like object (Streamlit UploadedFile)
    blob.upload_from_file(file, rewind=True)

    # Optional fallback:
    # blob.upload_from_string(file.getvalue())

    return f"gs://{bucket_name}/{destination_blob_name}"
