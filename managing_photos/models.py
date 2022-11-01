from email.policy import default
from turtle import width
from django.db import models

# Create your models here.

class Photo(models.Model):

    albumId = models.IntegerField(null=True, blank=True)
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length = 300, null=True, blank=True)
    url = models.URLField(null=True, blank=True)

    thumbnailUrl = models.URLField(null=True, blank=True)
    image = models.ImageField(upload_to='images')

    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    hexcolorDominant = models.CharField(max_length=7, null=True, blank=True)
