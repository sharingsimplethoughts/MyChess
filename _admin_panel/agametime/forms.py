from django import forms
from game.models import *

class AddOrEditGameTimeForm(forms.Form):
    def clean(self):
        newdur = self.data['newdur']
        if not newdur or newdur=="":
            raise forms.ValidationError('Please provide game duration')
        if newdur:
            obj = GameDuration.objects.filter(duration=newdur).first()
            if obj:
                raise forms.ValidationError('That duration is already exists')
            