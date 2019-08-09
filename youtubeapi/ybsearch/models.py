from django.db import models
from django.contrib.auth.models import User


class SearchVideo(models.Model):
    request_string = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now=True)


class Video(models.Model):
    title = models.CharField(max_length=255)
    image_url = models.CharField(max_length=255, null=True)
    liked_by = models.ManyToManyField(User)
    created_at = models.DateTimeField(auto_now=True)
    search = models.ForeignKey(SearchVideo, on_delete=models.CASCADE)

    def __repr__(self):
        return self.title
