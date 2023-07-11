from django.db import models


class Airplane(models.Model):
    airplane_id = models.CharField(max_length=8)
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()
    velocity = models.FloatField()
    fuel = models.FloatField()
    image = models.ImageField(upload_to="airport_app_images/")
    timestamp = models.DateTimeField()

    @classmethod
    def delete_all(cls):
        cls.objects.all().delete()

    @staticmethod
    def lerp(a, b, t):
        """Linear interpolation from a to b using t."""
        return a + (b - a) * t

    def project_to_screen(self, screen_width=1200, screen_height=1800, camera_z=-1000):
        """Projects the airplane's 3D coordinates to 2D screen coordinates."""
        d = self.z + abs(camera_z)  # distance from the camera to the airplane
        x_2d = (camera_z * self.x / d) + screen_width / 2
        y_2d = (camera_z * self.y / d) + screen_height / 2

        # Adjust size of image based on distance from the camera assuming that the maximum distance the airplane can be
        # from the camera is abs(camera_z) * 2
        t = 1 - min(d, abs(camera_z) * 2) / (abs(camera_z) * 2)
        image_size = self.lerp(50, 150, t)

        # Adjust coordinates so that the airplane image will be centered
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
