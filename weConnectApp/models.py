from datetime import datetime
import uuid
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, primary_key = True,on_delete=models.CASCADE)
    name = models.CharField(max_length =30, blank = True, null = True)
    about = models.TextField(max_length = 200, blank=True)
    profilePic = models.ImageField(upload_to='profilePic', default=None)
    DOB = models.DateField()

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)


class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)


class FollowersCount(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)