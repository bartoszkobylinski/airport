from django.db import models


class Airplane(models.Model):
    airplane_id = models.CharField(max_length=8)
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()
    velocity = models.FloatField()
    fuel = models.FloatField()
    timestamp = models.DateTimeField()

    @classmethod
    def delete_all(cls):
        cls.objects.all().delete()

    class Status(models.IntegerChoices):
        WAITING = 1
        APPROACHING = 2
        DESCENDING = 3
        LANDED = 4
        CRASHED = 5

    status = models.IntegerField(choices=Status.choices, default=Status.WAITING)

    def __str__(self):
        return f"{self.airplane_id} at x: {str(self.x)}, y: {str(self.y)}, z: {str(self.z)}"
