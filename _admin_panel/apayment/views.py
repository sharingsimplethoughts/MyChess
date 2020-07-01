from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
import pytz
import csv
from django.http import HttpResponse
import datetime
from django.utils import timezone
from usubscription.models import *
from accounts.models import User
# Create your views here.
class PaymentListView(TemplateView):
    def get(self,request,*args, **kwargs):
        # todate=datetime.datetime.now().date()
        # today = timezone.now()
        # plist=PaymentDetail.objects.filter(created_on__date=todate)
        plist=PaymentDetail.objects.all()
        print(plist)
        track='2'
        return render(request,'apayment/payments.html',{'plist':plist,'track':track})
    def post(self,request,*args, **kwargs):
        period=request.POST.get('period')
        if period==0:
            #today
            todate=datetime.datetime.now().date()
            plist=PaymentDetail.objects.filter(created_on__date=todate)
        elif period==1:
            #week
            todate=datetime.datetime.now().date()
            sevendaysearlierdate=(datetime.datetime.now()-datetime.timedelta(days=7)).date()
            plist=PaymentDetail.objects.filter(created_on__date__lte=todate,created_on__date__gte=sevendaysearlierdate)
        else:
            #all
            plist=PaymentDetail.objects.all()
        return render(request,'apayment/payments.html',{'plist':plist,'track':period})

class PaymentListExportView(TemplateView):
    def post(self,request,*args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="report.csv"'
        writer = csv.writer(response)
        # TID,Date,UID,User Name,Mobile,Subscription,Payment Mode,Amount
        field_names=['TID','Date','UID','Name','Mobile','Subscription','PaymentMode','Amount']
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
            queryset=PaymentDetail.objects.filter(created_on=todate)
        elif period==1:
            #week
            todate=datetime.datetime.now().date()
            sevendaysearlierdate=(datetime.datetime.now()-datetime.timedelta(days=7)).date()
            queryset=PaymentDetail.objects.filter(created_on__range=(todate,sevendaysearlierdate))
        else:
            #all
            queryset=PaymentDetail.objects.all()

        context=[]
        i=0
        for q in queryset:
            player=User.objects.filter(id=q.player.id).first()
            counter+=1
            # TID,Date,UID,User Name,Mobile,Subscription,Payment Mode,Amount
            row=[q.transaction.tid]
            row.append(q.created_on)
            row.append(player.id)
            if player.name:
                row.append(player.name)
            else:
                row.append('No Name')
            if player.mobile:
                row.append(player.country)
            else:
                row.append('No Mobile')
            row.append(q.subscription_plan.plan_name)
            row.append(q.payment_mode)
            row.append(q.amount)
            writer.writerow(row)

        return response