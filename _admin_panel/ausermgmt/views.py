from django.shortcuts import render
from django.views.generic import TemplateView
from datetime import datetime
import pytz
import csv
from django.http import HttpResponse
from accounts.models import *

from django.db.models import Sum,Max,Count
from django.db.models import Q
from achievement.models import AchievementManager
from achievement.api.serializers import AchievementDetailSerializer
from game.models import Game
from lessons.models import LessonManagement
from articles.models import VideoWatchHistory
from tournament.models import *

start_date = ""
end_date = ""
c = ""
# Create your views here.
class UserManagementListView(TemplateView):
    def get(self,request,*args,**kwargs):
        users = User.objects.all().exclude(is_superuser=True).order_by('-created_on')
        clist = CountryCode.objects.all()
        return render(request,'ausermgmt/user-management.html',{'users':users,'clist':clist})  
    def post(self,request,*args,**kwargs):
        start_date=request.POST.get('start_date')
        end_date=request.POST.get('end_date')
        status=request.POST.get('status')
        c=""
        
        startdate_p=start_date
        enddate_p=end_date
        status_p=status

        if start_date and end_date:
            s=start_date.split('/')
            e=end_date.split('/')
            start_date = datetime(int(s[2]), int(s[0]), int(s[1]), 0, 0, 0, 0, pytz.timezone('Asia/Dubai'))
            end_date = datetime(int(e[2]), int(e[0]), int(e[1]), 23, 59, 59, 999999, pytz.timezone('Asia/Dubai'))

        if status!='default' and (status or status!=""):
            c = CountryCode.objects.filter(id=status).first()
        
        if start_date and end_date and c:
            users = User.objects.filter(country=c.country,created_on__range=(start_date,end_date),is_superuser=False).order_by('-created_on')
        elif start_date and end_date and (not c or c==""):
            users = User.objects.filter(created_on__range=(start_date,end_date),is_superuser=False).order_by('-created_on')
        elif ((not start_date or start_date=="") or (not end_date or end_date=="")) and c:
            users = User.objects.filter(country=c.country,is_superuser=False).order_by('-created_on')
        else:
            users = User.objects.filter(is_superuser=False).order_by('-created_on')

        clist = CountryCode.objects.all()
        if status_p=='default':
            return render(request,'ausermgmt/user-management.html',{'users':users,'clist':clist, 'status':status_p, 'start_date':startdate_p, 'end_date':enddate_p})
        else:
            return render(request,'ausermgmt/user-management.html',{'users':users,'clist':clist, 'status':int(status_p), 'start_date':startdate_p, 'end_date':enddate_p})

class UserExportView(TemplateView):
    def post(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="report.csv"'
        writer = csv.writer(response)
        field_names=['User ID','User Name','Mobile Number','Email ID','Country']
        writer.writerow(field_names)
        counter=0

        start_date=request.POST.get('stdt')
        end_date=request.POST.get('eddt')
        status=request.POST.get('status_p')

        print(start_date)
        print(end_date)
        print(status)

        if start_date and end_date:
            s=start_date.split('/')
            e=end_date.split('/')
            start_date = datetime(int(s[2]), int(s[0]), int(s[1]), 0, 0, 0, 0, pytz.timezone('Asia/Dubai'))
            end_date = datetime(int(e[2]), int(e[0]), int(e[1]), 23, 59, 59, 999999, pytz.timezone('Asia/Dubai'))
        if status:
            c = CountryCode.objects.filter(id=status).first()
        
        if start_date and end_date and c:
            users = User.objects.filter(country=c.country,created_on__range=(start_date,end_date),is_superuser=False).order_by('-created_on')
        elif start_date and end_date and (not c or c==""):
            users = User.objects.filter(created_on__range=(start_date,end_date),is_superuser=False).order_by('-created_on')
        elif ((not start_date or start_date=="") or (not end_date or end_date=="")) and c:
            users = User.objects.filter(country=c.country,is_superuser=False).order_by('-created_on')
        else:
            users = User.objects.filter(is_superuser=False).order_by('-created_on')

        for u in users:
            counter+=1
            row=[u.id]
            if u.name:
                row.append(u.name)
            else:
                row.append('No Name')
            if u.mobile:
                if u.mobile==u.social_id:
                    row.append('Social Login')
                else:
                    row.append(u.mobile)
            else:
                row.append('No Mobile Given')
            if u.email:
                if u.social_id:
                    if u.social_id+"@temporary.com"==u.email:
                        row.append('Social Login')
                    else:
                        row.append(u.email)    
                else:
                    row.append(u.email)
            else:
                row.append('No Email Given')
            if u.country:
                row.append(u.country)
            else:
                row.append('No Country Selected')
            writer.writerow(row)

        return response

class UserDetailView(TemplateView):
    def get(self,request,*args,**kwargs):
        id = self.kwargs['pk']
        user=User.objects.filter(id=id).first()
        instance=user

        tgame=Game.objects.filter(Q(player1=instance)|Q(player2=instance)).count()
        tgwon=Game.objects.filter(winner=instance).count()
        tglost=Game.objects.filter(Q(player1=instance)|Q(player2=instance)&Q(winner=None)).count()
        # tpoints=user.total_points
        tlesson=LessonManagement.objects.filter(player=instance).count()
        tvideo=VideoWatchHistory.objects.filter(user=instance).count()
        rank=User.objects.filter(total_points__gte=instance.total_points).count()+1
        ttourn=TournamentPlayerManager.objects.filter(player=instance).count()
        thonor=0
        stdt=''
        eddt=''
        # tach=AchievementManager.objects.filter(player=instance).count()

        # bwstreak=====================
        wgames=Game.objects.filter(winner=instance)
        bwstreak=''
        if wgames:
            bwstreak=TournamentGameManager.objects.filter(game__in=wgames).values('winning_streak').annotate(count=Count('game')).order_by('-count').first()['winning_streak']
        # ttwon=========================
        tpm1=TournamentPlayerManager.objects.values('tournament').annotate(point=Max('points'))
        wcount=0
        if tpm1:
            for t in tpm1:
                t=TournamentPlayerManager.objects.filter(tournament__id=t['tournament'],points=t['point']).first()
                if t.player.id==instance.id:
                    wcount=wcount+1
        
        player = {
            'tgame':tgame,
            'tgwon':tgwon,
            'tglost':tglost,
            'bwstreak':bwstreak,
            'tlesson':tlesson,
            'tvideo':tvideo,
            'rank':rank,
            'ttourn':ttourn,
            'ttwon':wcount,
            'thonor':thonor,
            'stdt':stdt,
            'eddt':eddt
        }

        return render(request,'ausermgmt/user-view.html',{'user':user,'player':player,'rank':rank})