from django import forms
from lessons.models import *

class LessionsAddEditForm(forms.Form):
    def clean(self):
        les_name = self.data['les_name']
        les_cat = self.data['les_cat']
        les_desc = self.data['les_desc']
        les_hint = self.data['les_hint']
        les_exp = self.data['les_exp']
        les_learn = self.data['les_learn']
        if not les_name or les_name=="":
            raise forms.ValidationError('Please provide lesson name')
        if not les_cat or les_cat=="":
            raise forms.ValidationError('Please choose lesson category')
        if les_cat:
            obj = LessonCategory.objects.filter(id=les_cat).first()
            if not obj:
                raise forms.ValidationError('Please choose valid lesson category')
        if not les_desc or les_desc=="":
            raise forms.ValidationError('Please provide lesson description')
        if not les_hint or les_hint=="":
            raise forms.ValidationError('Please provide lesson hint')
        if not les_exp or les_exp=="":
            raise forms.ValidationError('Please provide lesson explanation')
        if not les_learn or les_learn=="":
            raise forms.ValidationError('Please provide lesson learning text')
        
class LessionCategoriesAddForm(forms.Form):
    def clean(self):
        cr_name=self.data['cr_name']
        cr_list=self.data['cr_list']
        if not cr_name or cr_name=="":
            raise forms.ValidationError('Please provide category name')
        # if not cr_list or cr_list=="," or cr_list=="":
        #     raise forms.ValidationError('Please select lessons')
        lcr = LessonCategory.objects.filter(name=cr_name).first()
        if lcr:
            raise forms.ValidationError('This category name already exists')

class LessionCategoriesEditForm(forms.Form):
    # def __init__(self,*args, **kwargs):
    #     self.cr_id=kwargs.pop('cr_id',None)
    #     super(LessionCategoriesEditForm,self).__init__(*args,**kwargs)
    def clean(self):
        cr_id=self.data['cr_id']
        cr_name=self.data['cr_name']
        cr_list=self.data['cr_list']
        if not cr_name or cr_name=="":
            raise forms.ValidationError('Please provide category name')
        # if not cr_list or cr_list=="," or cr_list=="":
        #     raise forms.ValidationError('Please select lessons')
        lcobj = LessonCategory.objects.filter(id=cr_id).first()
        if lcobj.name!=cr_name:
            lcr = LessonCategory.objects.filter(name=cr_name).first()
            if lcr:
                raise forms.ValidationError('This category name already taken')
        