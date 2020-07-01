from django import forms
from accounts.models import *


class CreateNotificationGroupForm(forms.Form):
    def clean(self):
        name = self.data['name']
        max_users = self.data['max_users']
        user_list = self.data['user_list']

        if not user_list or user_list=="" or user_list==",":
            raise forms.ValidationError('Please select users first')
        notobj=NotificationGroup.objects.filter(name=name).first()
        if notobj:
            raise forms.ValidationError('This group name already exists')

        if ',' in user_list and len(user_list)>1:
            user_list=user_list.split(',')
        else:
            user_list=[user_list]
        user_obj_list=[]
        ulist_len=0
        for u in user_list:
            if u:
                ulist_len+=1
                temp=User.objects.filter(id=u).first()
                if not temp:
                    raise forms.ValidationError(str(u)+'-this user is not valid')
                user_obj_list.append(temp)
        if ulist_len>int(max_users):
            raise forms.ValidationError('Number of selected user is greate than the max_users limit of the group')

class AddRecipient(forms.Form):
    def clean(self):
        c_user_list = self.data['c_user_list']
        c_group_list = self.data['c_group_list']

        if (not c_user_list or c_user_list=='' or c_user_list==',') and (not c_group_list or c_group_list=='' or c_group_list==','):
            raise forms.ValidationError('Please select user or group first')
    
class SendNotificationForm(forms.Form):
    def clean(self):
        nt_date = self.data['nt_date']
        nt_desc = self.data['nt_desc']
        gid_list = self.data['gid_list']
        uid_list = self.data['uid_list']

        if not nt_date or nt_date=="":
            raise forms.ValidationError('Please provide schedule date')
        if not nt_desc or nt_desc=="":
            raise forms.ValidationError('Please write the notification first')
        if (not gid_list or gid_list=="" or gid_list==",") and (not uid_list or uid_list=="" or uid_list==","):
            raise forms.ValidationError('Please select a user or group first')

        