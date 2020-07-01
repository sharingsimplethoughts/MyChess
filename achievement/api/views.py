from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (AllowAny,IsAuthenticated,)
from accounts.api.permissions import IsTokenValid
from rest_framework_jwt.authentication import  JSONWebTokenAuthentication
from accounts.models import *
from achievement.models import *
from .serializers import *


class AchievementListView(APIView):
    permission_classes=[IsAuthenticated, IsTokenValid,]
    authentication_classes=[JSONWebTokenAuthentication,]
    def get(self,request,*args, **kwargs):
        user=request.user
        queryset = Achievement.objects.filter(is_deleted=False,is_blocked=False).first()
        serializer = AchievementListSerializer(queryset,context={'request':request})
        if serializer:
            return Response({
                'message':'Data retrieved successfully',
                'success':'True',
                'data':serializer.data,
            },status=200,)
        return Response({
            'message':'Data retrieve failed',
            'success':'False',
        },status=400,)

class AchievementDetailView(APIView):
    permission_classes=[IsAuthenticated, IsTokenValid,]
    authentication_classes=[JSONWebTokenAuthentication,]
    def get(self,request,*args, **kwargs):
        id = self.kwargs['pk']
        ach = Achievement.objects.filter(id=id).first()
        if ach:
            serializer = AchievementDetailSerializer(ach,context={'request':request})
            if serializer:
                return Response({
                    'message':'Data retrieved successfully',
                    'success':'True',
                    'data':serializer.data,
                },status=200,)
        return Response({
            'message':'Data retrieve failed',
            'success':'False',
        },status=400,)

class APAchievementDetailView(APIView):
    def get(self,request,*args, **kwargs):
        id = self.kwargs['pk']
        ach = Achievement.objects.filter(id=id).first()
        if ach:
            serializer = AchievementDetailSerializer(ach,context={'request':request})
            if serializer:
                return Response({
                    'message':'Data retrieved successfully',
                    'success':'True',
                    'data':serializer.data,
                },status=200,)
        return Response({
            'message':'Data retrieve failed',
            'success':'False',
        },status=400,)

class APEditAchievementView(APIView):
    def post(self,request,*args, **kwargs):
        id=self.kwargs['pk']
        ach = Achievement.objects.filter(id=id).first()
        if ach:
            # ecomment = request.data['ecomment']
            ecomment = request.POST.get('ecomment')
            print(ecomment)
            if not ecomment or ecomment=="":
                return Response({
                    'message':'Unlock task text is missing',
                    'success':'False',
                },status=400)
            ach.unlock_task = ecomment
            ach.save()
            return Response({
                'message':'Data edited successfully',
                'success':'True',
            },status=200,)
        else:
            return Response({
                'message':'Id is invalid',
                'success':'False',
            },status=400)

class BlockUnblockAchievementView(APIView):
    def get(self,request,*args, **kwargs):
        id=self.kwargs['pk']
        ach = Achievement.objects.filter(id=id).first()
        if ach:
            if ach.is_blocked:
                ach.is_blocked=False
            else:
                ach.is_blocked=True
            ach.save()
            return Response({
                'message':'Data deleted successfully',
                'success':'True',
            },status=200,)
        else:
            return Response({
                'message':'id is invalid',
                'success':'False',
            },status=400,)
class DeleteAchievementView(APIView):
    def get(self,request,*args, **kwargs):
        id=self.kwargs['pk']
        ach = Achievement.objects.filter(id=id).first()
        if ach:
            ach.is_deleted=True
            ach.save()
            return Response({
                'message':'Data deleted successfully',
                'success':'True',
            },status=200,)
        else:
            return Response({
                'message':'id is invalid',
                'success':'False',
            },status=400,)

class AchievementCompletedView(APIView):
    permission_classes=[IsAuthenticated, IsTokenValid,]
    authentication_classes=[JSONWebTokenAuthentication,]
    def post(self,request,*args, **kwargs):
        ach_id=request.data['achievement_id']
        player=request.user
        if not ach_id or ach_id=="":
            return Response({
                'message':'Please provide achievement id',
                'success':'False'
            },status=400)
        ach=Achievement.objects.filter(id=ach_id).first()
        if not ach:
            return Response({
                'message':'Please provide valid achievement id',
                'success':'False'
            },status=400)
        am = AchievementManager(
            achievement=ach,
            player=player
        )
        am.save()
        return Response({
            'message':'Data saved successfully',
            'success':'True'
        },status=200)
