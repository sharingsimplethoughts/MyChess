from django import forms
from django.contrib.auth.models import User

from usubscription.models import *
from accounts.models import *


class AddSubscriptionForm(forms.Form):
    def clean(self):
        name=self.data['name']
        # duration_m=self.data['duration_m']
        # duration_y=self.data['duration_y']
        price_m=self.data['price_m']
        price_y=self.data['price_y']
        benefits=self.data['benefits']
        if not name or name=="":
            raise forms.ValidationError('Please provide name')
        # if not duration_m or duration_m=="":
        #     raise forms.ValidationError('Please provide (monthly) duration')
        # if not duration_y or duration_y=="":
        #     raise forms.ValidationError('Please provide (yearly) duration')
        if not price_m or price_m=="":
            raise forms.ValidationError('Please provide (monthly) price')
        if not price_y or price_y=="":
            raise forms.ValidationError('Please provide (yearly) price')
        if not benefits or benefits=="":
            raise forms.ValidationError('Please provide benefits')

        p1 = price_m.split('.')
        if len(p1)>2:
            raise forms.ValidationError('Price(monthly) is invalid')
        if not p1[0].isdigit():
            raise forms.ValidationError('Price(monthly) is invalid')
        if len(p1)==2 and (not p1[1].isdigit()):
            raise forms.ValidationError('Price(monthly) is invalid')

        p2 = price_y.split('.')
        if len(p2)>2:
            raise forms.ValidationError('Price(yearly) is invalid')
        if not p2[0].isdigit():
            raise forms.ValidationError('Price(yearly) is invalid')
        if len(p2)==2 and (not p2[1].isdigit()):
            raise forms.ValidationError('Price(yearly) is invalid')

        # if duration_m not in ['1','2','3','4','5','6','7','8','9','10','11']:
        #     raise forms.ValidationError('Duration(monthly) is not valid')
        # if duration_y not in ['1','2','3','4','5']:
        #     raise forms.ValidationError('Duration(yearly) is not valid')
        
        

