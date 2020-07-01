from django import forms
from django.contrib.auth.models import User
import string
import datetime
import re
from articles.models import *
from accounts.models import *

class CreateOrEditVideoCategoryForm(forms.Form):
    def clean(self):
        catName = self.data['catName']
        catDesc = self.data['catDesc']
        # finalVidIds = self.data['finalVidIds']

        if not catName or catName=="":
            raise forms.ValidationError('Please provide category name')
        if not catDesc or catDesc=="":
            raise forms.ValidationError('Please provide category description')
        # if finalVidIds:
        #     finalVidIds=finalVidIds.split(',')
        #     raise forms.ValidationError('Please add videos')


class CreateOrEditVideoForm(forms.Form):    
    def clean(self):
        vidName = self.data['vidName']   
        vidCat = self.data['status']
        vidAuthName = self.data['vidAuthName']
        vidAuthCountry = self.data['vidAuthCountry']        
        vidDesc = self.data['vidDesc']

        if not vidName or vidName=="":
            raise forms.ValidationError('Please provide video name')
        if not vidCat or vidCat=="":
            raise forms.ValidationError('Please provide video category')
        if not vidAuthName or vidAuthName=="":
            raise forms.ValidationError("Please provide author's name")
        if not vidAuthCountry or vidAuthCountry=="":
            raise forms.ValidationError("Please provide author's country name")
        if not vidDesc or vidDesc=="":
            raise forms.ValidationError('Please provide video description')
        
        country = CountryCode.objects.filter(country__iexact=vidAuthCountry)
        if not country:
            raise forms.ValidationError("Author's Country is not valid")
        pattern = re.compile("[A-Za-z ]+")
        if pattern.fullmatch(vidAuthName) is None:
            raise forms.ValidationError("Author's name is not valid")
        