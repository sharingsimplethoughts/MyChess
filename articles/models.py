from django.db import models
from accounts.models import *
# Create your models here.
class Article(models.Model):
    article_file=models.FileField(upload_to='articles',max_length=9000)
    article_file_url=models.URLField(max_length=9000, default='',blank=True,null=True,) 
    preview_image=models.ImageField(upload_to='articles/preview', default='', max_length=9000,blank=True,null=True,)   
    preview_image_url=models.URLField(max_length=1000,default='',blank=True,null=True,)    
    title = models.CharField(max_length=100,null=True,blank=True)
    description = models.CharField(max_length=500,null=True,blank=True)
    created_on = models.CharField(max_length=100,default='',blank=True,null=True)
    actually_created_on = models.DateTimeField(auto_now=True)
    author = models.CharField(max_length=100,null=True,blank=True)
    author_country = models.CharField(max_length=100,default='', blank=True, null=True)
    author_profile_photo = models.ImageField(upload_to='articles/auth_profile', default='', max_length=9000,blank=True,null=True,)
    author_profile_photo_url=models.URLField(max_length=9000,default='',blank=True,null=True,)
    number_of_views = models.PositiveIntegerField(default=0,blank=True, null=True)
    is_video = models.BooleanField(default=False)
    def __str__(self):
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='commt_user')
    created_on=models.DateField(auto_now=True)
    comment = models.CharField(max_length=500, blank=True, null=True)
    article = models.ForeignKey(Article,on_delete=models.CASCADE, related_name="commt_article")

    def __str__(self):
        return self.comment

class VideoCategory(models.Model):
    name=models.CharField(max_length=100,blank=True,null=True)
    icon=models.ImageField(upload_to='videos/category',blank=True,null=True)
    icon_url=models.URLField(max_length=1000,blank=True,null=True)
    description=models.CharField(max_length=1000,default='')
    created_on=models.DateTimeField(auto_now_add=True)
    is_blocked=models.BooleanField(default=False)    

    def __str__(self):
        return self.name

class Video(models.Model):
    name=models.CharField(max_length=500,blank=True,null=True)
    category=models.ForeignKey(VideoCategory,on_delete=models.CASCADE,related_name="v_cat")
    vfile=models.FileField(upload_to='videos',blank=True,null=True)
    vfileurl=models.URLField(max_length=1000,blank=True,null=True)
    vpreview=models.ImageField(upload_to='videos/preview',blank=True,null=True)
    vpreviewurl=models.URLField(max_length=1000,blank=True,null=True)
    description=models.CharField(max_length=1000,blank=True,null=True)
    authorname=models.CharField(max_length=100,blank=True,null=True)
    authorpic=models.ImageField(upload_to='videos/author',blank=True,null=True)
    authorpicurl=models.URLField(max_length=1000,default='',blank=True,null=True)    
    authorcountry=models.CharField(max_length=100,blank=True,null=True)
    created_on=models.DateTimeField(auto_now_add=True)
    is_blocked=models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

class VideoWatchHistory(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='v_w_user')
    video=models.ForeignKey(Video,on_delete=models.CASCADE,related_name='v_w_video')
    created_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name

class VideoComment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='vcommt_user')
    created_on=models.DateField(auto_now=True)
    comment = models.CharField(max_length=500, blank=True, null=True)
    video = models.ForeignKey(Video,on_delete=models.CASCADE, related_name="vcommt_video")

    def __str__(self):
        return self.comment
