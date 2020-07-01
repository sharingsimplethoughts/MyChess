from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from pyfcm import FCMNotification
from accounts.models import *
from game.models import *
from .forms import *

api_key=''

def send_email_notification():
    pass
def send_sms():
    pass

# Create your views here.
class SendNotification(TemplateView):
    def get(self,request,*args,**kwargs):
        context={}
        context['nt_date']=''
        context['nt_desc']=''
        context['gid_list'] = ''
        context['uid_list'] = ''


        u_obj_list=[]
        g_obj_list=[]
        u_obj=SampleImageStore.objects.filter(unique_identification='un_ap_1').first()
        if u_obj:
            user_list=[u_obj.sample_data]
            if ',' in u_obj.sample_data:
                user_list=u_obj.sample_data.split(',')
            for u in user_list:
                if u:
                    obj = User.objects.filter(id=u).first()
                    if obj:
                        u_obj_list.append(obj)

            g_obj=SampleImageStore.objects.filter(unique_identification='un_ap_2').first()
            group_list=[g_obj.sample_data]
            if ',' in g_obj.sample_data:
                group_list=g_obj.sample_data.split(',')
            for g in group_list:
                if g:
                    obj = NotificationGroup.objects.filter(id=g).first()
                    if obj:
                        g_obj_list.append(obj)
        
        return render(request,'anotification/notification-management.html',{'ulist':u_obj_list,'glist':g_obj_list,'context':context,})

    def post(self,request,*args, **kwargs):
        context={}
        nt_date=request.POST['nt_date']
        nt_desc=request.POST['nt_desc']
        gid_list=request.POST['gid_list']
        uid_list=request.POST['uid_list']
        gid_list=gid_list.split(',')
        uid_list=uid_list.split(',')
        context['nt_date']=nt_date
        context['nt_desc']=nt_desc
        context['gid_list'] = gid_list
        context['uid_list'] = uid_list

        ##############################################
        u_obj_list=[]
        g_obj_list=[]
        u_obj=SampleImageStore.objects.filter(unique_identification='un_ap_1').first()
        if u_obj:
            user_list=[u_obj.sample_data]
            if ',' in u_obj.sample_data:
                user_list=u_obj.sample_data.split(',')
            for u in user_list:
                if u:
                    obj = User.objects.filter(id=u).first()
                    if obj:
                        u_obj_list.append(obj)

            g_obj=SampleImageStore.objects.filter(unique_identification='un_ap_2').first()
            group_list=[g_obj.sample_data]
            if ',' in g_obj.sample_data:
                group_list=g_obj.sample_data.split(',')
            for g in group_list:
                if g:
                    obj = NotificationGroup.objects.filter(id=g).first()
                    if obj:
                        g_obj_list.append(obj)
        ######################################################################
        
        form = SendNotificationForm(data=request.POST or None)
        if form.is_valid():
            # SEND NOTIFICATION HERE NOW
            # save_notification()
            # send_firebase_notification()
            # send_email_notification() ---- not done as may b not required
            # send_sms() ---- not done as may b not required

            print('Hi====')
        
            for g in gid_list:
                if g:
                    ng = NotificationGroup.objects.filter(id=g).first()
                    ngu = ng.users.all()
                    for u in ngu:
                        un = UserNotification(
                            notification=nt_desc,
                            user=u,
                            req_type='3',
                            status='1',
                        )
                        un.save()

                        
                        if api_key!='':
                            print('inside push notification')
                            push_service= FCMNotification(api_key=api_key)
                            registration_id=u.device_token
                            message_title="KishMalik Admin Notification"
                            message_body=nt_desc
                            result=push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)

            for u in uid_list:
                if u:
                    uobj = User.objects.filter(id=u).first()
                    un = UserNotification(
                            notification=nt_desc,
                            user=uobj,
                            req_type='3',
                            status='1',
                        )
                    un.save()
                    
                    if api_key!='':
                        print('inside push notification')
                        push_service= FCMNotification(api_key=api_key)
                        registration_id=u.device_token
                        message_title="KishMalik Admin Notification"
                        message_body=nt_desc
                        result=push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)
            
            message='Notification sent successfully'
            messages.add_message(request, messages.INFO, message)
            return render(request,'anotification/notification-management.html',{'form':form,'ulist':u_obj_list,'glist':g_obj_list,'context':context})

        return render(request,'anotification/notification-management.html',{'form':form,'ulist':u_obj_list,'glist':g_obj_list,'context':context})

class AddRecipientView(TemplateView):
    def get(self,request,*args,**kwargs):
        users = User.objects.filter(is_active=True).exclude(is_superuser=True)
        groups = NotificationGroup.objects.all()
        return render(request,'anotification/add-recipient.html',{'users':users,'groups':groups})

    def post(self,request,*args,**kwargs):
        users = User.objects.filter(is_active=True).exclude(is_superuser=True)
        groups = NotificationGroup.objects.all()

        user_list = request.POST['c_user_list']
        group_list = request.POST['c_group_list']
        form = AddRecipient(data=request.POST or None)
        if form.is_valid():
            u_obj=SampleImageStore.objects.filter(unique_identification='un_ap_1').first()
            g_obj=SampleImageStore.objects.filter(unique_identification='un_ap_2').first()
            if u_obj:
                u_obj.sample_data=user_list
                u_obj.save()
            else:
                obj = SampleImageStore(
                    sample_data=user_list,
                    unique_identification='un_ap_1',
                )
                obj.save()
            if g_obj:
                g_obj.sample_data=group_list
                g_obj.save()
            else:
                obj = SampleImageStore(
                    sample_data=user_list,
                    unique_identification='un_ap_2',
                )
                obj.save()

            return HttpResponseRedirect(reverse('ap_notification:ap_nm_send_notification'))

        return render(request,'anotification/add-recipient.html',{'form':form,'users':users,'groups':groups})

class CreateGroupView(TemplateView):
    def post(self,request,*args,**kwargs):
        users = User.objects.filter(is_active=True)
        groups = NotificationGroup.objects.all()

        name=request.POST['name']
        max_users=request.POST['max_users']
        user_list=request.POST['user_list']
        form = CreateNotificationGroupForm(data = request.POST or None)
        message=''
        if form.is_valid():
            if ',' in user_list:
                user_list=user_list.split(',')
            else:
                user_list=[user_list]
            user_obj_list=[]
            for u in user_list:
                if u:
                    temp=User.objects.filter(id=u).first()
                    user_obj_list.append(temp)
            notobj=NotificationGroup(
                name=name,
                max_users=max_users,
            )
            notobj.save()
            for u in user_obj_list:
                notobj.users.add(u)

            groups = NotificationGroup.objects.all()
            
            message='Group created successfully'
            messages.add_message(request, messages.INFO, message)
            return HttpResponseRedirect(reverse('ap_notification:ap_nm_add_recipient'))

        return render(request,'anotification/add-recipient.html',{'form':form,'users':users,'groups':groups})

