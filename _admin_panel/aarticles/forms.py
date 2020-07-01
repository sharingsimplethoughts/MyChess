from django import forms
from django.contrib.auth.models import User
import string
import datetime
import re
from articles.models import *
from accounts.models import *

class CreateOrEditArticleForm(forms.Form):
    def clean(self):
        artName = self.data['artName']
        artDate = self.data['artDate']
        artAuthName = self.data['artAuthName']
        artAuthCountry = self.data['artAuthCountry']        
        artDesc = self.data['artDesc']

        if not artName or artName=="":
            raise forms.ValidationError('Please provide article name')
        if not artDate or artDate=="":
            raise forms.ValidationError('Please provide posted on date')
        if not artAuthName or artAuthName=="":
            raise forms.ValidationError("Please provide author's name")
        if not artAuthCountry or artAuthCountry=="":
            raise forms.ValidationError("Please provide author's country name")
        if not artDesc or artDesc=="":
            raise forms.ValidationError('Please provide article description')
        if '-' in artDate:
            if len(artDate.split('-'))==3:
                try:
                    x = datetime.datetime.strptime(artDate, '%Y-%m-%d')
                    y = datetime.datetime.now().date()
                    if y<x.date():
                        raise forms.ValidationError("Date can not be greater than today")    
                except ValueError:
                    raise forms.ValidationError("Incorrect data format, should be YYYY-MM-DD")
            else:
                raise froms.ValidationError('Date is not in proper format')
        else:
            raise forms.ValidationError('Date is not in proper format')
        country = CountryCode.objects.filter(country__iexact=artAuthCountry)
        if not country:
            raise forms.ValidationError("Author's Country is not valid")
        pattern = re.compile("[A-Za-z ]+")        
        if pattern.fullmatch(artAuthName) is None:
            raise forms.ValidationError("Author's name is not valid")