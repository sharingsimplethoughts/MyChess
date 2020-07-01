from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (AllowAny,IsAuthenticated,)
from accounts.api.permissions import IsTokenValid
from rest_framework_jwt.authentication import  JSONWebTokenAuthentication
from django.db.models import Q
from django.db.models import Sum
from accounts.models import *
# from category.models import *
from tournament.models import *
from .serializers import *
import openpyxl
import datetime

import logging
logger = logging.getLogger('accounts')


class AvailableTournamentListView(APIView):
    permission_classes=[IsAuthenticated, IsTokenValid,]
    authentication_classes=[JSONWebTokenAuthentication,]
    def get(self,request,*args,**kwargs):
        user=request.user
        existing = TournamentPlayerManager.objects.filter(player=user,tournament__is_active=True).first()
        # queryset = Tournament.objects.filter(is_active=True)
        queryset = Tournament.objects.filter(end_date__gte=datetime.datetime.now())
        if existing:
            # queryset = Tournament.objects.filter(is_active=True).exclude(id=existing.tournament.id)
            queryset = Tournament.objects.filter(end_date__gte=datetime.datetime.now()).exclude(id=existing.tournament.id)
        serializer = AvailableTournamentListSerializer(queryset,many=True,context={'request':request})
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

class JoinedTournamentListView(APIView):
    permission_classes=[IsAuthenticated, IsTokenValid,]
    authentication_classes=[JSONWebTokenAuthentication,]
    def get(self,request,*args,**kwargs):
        user=request.user
        tourt = TournamentPlayerManager.objects.filter(Q(player=user),tournament__is_active=True).first()
        if tourt:
            serializer = JoinedTournamentListSerializer(tourt.tournament,context={'request':request})
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
        return Response({
            'message':'User has not joined any tournament.',
            'success':'False',
        },status=400,)

class JoinTournamentView(APIView):
    permission_classes=[IsAuthenticated, IsTokenValid,]
    authentication_classes=[JSONWebTokenAuthentication,]
    def post(self,request,*args,**kwargs):
        user=request.user
        # id=self.kwargs['pk']
        print(request.data)
        if 'tid' in request.data.keys():
            tid = request.data['tid']
            if not tid or tid=="":
                return Response({
                    'message':'Tournament id missing',
                    'success':'False',
                },status=400,)
        else:
            return Response({
                'message':'Tournament id missing',
                'success':'False',
            },status=400,)
        t = Tournament.objects.filter(id=tid).first()
        check1=check2=check3=1
        if t:
            # is_only_sub_members,is_entry_before_tournament,is_entry_after_half_time,is_active
            if t.is_only_sub_members:
                if not user.is_subscribed:
                    check1=0
                    message='You must subscribe to a plan before joining to this tournament.'
            if t.is_entry_before_tournament:
                d = datetime.datetime.combine(t.start_date, datetime.datetime.min.time())
                diff = d-datetime.datetime.now()
                print(d)
                print(datetime.datetime.now())
                print('00000')
                print(diff.total_seconds())
                if diff.total_seconds()<=0:
                    check2=0
                    message='You should have joined this tournament before its start date.'
            if t.is_entry_after_half_time:
                a = datetime.datetime.combine(t.start_date, datetime.datetime.min.time())
                b = datetime.datetime.combine(t.end_date, datetime.datetime.min.time())
                c = a + (b - a)/2
                if c<datetime.datetime.now():
                    check3=0
                    message='Already half of the tournament is gone. Please join another tournament.'
            if check1 and check2 and check3:
                tpm = TournamentPlayerManager.objects.filter(player=user,tournament__is_active=True).first()
                if tpm:
                    tpm.tournament = t
                    tpm.points = 0
                    tpm.total_games_played = 0
                    tpm.total_games_won = 0
                    tpm.total_games_lost = 0
                    tpm.save()
                else:
                    tpm = TournamentPlayerManager(
                    tournament = t,
                    player = user,
                    )
                    tpm.save()

                serializer=TournamentStandingsSerializer(t,context={'request':request})
                if serializer:
                    return Response({
                        'message':'Joined the tournament successfully',
                        'success':'True',
                        'data':serializer.data,
                    },status=200,)
            else:
                return Response({
                    'message':message,
                    'success':'False',
                },status=200,)
        return Response({
            'message':'Invalid tournament id',
            'success':'False',
        },status=400,)

class TournamentStandingsView(APIView):
    permission_classes=[IsAuthenticated, IsTokenValid,]
    authentication_classes=[JSONWebTokenAuthentication,]
    def get(self,request,*args,**kwargs):
        id = self.kwargs['pk']
        t=Tournament.objects.filter(id=id).first()
        if t:
            # queryset=TournamentPlayerManager.objects.filter(tournament=t).order_by('points')
            serializer=TournamentStandingsSerializer(t,context={'request':request})
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
        return Response({
            'message':'Invalid tournament id',
            'success':'False',
        },status=400,)

class UserTournamentStatusView(APIView):
    permission_classes=[IsAuthenticated, IsTokenValid,]
    authentication_classes=[JSONWebTokenAuthentication,]
    def get(self,request,*args, **kwargs):
        user=request.user
        queryset = TournamentPlayerManager.objects.filter(player=user,tournament__is_active=True).first()
        if queryset:
            serializer = UserTournamentStatusSerializer(queryset,context={'request':request})
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
        return Response({
            'message':'Sorry, this user has not joined any tournament yet.',
            'success':'False',
        },status=400,)

class DeleteTournamentView(APIView):
    def post(self,request,*args,**kwargs):
        pk = self.kwargs['pk']
        tournament = Tournament.objects.filter(id=pk).first()
        if tournament:
            tournament.delete()
            return Response({
                'message':'Successfully deleted record',
                'success':'True'
            },200)
        else:
            return Response({
                'message':'Not item available to delete',
                'success':'False'
            },400)

class RateTournamentView(APIView):
    permission_classes=[IsAuthenticated, IsTokenValid,]
    authentication_classes=[JSONWebTokenAuthentication,]
    def post(self,request,*args, **kwargs):
        user = request.user
        if 'tid' in request.data.keys():
            tid = request.data['tid']
            if not tid or tid=="":
                return Response({
                    'message':'Tournament id missing',
                    'success':'False',
                },status=400,)
        else:
            return Response({
                'message':'Tournament id missing',
                'success':'False',
            },status=400,)
        t = Tournament.objects.filter(id=tid).first()
        if t:
            if 'rating' in request.data.keys():
                rating = request.data['rating']
                if not rating or rating=="":
                    return Response({
                        'message':'Rating is missing',
                        'success':'False',
                    },status=400,)
            else:
                return Response({
                    'message':'Rating is missing',
                    'success':'False',
                },status=400,)

            if rating not in ['1','2','3','4','5']:
                return Response({
                    'message':'Rating must be in between 1 to 5',
                    'success':'False',
                },status=400,)
            tpm = TournamentPlayerManager.objects.filter(player=user,tournament=t).first()
            if tpm:
                tpm.rating = int(rating)
                tpm.save()
                tpmcount = TournamentPlayerManager.objects.filter(tournament=t).exclude(rating=0).count()
                tpms = TournamentPlayerManager.objects.filter(tournament=t).aggregate(sum=Sum('rating'))
                tpmsum = tpms['sum']
                t.rating = tpmsum/tpmcount
                t.save()
                return Response({
                    'message':'Rating saved successfully',
                    'success':'True',
                },status=200,)
            return Response({
                'message':'You must join this tournament to give rating',
                'success':'False',
            },status=400,)

        return Response({
            'message':'Invalid tournament id',
            'success':'False',
        },status=400,)
            

class SpecialApiView(APIView):
    def post(self,request,*args, **kwargs):
        pk = request.data['id']
        if not pk or pk=='':
            return Response({
                'status':False,
            },400)
        else:
            tournament = Tournament.objects.filter(id=pk).first()
            if tournament:
                return Response({
                    'status':True,
                },200)
            else:
                return Response({
                    'status':False,
                },400)
