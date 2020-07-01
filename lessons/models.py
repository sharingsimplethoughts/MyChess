from django.db import models
from accounts.models import *

# Create your models here..

class LessonCategory(models.Model):
    name = models.CharField(max_length=300,default='')
    icon = models.ImageField(upload_to='lessons/category',blank=True,null=True)
    iconurl = models.URLField(default='',blank=True,null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    is_blocked = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Lesson(models.Model):
    name = models.CharField(max_length=500,default='')
    # lesson_image = models.ImageField(upload_to='lessons/images', blank=True,null=True, default=None)
    # lesson_image_url = models.URLField(default='',blank=True,null=True)
    category = models.ForeignKey(LessonCategory,on_delete=models.CASCADE,related_name='l_cat')
    video = models.FileField(upload_to='lessons/videos',blank=True,null=True)
    videourl = models.URLField(default='',blank=True,null=True)
    videopreview = models.ImageField(upload_to='lessons/videoprevs',blank=True,null=True)
    videopreviewurl = models.URLField(default='',blank=True,null=True)
    description = models.CharField(max_length=1000,default='')
    hint = models.CharField(max_length=1000,default='')
    explanation = models.CharField(max_length=1000,default='')
    learned = models.CharField(max_length=1000,default='')
    created_on = models.DateTimeField(auto_now_add=True)
    is_blocked = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name + '---' + self.category.name

class LessonManagement(models.Model):
    lesson = models.ForeignKey(Lesson,on_delete=models.CASCADE,related_name='lm_lesson')
    player = models.ForeignKey(User,on_delete=models.CASCADE,related_name='lm_user')
    created_on=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.id)


class Tactic(models.Model):
    help_text = models.CharField(max_length=2000,default='')

    def __str__(self):
        return self.help_text