from django.db import models


class DataPoint(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    difficulty = models.IntegerField()
    value = models.IntegerField()