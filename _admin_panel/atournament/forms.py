from django import forms
from django.contrib.auth.models import User
import string
import datetime
import re
from articles.models import *
from accounts.models import *
from tournament.models import *

class CreateTournamentForm(forms.Form):
    def clean(self):
        tname = self.data['tname']
        tstart_date = self.data['tstart_date']
        tend_date = self.data['tend_date']
        # tduration = self.data['tduration']
        tlimit = self.data['tlimit']
        thh = self.data['thh']
        tmm = self.data['tmm']
        trounds = self.data['trounds']
        ttrating = self.data['trating']

        if not tname or tname=="":
            raise forms.ValidationError('Please provide tournament name')
        if not tstart_date or tstart_date=="":
            raise forms.ValidationError('Please provide tournament start date')
        if not tend_date or tend_date=="":
            raise forms.ValidationError('Please provide tournament end date')
        # if not tduration or tduration=="":
        #     raise forms.ValidationError('Please provide tournament duration')
        

        if not thh or thh=="":
            raise forms.ValidationError('Please provide tournament start time')
        if not tmm or tmm=="":
            raise forms.ValidationError('Please provide tournament start time')
        if not trounds or trounds=="":
            raise forms.ValidationError('Please provide tournament rounds')
        if not tlimit or tlimit=="":
            raise forms.ValidationError('Please provide each game time limit in tournament')
        if not ttrating or ttrating=="":
            raise forms.ValidationError('Please provide tournament rating')

        # str1=tduration
        # alpha = ""
        # num = ""
        # special = ""
        # for i in range(len(str1)):
        #     if (str1[i].isdigit()):
        #         num = num+ str1[i]
        #     elif((str1[i] >= 'A' and str1[i] <= 'Z') or
        #         (str1[i] >= 'a' and str1[i] <= 'z')):
        #         alpha += str1[i]
        #     else:
        #         special += str1[i] 
        # if alpha or special:
        #     raise forms.ValidationError('Please provide valid duration')
        # if not num:
        #     raise forms.ValidationError('Please provide valid duration')
        # if int(tduration)>365:
        #     raise forms.ValidationError('Please provide valid duration')
        
        str1=tlimit
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
        if alpha or special:
            raise forms.ValidationError('Please provide valid game time limit')
        if not num:
            raise forms.ValidationError('Please provide valid game time limit')
        if int(tlimit)>30:
            raise forms.ValidationError('Please provide valid game time limit')

        print(tstart_date)
        print(tend_date)
        tstart_date=tstart_date.split('/')
        tend_date=tend_date.split('/')

        tstart_date = datetime.date(int(tstart_date[2]),int(tstart_date[0]),int(tstart_date[1]))
        tend_date = datetime.date(int(tend_date[2]),int(tend_date[0]),int(tend_date[1]))
        # tend_date = datetime.date()
        if tstart_date<datetime.date.today():
            raise forms.ValidationError('Start and End date is not valid')
        if tend_date<tstart_date:
            raise forms.ValidationError('Start and End date is not valid')

        thh=int(thh)
        tmm=int(tmm)
        if thh==0 and tmm==0:
            raise forms.ValidationError('Please provide valid tournament start time')
        # if thh==2 and tmm!=0:
        #     raise forms.ValidationError('Please provide valid tournament start time')


