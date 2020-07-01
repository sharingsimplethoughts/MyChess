from rest_framework import serializers
from rest_framework.exceptions import APIException
from accounts.models import *
from achievement.models import *
from django.contrib.sites.shortcuts import get_current_site
import cv2
import datetime
from datetime import date

class AchievementListSerializer(serializers.ModelSerializer):
    achieved = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()
    achievements = serializers.SerializerMethodField()
    class Meta:
        model = Achievement
        fields = ('achieved','total','achievements')
    def get_achieved(self,instance):
        request = self.context['request']
        user=request.user
        achieved = AchievementManager.objects.filter(player=user).count()
        return achieved
    def get_total(self,instance):
        total = Achievement.objects.filter(is_deleted=False,is_blocked=False).count()
        return total
    def get_achievements(self,instance):
        queryset = Achievement.objects.filter(is_deleted=False,is_blocked=False)
        serializer = AchievementDetailSerializer(queryset,many=True,context={'request':self.context['request']})
        return serializer.data

class AchievementDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = '__all__' 