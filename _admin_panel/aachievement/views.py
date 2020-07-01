from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login ,logout
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy,reverse
from django.contrib import messages
from achievement.models import *
import openpyxl

# Create your views here.
class AchivementListView(TemplateView):
    def get(self,request,*args, **kwargs):
        achlist = Achievement.objects.filter(is_deleted=False)
        return render(request,'aachievement/achievement.html',context={'achlist':achlist})

class AddAchievementView(TemplateView):
    def get(self,request,*args, **kwargs):
        # id = self.kwargs['pk']
        # ach = Achievement.objects.filter(id=id).first()
        return render(request,'aachievement/add-achievement.html',)
    def post(self,request,*args, **kwargs):
        # form = AddAchievementForm(data=request.POST or None)
        name = request.POST['name']
        unlock_task = request.POST['comment']
        image = request.FILES.get('ach_image')
        data={}
        data['name']=name
        data['unlock_task']=unlock_task
        # if form.is_valid():
        if image:
            ach = Achievement(
                name=name,
                unlock_task=unlock_task,
                image=image,
            )
            ach.save()
            ach.image_url=ach.image.url
            ach.save()
            message = "Achievement added successfully"
            send_notification_to_all()
        else:
            message = "Please provide image"
        messages.add_message(request, messages.INFO, message)
        return render(request,'aachievement/add-achievement.html',context={'data':data})
        # return render(request,'aachievement/add-achievement.html',context={'data':data})

class ImportAchievementView(TemplateView):
    def post(self,request,*args,**kwargs):
        message=''
        excel_file = request.FILES["excel_file"]
        wb = openpyxl.load_workbook(excel_file)
        worksheet = wb["Sheet1"]
        excel_data = list()
        for row in worksheet.iter_rows():
            row_data = list()
            for cell in row:
                row_data.append(str(cell.value))
            excel_data.append(row_data)
        status = validate_excel(excel_data)
        if status!="1":
            messages.add_message(request, messages.INFO, status)
            return HttpResponseRedirect('/admin_panel/achievement/list')     
        counter=0
        for row_data in excel_data:
            counter+=1
            if counter!=1:
                ach = Achievement(
                    name=row_data[0],
                    unlock_task=row_data[1],
                    image_url=row_data[2]
                )
                ach.save()
                message='Data saved successfully'
        messages.add_message(request, messages.INFO, message)
        return HttpResponseRedirect('/admin_panel/achievement/list')  

def validate_excel(excel_data):
    counter=0
    less_id_list=[]
    if len(excel_data[0])<3:
        return 'Please use proper excel file format'
    for row_data in excel_data:
        counter += 1
        name=row_data[0]
        unlock_task=row_data[1]
        image=row_data[2]
        if counter==1:
            if (name!='Name' or unlock_task!='Unlock Task' 
                or image!='Icon Link'):
                return 'Please use proper excel file format'
        else:
            if not name or name=="":
                return 'Please provide name at row '+str(counter)
            if not unlock_task or unlock_task=="":
                return 'Please provide unlock task '+str(counter)
            if not image or image=="":
                return 'Please provide icon link '+str(counter)
            if len(name)>90:
                return "Name length is exceeding at row "+str(counter)
            if len(unlock_task)>900:
                return "Unlock task length is exceeding at row "+str(counter)
            if 'http' not in image:
                return "Please provide valid icon link at row "+str(counter)
    if counter in (0,1):
        return "Excel file is empty"
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

