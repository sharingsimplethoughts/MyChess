from django import forms
from puzzles.models import *

class PuzzlesAddEditForm(forms.Form):
    def clean(self):
        les_name = self.data['les_name']
        les_cat = self.data['les_cat']
        les_desc = self.data['les_desc']
        les_hint = self.data['les_hint']
        les_exp = self.data['les_exp']
        les_learn = self.data['les_learn']
        if not les_name or les_name=="":
            raise forms.ValidationError('Please provide puzzle name')
        if not les_cat or les_cat=="":
            raise forms.ValidationError('Please choose puzzle category')
        if les_cat:
            obj = PuzzleCategory.objects.filter(id=les_cat).first()
            if not obj:
                raise forms.ValidationError('Please choose valid puzzle category')
        if not les_desc or les_desc=="":
            raise forms.ValidationError('Please provide puzzle description')
        if not les_hint or les_hint=="":
            raise forms.ValidationError('Please provide puzzle hint')
        if not les_exp or les_exp=="":
            raise forms.ValidationError('Please provide puzzle explanation')
        if not les_learn or les_learn=="":
            raise forms.ValidationError('Please provide puzzle learning text')
        
class PuzzleCategoriesAddForm(forms.Form):
    def clean(self):
        cr_name=self.data['cr_name']
        cr_list=self.data['cr_list']
        if not cr_name or cr_name=="":
            raise forms.ValidationError('Please provide category name')
        # if not cr_list or cr_list=="," or cr_list=="":
        #     raise forms.ValidationError('Please select puzzles')
        lcr = PuzzleCategory.objects.filter(name=cr_name).first()
        if lcr:
            raise forms.ValidationError('This category name already exists')

class PuzzleCategoriesEditForm(forms.Form):
    # def __init__(self,*args, **kwargs):
    #     self.cr_id=kwargs.pop('cr_id',None)
    #     super(PuzzleCategoriesEditForm,self).__init__(*args,**kwargs)
    def clean(self):
        cr_id=self.data['cr_id']
        cr_name=self.data['cr_name']
        cr_list=self.data['cr_list']
        if not cr_name or cr_name=="":
            raise forms.ValidationError('Please provide category name')
        # if not cr_list or cr_list=="," or cr_list=="":
        #     raise forms.ValidationError('Please select puzzles')
        lcobj = PuzzleCategory.objects.filter(id=cr_id).first()
        if lcobj.name!=cr_name:
            lcr = PuzzleCategory.objects.filter(name=cr_name).first()
            if lcr:
                raise forms.ValidationError('This category name already taken')
        