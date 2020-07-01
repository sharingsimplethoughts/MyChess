from django import forms
from django.contrib.auth.models import User

from accounts.models import *


class LoginForm(forms.Form):
    # em=forms.CharField(max_length=100)
    # password=forms.CharField(max_length=100)
    def clean(self):
        em=self.data['email']
        password=self.data['password']

        if not em or em=='':
            raise forms.ValidationError('Please provide email id first')
        if '@' not in em:
            raise forms.ValidationError('Please provide valid email id')
        emm=em.split('@')
        if not emm[0] or emm[0]=='':
            raise forms.ValidationError('Please provide valid email id')
        if '.' not in emm[1]:
            raise forms.ValidationError('Please provide valid email id')
        emmm=emm[1].split('.')
        if not emmm[0] or emmm[0]=='':
            raise forms.ValidationError('Please provide valid email id')
        if not emm[1] or emmm[1]=='':
            raise forms.ValidationError('Please provide valid email id')
        if not password or password=='':
            raise forms.ValidationError('Please provide password first')
        if len(password)<8:
            raise forms.ValidationError('Password must be of length 8 or more')

        user_qs = User.objects.filter(email=em)
        usertemp = user_qs.exclude(email__isnull=True).exclude(email__iexact='').distinct()
        if usertemp.exists() and usertemp.count()==1:
            userObj=usertemp.first()
        else:
            raise forms.ValidationError('This email id does not exists')

        checked_pass = userObj.check_password(password)
        if checked_pass:
            if not userObj.is_superuser or not userObj.is_active:
                raise forms.ValidationError('You are not authorised to access this panel')
        else:
            raise forms.ValidationError('Authentication failed')

        return self.data

class ChangePasswordForm(forms.Form):
    oldpassword 	= forms.CharField()
    password 		= forms.CharField()
    confpassword 	= forms.CharField()

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user',None)
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        self.fields['oldpassword'].strip = False
        self.fields['password'].strip = False
        self.fields['confpassword'].strip = False

    def clean(self):
        oldpassword = self.cleaned_data.get('oldpassword')
        password = self.cleaned_data.get('password')
        confpassword =self.cleaned_data.get('confpassword')

        if not oldpassword or oldpassword=="":
            raise forms.ValidationError('Please provide old password')
        if not password or password=="":
            raise forms.ValidationError('Please provide new password')
        if not confpassword or confpassword=="":
            raise forms.ValidationError('Please provide confirm password')

        if not len(password) >= 8 or not len(confpassword) >= 8:
            raise forms.ValidationError('Password must have at least 8 characters')
        if not self.user.check_password(oldpassword):
            raise forms.ValidationError('Incorrect old password')
        if password!=confpassword:
            raise forms.ValidationError('Both password fields should be same')
        return self.cleaned_data
        
class AdminProfileEditForm(forms.Form):
    name = forms.CharField(max_length=50)
    email = forms.EmailField()
    mobile = forms.CharField(max_length=15)
    country = forms.CharField(max_length=50)
    about = forms.CharField(max_length=500)


    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user','None')
        super(AdminProfileEditForm,self).__init__(*args,**kwargs)

    def clean(self):
        name = self.cleaned_data.get('name')
        str1=name
        alpha = ""
        num = ""
        special = ""
        for i in range(len(str1)):
            if (str1[i].isdigit()):
                num = num+ str1[i]
            elif((str1[i] >= 'A' and str1[i] <= 'Z') or
                (str1[i] >= 'a' and str1[i] <= 'z')):
                alpha += str1[i]
            else:
                special += str1[i]
        if special:
            raise forms.ValidationError('Please provide valid name')
        if num:
            raise forms.ValidationError('Please provide valid name')

        email = self.cleaned_data.get('email')

        if not self.user.email==email:
            if email.count('@')>1:
                raise forms.ValidationError('Please provide a valid email')
            try:
                domain=email.split('@')[1]
            except:
                raise forms.ValidationError('Please provide a valid email')
            user_qs=User.objects.filter(email__iexact=email)
            if user_qs.exists():
                raise forms.ValidationError('This email already exists')

        mob=self.cleaned_data.get('mobile')
        str1=mob
        alpha = ""
        num = ""
        special = ""
        for i in range(len(str1)):
            if (str1[i].isdigit()):
                num = num+ str1[i]
            elif((str1[i] >= 'A' and str1[i] <= 'Z') or
                (str1[i] >= 'a' and str1[i] <= 'z')):
                alpha += str1[i]
            else:
                special += str1[i] 
        if special:
            raise forms.ValidationError('Please provide valid mobile number')
        if alpha:
            raise forms.ValidationError('Please provide valid mobile number')

        if not mob==self.user.mobile:
            if mob.isdigit() and len(mob)<10:
                raise forms.ValidationError('This mobile number is not valid')
            user_qs=User.objects.filter(mobile__iexact=mob)
            if user_qs.exists():
                raise forms.ValidationError('This mobile number already exists')

        country=self.cleaned_data.get('country')
        if not country or country=="":
            raise forms.ValidationError('Please provide country')
        countryobj = CountryCode.objects.filter(country__iexact = country).first()
        if not countryobj:
            raise forms.ValidationError('This country is not valid')

        return self.cleaned_data