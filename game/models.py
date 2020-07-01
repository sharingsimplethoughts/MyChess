from django.db import models
from accounts.models import *

friend_status=(('1','waiting'),('2','accepted'),('3','declined'))
game_status=(('1','waiting'),('2','started'),('3','declined'),('4','timedout'),('5','finished'))
# Create your models here.
class GameType(models.Model):
    name=models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.name

class Friends(models.Model):
    player=models.ForeignKey(User,on_delete=models.CASCADE,related_name='f_user')
    friend=models.ForeignKey(User,on_delete=models.CASCADE,related_name='f_friend')
    status=models.CharField(max_length=50,choices=friend_status,default='1')
    created_on=models.DateTimeField(auto_now=True)
    # request_status=models.CharField(max_length=50,choices=friend_status,default='1')

    def __str__(self):
        return 'user-'+str(self.player.id)+'-friend-'+str(self.friend.id)

class GameDuration(models.Model):
    duration=models.PositiveIntegerField(default=10)
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return str(self.duration)

class Game(models.Model):
    game_type=models.ForeignKey(GameType,on_delete=models.CASCADE,related_name='g_game_type',null=True)
    player1=models.ForeignKey(User,on_delete=models.CASCADE,related_name='g_player1')
    player2=models.ForeignKey(User,on_delete=models.CASCADE,related_name='g_player2')
    winner=models.ForeignKey(User,on_delete=models.CASCADE,related_name='g_winner',null=True,)
    duration=models.ForeignKey(GameDuration, on_delete=models.CASCADE, related_name='g_duration')
    room_id=models.CharField(max_length=1000,blank=True,null=True,default='')
    created_on=models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=20,choices=game_status,default='1')
    player1_point = models.PositiveIntegerField(default=0)
    player2_point = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.id)

class SampleImageStore(models.Model):
    sample_image=models.ImageField(upload_to='user/profile_image',blank=True,null=True)
    sample_data=models.CharField(max_length=1000,default='')
    unique_identification=models.CharField(max_length=50, default='')
    def __str__(self):
        return str(self.id)

