from django import forms
from django.contrib.auth.models import User
import string
import datetime
import re
from achievement.models import *

# class AddAchievementForm(forms.Form):
#     def clean(self):
#         name=self.data['name']
#         unlock_task=self.data['unlock_task']

#         if n