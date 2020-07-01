from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login ,logout
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy,reverse
from django.contrib import messages
import datetime
from datetime import datetime
from django.db.models import Count, Max
from django.contrib.sites.shortcuts import get_current_site
import pytz
import openpyxl
import cv2
import re
from django.db.models import Q
from .forms import *
from django.contrib.auth import views as auth_views
from tournament.models import *

class AllTournamentListView(TemplateView):
    def get(self,request,*args,**kwargs):
        tourts = Tournament.objects.all()
        return render(request,'atournament/tournament-all.html',{'tourts':tourts})  

class FilterTournamentView(TemplateView):
    def get(self,request,*args,**kwargs):
        tourts = Tournament.objects.all()
        return render(request,'atournament/tournament-all.html',context={'tourts':tourts})
    def post(self,request,*args,**kwargs):
        startdate_p=request.POST.get('startdate')
        enddate_p=request.POST.get('enddate')
        selection=request.POST.get('selection')

        startdate=startdate_p
        enddate=enddate_p

        if startdate and enddate:
            s=startdate.split('/')
            e=enddate.split('/')
            startdate = datetime(int(s[2]), int(s[0]), int(s[1]), 0, 0, 0, 0, pytz.timezone('Asia/Dubai'))
            enddate = datetime(int(e[2]), int(e[0]), int(e[1]), 23, 59, 59, 999999, pytz.timezone('Asia/Dubai'))
            if selection != 'Select':
                sel = True if selection=='0' else False
                tourts = Tournament.objects.filter(Q(is_active=sel) & Q(Q(start_date__gte=startdate) & Q(end_date__lte=enddate))).order_by('-start_date')
            else:
                tourts = Tournament.objects.filter(Q(start_date__gte=startdate) & Q(end_date__lte=enddate)).order_by('-start_date')
        elif selection != 'Select':
            sel = True if selection=='0' else False
            tourts = Tournament.objects.filter(is_active=sel).order_by('-start_date')
        else:
            tourts = Tournament.objects.all().order_by('-start_date')

        return render(request,'atournament/tournament-all.html',context={'tourts':tourts, 'selection':selection, 'startdate':startdate_p, 'enddate':enddate_p})

class AddTournamentView(TemplateView):
    def get(self,request,*args,**kwargs):
        return render(request,'atournament/add-tournament.html',)  
    def post(self,request,*args,**kwargs):
        form = CreateTournamentForm(data=request.POST or None,)
        message=''
        context=''
        tname = request.POST['tname']
        tstart_date = request.POST['tstart_date']
        tend_date = request.POST['tend_date']
        # tduration = request.POST['tduration'] 
        tlimit = request.POST['tlimit']
        tcond = request.POST.getlist('tcond')
        thh = request.POST['thh']
        tmm = request.POST['tmm']
        trounds = request.POST['trounds']
        trating = request.POST['trating']

        print(tcond)
        
        if form.is_valid():
            tstart_date=tstart_date.split('/')
            tend_date=tend_date.split('/')
            tstart_date = datetime.date(int(tstart_date[2]),int(tstart_date[0]),int(tstart_date[1]))
            tend_date = datetime.date(int(tend_date[2]),int(tend_date[0]),int(tend_date[1]))

            thh = int(thh)
            tmm = int(tmm)
            tstart_time = datetime.time(thh, tmm, 00)

            t = Tournament(
                name = tname,
                game_time_limit = tlimit,
                start_date = tstart_date,
                end_date = tend_date,
                duration = 10,
                start_time = tstart_time,
                rounds = trounds,
                rating = trating,
                # duration = tduration,
            )
            t.save()
            if '1' in tcond:
                print('hi')
                t.is_only_sub_members = True
            if '2' in tcond:
                print('hello')
                t.is_entry_before_tournament = True
            if '3' in tcond:
                t.is_entry_after_half_time = True
            t.save()

            send_notification_to_all()

            message="Tournament added successfully"
            messages.add_message(request, messages.INFO, message)
            return render(request,'atournament/add-tournament.html')

        context = {
            'tname':tname,
            'tstart_date':tstart_date,
            'tend_date':tend_date,
            # 'tduration':tduration,
            'tlimit':tlimit,
            'tcond':tcond,
            'thh': thh,
            'tmm': tmm,
            'trounds': trounds,
            'trating': trating
        }
        messages.add_message(request, messages.INFO, message)
        return render(request,'atournament/add-tournament.html',{'form':form,'context':context})

class ViewTournament(TemplateView):
    def get(self,request,*args,**kwargs):
        id = self.kwargs['pk']
        tourt = Tournament.objects.filter(id=id).first()

        total_game_played=""
        most_games_played_by=""
        most_games_won_by=""
        most_games_lost_by=""
        best_winning_streak=""
        leader_board=""

        total_game_played = TournamentGameManager.objects.filter(tournament=tourt).count()
        if total_game_played!=0:
            most_games_played_by = TournamentPlayerManager.objects.filter(tournament=tourt).annotate(Max('total_games_played')).order_by('-total_games_played__max').first().player.name
            most_games_won_by = TournamentPlayerManager.objects.filter(tournament=tourt).annotate(Max('total_games_won')).order_by('-total_games_won__max').first().player.name
            most_games_lost_by = TournamentPlayerManager.objects.filter(tournament=tourt).annotate(Max('total_games_lost')).order_by('-total_games_lost__max').first().player.name
            best_winning_streak = TournamentGameManager.objects.filter(tournament=tourt).values('winning_streak').annotate(Count('id')).order_by('-id__count').first()['winning_streak']

            leader_board = TournamentPlayerManager.objects.filter(tournament=tourt).order_by('-points')[0:10]

        return render(request,'atournament/view-tournament.html',context={
                                                                    'tourt':tourt,
                                                                    'total_game_played':total_game_played,
                                                                    'most_games_played_by':most_games_played_by,
                                                                    'most_games_won_by':most_games_won_by,
                                                                    'most_games_lost_by':most_games_lost_by,
                                                                    'best_winning_streak':best_winning_streak,
                                                                    'leader_board':leader_board,
                                                                })  

class ImportTournamentView(TemplateView):
    def get(self,request,*args,**kwargs):
        tourts = Tournament.objects.all()        
        return render(request,'atournament/tournament-all.html',{'tourts':tourts}) 
    def post(self,request,*args,**kwargs):    
        message=''    
        excel_file = request.FILES["excel_file"]
        wb = openpyxl.load_workbook(excel_file)
        worksheet = wb["Sheet1"]
        print(worksheet)
        excel_data = list()
        for row in worksheet.iter_rows():
            row_data = list()
            for cell in row:
                row_data.append(str(cell.value))
            excel_data.append(row_data)

        status = validate_excel(excel_data)
        print(status)
        if status!="1":
            messages.add_message(request, messages.INFO, status)
            return HttpResponseRedirect('/admin_panel/tournament/tournament_list')
        
        counter=0
        for row_data in excel_data:
            counter+=1
            if counter!=1:
                thh = int(row_data[3].split(':')[0])
                tmm = int(row_data[3].split(':')[1])
                tstart_time = datetime.time(thh, tmm, 00)
                t = Tournament(
                    name = row_data[0],
                    start_date = row_data[1].split(' ')[0],
                    end_date = row_data[2].split(' ')[0],
                    duration = 10,
                    start_time = tstart_time,
                    rounds = row_data[4],
                    game_time_limit = row_data[5],
                    rating = row_data[6],
                )
                t.save()
                t.is_only_sub_members = True if row_data[7] == '1' else False
                t.is_entry_before_tournament = True if row_data[8] == '1' else False
                t.is_entry_after_half_time = True if row_data[9] == '1' else False
                t.save()

        message='Data saved successfully'
        messages.add_message(request, messages.INFO, message)
        return HttpResponseRedirect('/admin_panel/tournament/tournament_list')

def validate_excel(excel_data):
    counter=0
    if len(excel_data[0])<8:
        return 'Please use proper excel file format'
    if len(excel_data)==1:
        return 'There is no data available in the file'
    for row_data in excel_data:
        print(row_data)
        print(row_data[0])
        counter += 1
        tName=row_data[0]
        tStartDate=row_data[1]
        tEndDate=row_data[2]
        # tDuration=row_data[3]
        tStartTime=row_data[3]
        tRounds=row_data[4]
        tTimeLimit=row_data[5]
        tRating=row_data[6]
        tC1=row_data[7]
        tC2=row_data[8]
        tC3=row_data[9]
        print(counter)
        if counter==1:
            if (tName!='Name' or tStartDate!='Start Date(YYYY-MM-DD)' 
            or tEndDate!='End Date(YYYY-MM-DD)' or tStartTime!='Start Time(24 hr format)' or tRounds!='Number of Rounds(1-20)' or tTimeLimit!='Time Control(mins)' or tRating!='Rating(1-5)' 
            or tC1!='Allow Entery For Subscribed Members Only? [1=yes,0=no]' or tC2!='Allow User to Enter Tournament Before Starting? [1=yes,0=no]' 
            or tC3!='Allow User to Enter More Than Half Way Around Tournament Time is Passed? [1=yes,0=no]'):
                return 'Please use proper column names'
        else:
            tStartDate = tStartDate.split(' ')[0]
            tEndDate = tEndDate.split(' ')[0]

            if not tName or tName=="":
                return 'Please provide Name at row '+str(counter)
            if not tStartDate or tStartDate=="":
                return 'Please provide Start Date at row '+str(counter)
            if not tEndDate or tEndDate=="":
                return 'Please provide End Date at row '+str(counter)
            if not tStartTime or tStartTime=="":
                return 'Please provide Start Time at row '+str(counter)
            if not tRounds or tRounds=="":
                return 'Please provide Rounds at row '+str(counter)
            if not tTimeLimit or tTimeLimit=="":
                return 'Please provide Time Limit at row '+str(counter)
            if not tRating or tRating=="":
                return 'Please provide Rating at row '+str(counter)
            if not tC1 or tC1=="":
                return "Please provide 0 or 1 at row="+str(counter)+", column=6"
            if not tC2 or tC2=="":
                return "Please provide 0 or 1 at row "+str(counter)+", column=7"
            if not tC3 or tC3=="":
                return "Please provide 0 or 1 at row "+str(counter)+", column=8"
            
            if '-' in tStartDate:
                if len(tStartDate.split('-'))==3:
                    try:
                        x = datetime.datetime.strptime(tStartDate, '%Y-%m-%d')
                        y = datetime.datetime.now().date()
                        if y<x.date():
                            return "Start Date can not be greater than today at row "+str(counter)
                    except ValueError:
                        return "Incorrect Start Date format, should be YYYY-MM-DD at row "+str(counter)
                else:
                    return 'Start Date is not in proper format at row '+str(counter)
            else:
                return 'Start Date is not in proper format at row '+str(counter)

            if '-' in tEndDate:
                if len(tEndDate.split('-'))==3:
                    try:
                        x = datetime.datetime.strptime(tEndDate, '%Y-%m-%d')
                        y = datetime.datetime.strptime(tStartDate, '%Y-%m-%d').date()
                        if y>x.date():
                            return "End Date can not be less than Start Date at row "+str(counter)
                    except ValueError:
                        return "Incorrect End Date format, should be YYYY-MM-DD at row "+str(counter)
                else:
                    return 'End Date is not in proper format at row '+str(counter)
            else:
                return 'End Date is not in proper format at row '+str(counter)
            # if not tDuration.isnumeric():
            #     return 'Duration must be numeric at row '+str(counter)
            # else:
            #     d = int(tDuration)
            #     x = datetime.datetime.strptime(tEndDate, '%Y-%m-%d')
            #     y = datetime.datetime.strptime(tStartDate, '%Y-%m-%d')
            #     diff = x.date()-y.date()
            #     if d!=diff.days:
            #         return 'Duration is not valid at row '+str(counter)
            if ':' not in tStartTime:
                return 'Start Time is invalid at row '+str(counter)
            stt=tStartTime.split(':')
            if not stt[0].isnumeric():
                return 'Start Time is invalid at row '+str(counter)
            if not stt[1].isnumeric():
                return 'Start Time is invalid at row '+str(counter)
            hh=int(stt[0])
            mm=int(stt[1])
            if hh==0 and mm==0:
                return 'Start Time is invalid at row '+str(counter)
            if hh<0 or hh>23:
                return 'Start Time is invalid at row '+str(counter)
            if mm<0 or mm>60:
                return 'Start Time is invalid at row '+str(counter)
            if not tRounds.isnumeric():
                return 'Round is invalid at row '+str(counter)
            ro=int(tRounds)
            if ro<1 or ro>20:
                print('hii')
                return 'Round is invalid at row '+str(counter)
            
            if not tTimeLimit.isnumeric():
                return 'Time Limit must be numeric at row '+str(counter)
            else:
                d = int(tTimeLimit)
                if d>30 or d<5:
                    return 'Time Limit is not valid at row '+str(counter)

            if not tRating.isnumeric():
                return 'Rating is invalid at row '+str(counter)
            ro=int(tRating)
            if ro<0 or ro>5:
                return 'Rating is invalid at row '+str(counter)
            
            if tC1 not in ('1','0'):
                return "Please provide 0 or 1 at row "+str(counter)+", column=6"
            if tC2 not in ('1','0'):
                return "Please provide 0 or 1 at row "+str(counter)+", column=7"
            if tC3 not in ('1','0'):
                return "Please provide 0 or 1 at row "+str(counter)+", column=8"
            if len(tName)>450:
                return "Name length is exceeding at row "+str(counter)

    return "1"

from pyfcm import FCMNotification
def send_notification_to_all():
    api_key=''
    if api_key!='':
        print('inside push notification')
        ids = User.objects.filter(is_active=True,is_superuser=False).values_list('device_token',flat=True)
        ids = list(ids)

        push_service= FCMNotification(api_key=api_key)
        registration_ids=ids
        message_title="KishMalik Notification"
        message_body='Please check a new article added in the list'
        result=push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title, message_body=message_body)

        users = User.objects.filter(is_active=True,is_superuser=False)
        for u in users:
            un=UserNotification(
                user=u,
                notification=notification_msg,
                req_type='6',
            )
            un.save()
        return True
    return False