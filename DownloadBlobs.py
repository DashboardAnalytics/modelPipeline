from google.cloud import storage

bucketName = "streamed-videos"

# Get elements name
def download(bucketName):
    storageClient = storage.Client()
    bucket = storageClient.get_bucket(bucketName)
    blobs = storageClient.list_blobs(bucketName)
    for blob in blobs:
        print("Downloading blob:", blob.name)
        blob.download_to_filename(fileDestinationName)

    return True



if(download(bucketName)):
    print("Downloads complete!")
