from django.db import models
import datetime
from accounts.models import *
from game.models import *

game_status=(('1','waiting'),('2','started'),('3','declined'),('4','timedout'),('5','finished'))

class Tournament(models.Model):
    name=models.CharField(max_length=500, blank=True, null=True)
    game_time_limit=models.PositiveIntegerField(default=10)
    start_date=models.DateField()
    end_date=models.DateField()
    duration=models.PositiveIntegerField(default=10)
    is_only_sub_members=models.BooleanField(default=False)
    is_entry_before_tournament=models.BooleanField(default=False)
    is_entry_after_half_time=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    start_time=models.TimeField(default=datetime.time(9, 00))
    rounds=models.PositiveIntegerField(default=1)
    rating=models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.name

class TournamentPlayerManager(models.Model):
    tournament=models.ForeignKey(Tournament,on_delete=models.CASCADE,related_name='tpm_tp', null=True)
    player=models.ForeignKey(User,on_delete=models.CASCADE,related_name='tpm_player')
    points=models.PositiveIntegerField(default=0,)
    total_games_played = models.PositiveIntegerField(default=0)
    total_games_won = models.PositiveIntegerField(default=0)
    total_games_lost = models.PositiveIntegerField(default=0)
    total_games_drawn = models.PositiveIntegerField(default=0)
    rating = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.tournament.name+'--'+self.player.name+'--'+str(self.points)

class TournamentGameManager(models.Model):
    # game_type=models.ForeignKey(GameType,on_delete=models.CASCADE,related_name='tg_game_type',null=True)
    # player1=models.ForeignKey(User,on_delete=models.CASCADE,related_name='tg_player1')
    # player2=models.ForeignKey(User,on_delete=models.CASCADE,related_name='tg_player2')
    # winner=models.ForeignKey(User,on_delete=models.CASCADE,related_name='tg_winner',null=True,)
    # duration=models.PositiveIntegerField(default=30)
    # room_id=models.CharField(max_length=1000,blank=True,null=True,default='')
    # created_on=models.DateTimeField(auto_now=True)
    # status=models.CharField(max_length=20,choices=game_status,default='1')
    game = models.ForeignKey(Game,on_delete=models.CASCADE,related_name='tg_game',default=None)
    tournament=models.ForeignKey(Tournament,on_delete=models.CASCADE,related_name='tg_tournament')
    winning_streak=models.CharField(max_length=100,blank=True,null=True)

    def __str__(self):
        return str(self.id)




