from celery import shared_task
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from dateutil.relativedelta import relativedelta
from pyfcm import FCMNotification
import datetime
from datetime import timedelta
from django.db.models import Max

from accounts.models import *
from usubscription.models import *

api_key = ''

@periodic_task(run_every=crontab(hour=1, minute=5, day_of_week="sun,mon,tue,wed,thu,fri,sat"))
def everyday_night_tournament_end():
    api_key=''
    if api_key!='':
        push_service_sp = FCMNotification(api_key=api_key)
        print('inside push notification')
        yesterday = datetime.datetime.now().date()-timedelta(1)
        tlist = Tournament.objects.filter(end_date=yesterday)
        
        tpm = TournamentPlayerManager.objects.filter(tournament__in=tlist).values('tournament').annotate(max_point=Max('points'))
        for t in tpm:
            t_winners = TournamentPlayerManager.objects.filter(tournament = t.tournament, points = t.max_point)
            tname = t.tournament.name
            count=0
            for w in t_winners:
                winner_name = w.name + ','
                count+=1
            winner_name = winner_name[0:-1]
            notification_msg=''
            if count==1:
                notification_msg = 'The winner of '+tname+' is '+winner_name
            if count>1:
                notification_msg = 'The winners of '+tname+' are '+winner_name
            
            players_list = TournamentPlayerManager.objects.filter(tournament=t.tournament).values_list('player__device_token',flat=True)
            players_list = list(players_list)

            push_service= push_service_sp
            registration_ids=players_list
            message_title="KishMalik Notification"
            message_body=notification_msg
            result=push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title, message_body=message_body)

            pp = TournamentPlayerManager.objects.filter(tournament=t.tournament)
            for p in pp:
                un=UserNotification(
                    user=p.player,
                    notification=notification_msg,
                    req_type='10',
                )
                un.save()
            
@periodic_task(run_every=crontab(hour=7, minute=30, day_of_week="sun,mon,tue,wed,thu,fri,sat"))
def every_day_morning():
    dt = datetime.datetime.now()+timedelta(7)
    dt = dt.replace(tzinfo=timezone.utc)
    usersub_qs=UserSubscription.objects.filter(user__is_active=True,user__is_superuser=False,exp_date__lt=dt).values_list('user__device_token',flat=True)
    if usersub_qs:
        api_key=''
        if api_key!='':
            push_service_sp = FCMNotification(api_key=api_key)
            push_service = push_service_sp
            registration_ids=usersub_qs
            message_title="KishMalik Subscription Plan"
            message_body='Please subscribe to a new plan to continue with offer creation for your garage. Your current plan expiry date: '+str(s.expires_on.date())+'. If already subscribed then please ignore this.'
            result=push_service.notify_multiple_devices(registration_id=registration_ids, message_title=message_title, message_body=message_body)

            us = UserSubscription.objects.filter(user__is_active=True,user__is_superuser=False,exp_date__lt=dt)
            for s in us:
                un=UserNotification(
                    user=s.user,
                    notification=notification_msg,
                    req_type='11',
                )
                un.save()









