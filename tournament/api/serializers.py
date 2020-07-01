from rest_framework import serializers
from rest_framework.exceptions import APIException
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import User
import datetime
from django.contrib.sites.shortcuts import get_current_site

from accounts.models import *
from tournament.models import *

class AvailableTournamentListSerializer(serializers.ModelSerializer):
    # id = serializers.SerializerMethodField()
    # name = serializers.SerializerMethodField()
    end_in = serializers.SerializerMethodField()
    arena = serializers.SerializerMethodField()
    number_of_players = serializers.SerializerMethodField()
    class Meta:
        model = Tournament
        fields = ('id','name','start_date','start_time','end_in','arena','number_of_players','rounds','rating','game_time_limit')
    # def get_id(self,instance):
    #     return instance.tournament.id
    # def get_name(self,instance):
    #     return instance.tournament.name
    def get_end_in(self,instance):
        #NEED COMMENT AS PER REQUIREMENT OF ABHISHEK--------------------
        d = datetime.datetime.combine(instance.end_date, datetime.datetime.min.time())
        diff = d - datetime.datetime.now()
        days, seconds = diff.days, diff.seconds
        hours = days * 24 + seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return 'Starts in '+str(hours)+'hr '+str(minutes)+'min '+str(seconds)+'sec'
        #-----------------FALTU CODE AS PER REQUIREMENT OF ABHISHEK----------------
        # return 'End in 10 min'
    def get_arena(self,instance):
        return 'Arena'
    def get_number_of_players(self,instance):
        number_of_players = TournamentPlayerManager.objects.filter(tournament=instance).count()
        return number_of_players

class JoinedTournamentListSerializer(serializers.ModelSerializer):
    # id = serializers.SerializerMethodField()
    # name = serializers.SerializerMethodField()
    end_in = serializers.SerializerMethodField()
    arena = serializers.SerializerMethodField()
    number_of_players = serializers.SerializerMethodField()
    class Meta:
        model = Tournament
        fields = ('id','name','start_date','start_time','end_in','arena','number_of_players','rounds','rating','game_time_limit')
    # def get_id(self,instance):
    #     return instance.tournament.id
    # def get_name(self,instance):
    #     return instance.tournament.name
    def get_end_in(self,instance):
        #NEED COMMENT AS PER REQUIREMENT OF ABHISHEK-------------------
        d = datetime.datetime.combine(instance.end_date, datetime.datetime.min.time())
        diff = d - datetime.datetime.now()
        days, seconds = diff.days, diff.seconds
        hours = days * 24 + seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return 'Ends in '+str(hours)+'hr '+str(minutes)+'min '+str(seconds)+'sec'
        #-----------------FALTU CODE AS PER REQUIREMENT OF ABHISHEK----------------
        # return 'End in 10 min'
    def get_arena(self,instance):
        return 'Arena'
    def get_number_of_players(self,instance):
        number_of_players = TournamentPlayerManager.objects.filter(tournament=instance).count()
        return number_of_players

class GetTournamentPlayerDetailSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()
    country_flag = serializers.SerializerMethodField()
    game_points = serializers.SerializerMethodField()
    class Meta:
        model = TournamentPlayerManager
        fields = ('profile_image','user_name','country_flag','game_points')
        # fields = ('profile_image','user_name','country_flag','game_points')
    def get_profile_image(self,instance):
        if instance.player.profile_image:
            curr_site = get_current_site(self.context['request'])
            return 'http://'+str(curr_site)+instance.player.profile_image.url
        return ''
    def get_user_name(self,instance):
        return instance.player.name
    def get_country_flag(self,instance):
        cc = CountryCode.objects.filter(code=instance.player.country_code).last()
        if cc:
            return 'https://www.countryflags.io/'+cc.count_code+'/flat/64.png'
        return ''
    def get_game_points(self,instance):
        return instance.points

class TournamentStandingsSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    game_time_limit = serializers.SerializerMethodField()
    number_of_players = serializers.SerializerMethodField()
    player_detail = serializers.SerializerMethodField()
    class Meta:
        model = Tournament
        fields = ('name','start_date','start_time','game_time_limit','number_of_players','rounds','rating','player_detail')
    def get_name(self,instance):
        return instance.name
    def get_game_time_limit(self,instance):
        return instance.game_time_limit
    def get_number_of_players(self,instance):
        return TournamentPlayerManager.objects.filter(tournament=instance).count()
    def get_player_detail(self,instance):
        queryset=TournamentPlayerManager.objects.filter(tournament=instance).order_by('-points')
        if queryset:
            serializer = GetTournamentPlayerDetailSerializer(queryset,many=True,context={'request':self.context['request']})
            return serializer.data
        return 'No data available'

class UserTournamentStatusSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    number_of_players = serializers.SerializerMethodField()
    game_time_limit = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()
    profile_image = serializers.SerializerMethodField()
    country_flag = serializers.SerializerMethodField()
    game_points = serializers.SerializerMethodField()
    # total_games_played
    # total_games_won
    # total_games_lost
    number_of_winning_streak = serializers.SerializerMethodField()
    class Meta:
        model = TournamentPlayerManager
        fields = ('name','number_of_players','game_time_limit',
        'user_name','profile_image','country_flag','game_points','total_games_played',
        'total_games_won','total_games_lost','number_of_winning_streak')
    def get_name(self,instance):
        print(instance)
        return instance.tournament.name
    def get_number_of_players(self,instance):
        return TournamentPlayerManager.objects.filter(tournament__id=instance.tournament.id).count()
    def get_game_time_limit(self,instance):
        return instance.tournament.game_time_limit
    def get_user_name(self,instance):
        return instance.player.name
    def get_profile_image(self,instance):
        if instance.player.profile_image:
            curr_site = get_current_site(self.context['request'])
            return 'http://'+str(curr_site)+instance.player.profile_image.url
        return ''
    def get_country_flag(self,instance):
        cc = CountryCode.objects.filter(code=instance.player.country_code).last()
        if cc:
            return 'https://www.countryflags.io/'+cc.count_code+'/flat/64.png'
        return ''
    def get_game_points(self,instance):
        return instance.points
    def get_number_of_winning_streak(self,instance):
        games = Game.objects.filter(winner=instance.player)
        number_of_winning_streak=TournamentGameManager.objects.filter(game__in=games,tournament=instance.tournament).count()
        # number_of_winning_streak = TournamentGameManager.objects.filter(winner=instance.player,tournament=instance.tournament).count()
        return number_of_winning_streak
