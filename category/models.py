from django.db import models
from accounts.models import *
# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=50,blank=True,null=True)

    def __str__(self):
        return self.category_name

class Video(models.Model):
    video_file = models.FileField(upload_to='category/videos')
    title = models.CharField(max_length=300,blank=True,null=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='vid_cat')
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='vid_user')
    detail = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    text = models.CharField(max_length=1000,blank=True,null=True)
    video = models.ForeignKey(Video,on_delete=models.CASCADE,related_name='comm_vid')
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='comm_user')
    created_on = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.text
