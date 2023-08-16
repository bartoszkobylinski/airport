from django.db import models
import boto3
import os

aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
region_name = 'eu-north-1'
aws_storage_bucket_name = "airport-app"

s3 = boto3.resource("s3",
                    aws_access_key_id=aws_access_key_id,
                    aws_secret_access_key=aws_secret_access_key,
                    region_name=region_name)

bucket = s3.Bucket(aws_storage_bucket_name)


def get_plane_images():
    import boto3
    from botocore.exceptions import NoCredentialsError

    s3 = boto3.resource('s3')

    amazon_bucket = s3.Bucket('airport-app')

    try:
        AIRPLANE_IMAGES = ["https://airport-app.s3.amazonaws.com/" + file.key for file in amazon_bucket.objects.all()]
        print(f"Retrieved images: {AIRPLANE_IMAGES}")  # Debug print statement
    except NoCredentialsError:
        print("No AWS credentials were found.")
        AIRPLANE_IMAGES = []

    return AIRPLANE_IMAGES


AIRPLANE_IMAGES = get_plane_images()


class Airplane(models.Model):
    airplane_id = models.CharField(max_length=8)
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()
    velocity = models.FloatField()
    fuel = models.FloatField()
    image_url = models.CharField(max_length=255, blank=True)
    timestamp = models.DateTimeField()

    @classmethod
    def delete_all(cls):
        cls.objects.all().delete()

    @staticmethod
    def lerp(a, b, t):
        """Linear interpolation from a to b using t."""
        return a + (b - a) * t

    '''
    @staticmethod
    def project_to_screen(x, y, z, screen_width=1200, screen_height=1800, camera_z=-1000):
        """Projects the 3D coordinates to 2D screen coordinates."""
        d = z + abs(camera_z)  # distance from the camera to the object
        x_2d = (camera_z * x / d) + screen_width / 2
        y_2d = (camera_z * y / d) + screen_height / 2

        # Adjust size of image based on distance from the camera assuming that the maximum distance the object can be
        # from the camera is abs(camera_z) * 2
        t = 1 - min(d, abs(camera_z) * 2) / (abs(camera_z) * 2)
        image_size = Airplane.lerp(50, 150, t)

        # Adjust coordinates so that the image will be centered
        image_x, image_y = x_2d - image_size / 2, y_2d - image_size / 2

        return image_x, image_y, image_size
    '''

    @staticmethod
    def project_to_screen(x, y, z, screen_width=1200, screen_height=900, camera_z=-1000):
        """Projects the 3D coordinates to 2D screen coordinates."""

        # Translate so the 3D and 2D spaces are aligned
        # x += 5000
        # y += 5000

        # Scale down the 3D coordinates to fit the screen
        x = (x / 10000) * screen_width
        y = (y / 10000) * screen_height

        d = z + abs(camera_z)  # distance from the camera to the object
        x_2d = (camera_z * x / d) + screen_width / 2
        y_2d = (camera_z * y / d) + screen_height / 2

        # Adjust size of image based on distance from the camera assuming that the maximum distance the object can be
        # from the camera is abs(camera_z) * 2
        t = 1 - min(d, abs(camera_z) * 2) / (abs(camera_z) * 2)
        image_size = Airplane.lerp(50, 150, t)

        # Adjust coordinates so that the image will be centered
        image_x, image_y = x_2d - image_size / 2, y_2d - image_size / 2

        return image_x, image_y, image_size

    class Status(models.IntegerChoices):
        WAITING = 1
        APPROACHING = 2
        DESCENDING = 3
        LANDED = 4
        CRASHED = 5

    status = models.IntegerField(choices=Status.choices, default=Status.WAITING)

    def __str__(self):
        return f"{self.airplane_id} at x: {str(self.x)}, y: {str(self.y)}, z: {str(self.z)}"
