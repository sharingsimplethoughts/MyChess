from django.db import models
from accounts.models import *

# Create your models here..

class Achievement(models.Model):
    name=models.CharField(max_length=500,blank=True,null=True)
    image=models.ImageField(upload_to='achievement/')
    image_url=models.URLField(default='',blank=True,null=True)
    unlock_task=models.CharField(max_length=1000,blank=True,null=True)
    is_blocked=models.BooleanField(default=False)
    is_deleted=models.BooleanField(default=False)

    def __str__(self):
        return self.name

class AchievementManager(models.Model):
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE, related_name='am_ach')
    player = models.ForeignKey(User,on_delete=models.CASCADE, related_name='am_user')
    created_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.achivement.name+'---'+self.user.first_name



