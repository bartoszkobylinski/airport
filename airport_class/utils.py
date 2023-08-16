def get_plane_images():
    import boto3
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('airport-app')
    AIRPLANE_IMAGES = ["https://airport-app.s3.amazonaws.com/" + file.key for file in bucket.objects.all()]

    return AIRPLANE_IMAGES
