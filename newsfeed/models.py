from django.db import models

from accounts.models import User
from django.utils.timezone import now
from django.conf import settings

from PIL import Image
from django.urls import reverse


class Post(models.Model):
 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    body = models.TextField(null=False)
    created_at = models.DateTimeField(default=now)
    post_image = models.ImageField(upload_to="pics",default='avatars/default.jpg',null=True)
    def __str__(self):
        return self.body
    

    def get_absolute_url(self):
        return reverse('core:home')
    def save(self):
        super().save()
        img = Image.open(self.post_image.path)
        if img.height>600 or img.width>600:
            outputsize=(600,600)
            img.thumbnail(outputsize)
            img.save(self.post_image.path)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=now)

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes",null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=now)
    def __str__(self):
            return "%s" % self.user


class Dislike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="dislikes",null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=now)


def save(self):
    super().save()
    img = Image.open(self.image.path)
    if img.height>300 or img.width>300:
        outputsize=(300,300)
        img.thumbnail(outputsize)
        img.save(self.image.path)