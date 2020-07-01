from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.contrib import messages
from accounts.models import *
from django.db.models import Sum,Max,Count
import pytz
import csv
from django.http import HttpResponse

from django.db.models import Q
from achievement.models import AchievementManager
from achievement.api.serializers import AchievementDetailSerializer
from game.models import Game
from lessons.models import LessonManagement
from articles.models import VideoWatchHistory
from tournament.models import *
import datetime


# Create your views here.
class LeaderBoardListView(TemplateView):
    def get(self,request,*args, **kwargs):
        queryset=PlayerPoint.objects.values('player').annotate(sumofpoint=Sum('point')).order_by('-sumofpoint')[:10]
        context=[]
        i=0
        track='2'
        for q in queryset:
            player=User.objects.filter(id=q['player']).first()
            context.append({
                'point':q['sumofpoint'],
                'player':player,
            })
            i=i+1
        return render(request,'aleaderboard/leaderboard.html',{'context':context,'track':track})
    def post(self,request,*args,**kwargs):
        print('------------------------------------')
        period=request.POST.get('period')
        print(period)
        queryset=[]
        if period=='0':
            print('today')
            todate=datetime.datetime.now().date()
            queryset=PlayerPoint.objects.filter(created_on=todate).values('player').annotate(sumofpoint=Sum('point')).order_by('-sumofpoint')[:10]
            print(queryset)
        elif period=='1':
            #week
            todate=datetime.datetime.now().date()
            sevendaysearlierdate=(datetime.datetime.now()-datetime.timedelta(days=7)).date()
            queryset=PlayerPoint.objects.filter(created_on__lte=todate,created_on__gte=sevendaysearlierdate).values('player').annotate(sumofpoint=Sum('point')).order_by('-sumofpoint')[:10]
            # queryset=PlayerPoint.objects.filter(created_on__range=(todate,sevendaysearlierdate)).values('player').annotate(sumofpoint=Sum('point')).order_by('-sumofpoint')[:10]
        else:
            #all
            queryset=PlayerPoint.objects.values('player').annotate(sumofpoint=Sum('point')).order_by('-sumofpoint')[:10]
        context=[]
        i=0
        for q in queryset:
            player=User.objects.filter(id=q['player']).first()
            context.append({
                'point':q['sumofpoint'],
                'player':player,
            })
            i=i+1
        print(context)
        return render(request,'aleaderboard/leaderboard.html',{'context':context,'track':period})

class LeaderBoardExportView(TemplateView):
    def post(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="report.csv"'
        writer = csv.writer(response)
        field_names=['User ID','Rank','Name','Country','Point']
        writer.writerow(field_names)
        counter=0
        period=request.POST.get('track')
        print(period)
        if not period or period=="":
            period=0
        print(period)
        if period==0:
            #today
            todate=datetime.datetime.now().date()
            queryset=PlayerPoint.objects.filter(created_on=todate).values('player').annotate(sumofpoint=Sum('point')).order_by('-sumofpoint')[:10]
        elif period==1:
            #week
            todate=datetime.datetime.now().date()
            sevendaysearlierdate=(datetime.datetime.now()-datetime.timedelta(days=7)).date()
            queryset=PlayerPoint.objects.filter(created_on__range=(todate,sevendaysearlierdate)).values('player').annotate(sumofpoint=Sum('point')).order_by('-sumofpoint')[:10]
        else:
            #all
            queryset=PlayerPoint.objects.values('player').annotate(sumofpoint=Sum('point')).order_by('-sumofpoint')[:10]

        context=[]
        i=0
        for q in queryset:
            player=User.objects.filter(id=q['player']).first()
            # field_names=['User ID','Rank','Name','Country','Points']
            # field_names=['User ID','User Name','Mobile Number','Email ID','Country']
            counter+=1
            row=[player.id]
            row.append(counter)
            if player.name:
                row.append(player.name)
            else:
                row.append('No Name')
            if player.country:
                row.append(player.country)
            else:
                row.append('No Country Selected')
            row.append(q['sumofpoint'])
            writer.writerow(row)

        return response

class LeaderDetailView(TemplateView):
    def get(self,request,*args,**kwargs):
        id = self.kwargs['pk']
        rank = self.kwargs['rank']
        user=User.objects.filter(id=id).first()
        instance=user
        tgame=Game.objects.filter(Q(player1=instance)|Q(player2=instance)).count()
        tgwon=Game.objects.filter(winner=instance).count()
        tglost=Game.objects.filter(Q(player1=instance)|Q(player2=instance)&Q(winner=None)).count()
        tpoints=user.total_points
        ttourn=TournamentPlayerManager.objects.filter(player=instance).count()
        tach=AchievementManager.objects.filter(player=instance).count()

        # bwstreak=====================
        wgames=Game.objects.filter(winner=instance)
        bwstreak=TournamentGameManager.objects.filter(game__in=wgames).values('winning_streak').annotate(count=Count('game')).order_by('-count').first()['winning_streak']
        # ttwon=========================
        tpm1=TournamentPlayerManager.objects.values('tournament').annotate(point=Max('points'))
        wcount=0
        for t in tpm1:
            t=TournamentPlayerManager.objects.filter(tournament__id=t['tournament'],points=t['point']).first()
            if t.player.id==instance.id:
                wcount=wcount+1
        
        player = {
            'tgame':tgame,
            'tgwon':tgwon,
            'tglost':tglost,
            'tpoints':tpoints,
            'bwstreak':bwstreak,
            'ttourn':ttourn,
            'ttwon':wcount,
            'tach':tach
        }

        return render(request,'aleaderboard/detail-view.html',{'user':user,'player':player,'rank':rank})
        


class PlayerPointDetailView(TemplateView):
    def get(self,request,*args, **kwargs):
        id = self.kwargs['pk']
        tid = self.kwargs['tid']
        player=User.objects.filter(id=id).first()
        t=''
        if tid==0:
            queryset=Game.objects.filter(Q(player1=player)|Q(player2=player))
        else:
            t = Tournament.objects.filter(id=tid).first()
            glist = TournamentGameManager.objects.filter(tournament=t).values_list('game').distinct()
            queryset=Game.objects.filter(player1=player,id__in=glist)
        return render(request,'aleaderboard/user-detail-points.html',{'context':queryset,'t':t,'tid':tid,'pk':id})

class PlayerPointDetailExportView(TemplateView):
    def post(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="report.csv"'
        writer = csv.writer(response)
        field_names=['Player1 ID','Player1 Name','Player2 ID','Player2 Name','Winner','Player1 Point','Player2 Point','Date']
        writer.writerow(field_names)
        counter=0
        tid=request.POST.get('tid')
        id=request.POST.get('pk')
        player=User.objects.filter(id=id).first()
        print(tid)
        if tid==0:
            queryset=Game.objects.filter(Q(player1=player)|Q(player2=player))
        else:
            t = Tournament.objects.filter(id=tid).first()
            glist = TournamentGameManager.objects.filter(tournament=t).values_list('game').distinct()
            queryset=Game.objects.filter(player1=player,id__in=glist)

        context=[]
        i=0
        for q in queryset:
            counter+=1
            row=[q.player1.id]
            # row.append(counter)
            # row=[counter]
            # row.append(q.player1.id)
            row.append(q.player1.name)
            row.append(q.player2.id)
            row.append(q.player2.name)
            if q.winner:
                row.append(q.winner.name)
            else:
                row.append(' ')
            row.append(q.player1_point)
            row.append(q.player2_point)
            row.append(q.created_on)
            
            writer.writerow(row)

        return response