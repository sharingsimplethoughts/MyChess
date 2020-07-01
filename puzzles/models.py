from django.db import models
from accounts.models import User
# Create your models here.

class PuzzleCategory(models.Model):
    name = models.CharField(max_length=300,default='')
    icon = models.ImageField(upload_to='puzzles/category',blank=True,null=True)
    iconurl = models.URLField(default='',blank=True,null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    is_blocked = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Puzzle(models.Model):
    name = models.CharField(max_length=500,default='')
    category = models.ForeignKey(PuzzleCategory,on_delete=models.CASCADE,related_name='l_cat')
    video = models.FileField(upload_to='puzzles/videos',blank=True,null=True)
    videourl = models.URLField(default='',blank=True,null=True)
    videopreview = models.ImageField(upload_to='puzzles/videoprevs',blank=True,null=True)
    videopreviewurl = models.URLField(default='',blank=True,null=True)
    description = models.CharField(max_length=1000,default='')
    hint = models.CharField(max_length=1000,default='')
    explanation = models.CharField(max_length=1000,default='')
    learned = models.CharField(max_length=1000,default='')
    created_on = models.DateTimeField(auto_now_add=True)
    is_blocked = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name + '---' + self.category.name

class PuzzleManagement(models.Model):
    puzzle=models.ForeignKey(Puzzle,on_delete=models.CASCADE,related_name='pm_puzzle')
    player=models.ForeignKey(User,on_delete=models.CASCADE,related_name='pm_player')
    created_on=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.id)
