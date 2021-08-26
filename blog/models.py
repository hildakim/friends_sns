from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.contrib.auth.models import User

# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, related_name='author', on_delete=models.CASCADE)
    body = models.TextField()
    upload_date = models.DateTimeField()
    image = models.ImageField(upload_to='blog/', null=True, blank=True)
    image_thumbnail = ImageSpecField(source='image', processors=[ResizeToFill(150, 150)])
    #좋아요
    like = models.ManyToManyField(User, related_name='like', blank=True)

    def __str__(self):
        return self.title 

    def summary(self):
        return self.body[:100]+'...'

class Comment(models.Model):
    post_id = models.ForeignKey("Blog", on_delete=models.CASCADE, db_column="post_id", default="0")
    comment_id = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True)
    writer = models.ForeignKey(User, related_name='writer', on_delete=models.CASCADE)
    body = models.TextField()

class Follow(models.Model):
    target = models.ForeignKey(User, related_name='target', on_delete=models.CASCADE)
    follower = models.ForeignKey(User, related_name='follower', on_delete=models.CASCADE)
    