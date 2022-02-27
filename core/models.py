from pyexpat import model
from django.db import models

# Create your models here.

class Song_data(models.Model):
    title = models.CharField(max_length=200)
    download_complete = models.BooleanField(default=False)
    record=models.BinaryField(blank=True,null=True)