from django.shortcuts import render
from django.views.generic import TemplateView
from django.views import View
import datetime
import pytz
from django.db.models import Q

from extra.models import *
from .forms import *


class SettingsManagementListView(TemplateView):
    def get(self,request,*args,**kwargs):
        return render(request,'asettings/settings_list.html')

class SettingsManagementEditView(View):
    def get(self,request,*args,**kwargs):
        id=self.kwargs['id']
        context=''
        if id=='f1':
            context=AboutUs.objects.all().first()
        elif id=='f2':
            context=TermsAndCondition.objects.all().first()
        elif id=='f3':
            context=Faq.objects.all().first()
        elif id=='f4':
            context=Help.objects.all().first()
        elif id=='f5':
            context=PrivacyPolicy.objects.all().first()
        elif id=='f6':
            context=Legal.objects.all().first()
        
        return render(request,'asettings/edit/settings_common_edit.html',{'context':context,'id':id})
    def post(self,request,*args,**kwargs):
        id=self.kwargs['id']
        form=SettingsManagementEditForm(request.POST or None)
        obj=''
        succ_messages=''
        if id=='f1':
            obj=AboutUs.objects.all().first()
        elif id=='f2':
            obj=TermsAndCondition.objects.all().first()
        elif id=='f3':
            obj=Faq.objects.all().first()
        elif id=='f4':
            obj=Help.objects.all().first()
        elif id=='f5':
            obj=PrivacyPolicy.objects.all().first()
        elif id=='f6':
            obj=Legal.objects.all().first()
        
        if form.is_valid():
            if id=='f1':
                obj.content=form.cleaned_data['servicedesc']
                # obj.content_ar=form.cleaned_data['servicedesc_ar']
                obj.save()
                obj=AboutUs.objects.all().first()
            elif id=='f2':
                obj.content=form.cleaned_data['servicedesc']
                # obj.content_ar=form.cleaned_data['servicedesc_ar']                
                obj.save()
                obj=TermsAndCondition.objects.all().first()
            elif id=='f3':
                obj.content=form.cleaned_data['servicedesc']
                # obj.content_ar=form.cleaned_data['servicedesc_ar']
                obj.save()
                obj=Faq.objects.all().first()
            elif id=='f4':
                obj.content=form.cleaned_data['servicedesc']
                # obj.content_ar=form.cleaned_data['servicedesc_ar']
                obj.save()
                obj=Help.objects.all().first()
            elif id=='f5':
                obj.content=form.cleaned_data['servicedesc']
                # obj.content_ar=form.cleaned_data['servicedesc_ar']
                obj.save()
                obj=PrivacyPolicy.objects.all().first()
            elif id=='f6':
                obj.content=form.cleaned_data['servicedesc']
                # obj.content_ar=form.cleaned_data['servicedesc_ar']
                obj.save()
                obj=Legal.objects.all().first()
            
            succ_messages='Settings edited successfully'

        return render(request,'asettings/edit/settings_common_edit.html',{'context':obj,'id':id,'succ_messages':succ_messages,'form':form})

class SettingsManagementFaqEditView(TemplateView):
    def get(self,request,*args,**kwargs):
        faqs=Faq.objects.all()
        return render(request,'asettings/edit/faq.html',{'faqs':faqs})
    def post(self,request,*args,**kwargs):
        title=request.POST['title']
        content=request.POST['content']
        # title_ar=request.POST['title_ar']
        # content_ar=request.POST['content_ar']
        f = Faq(
            title=title,
            content=content,
            # title_ar=title_ar,
            # content_ar=content_ar,
        )
        f.save()
        faqs=Faq.objects.all()
        return render(request,'asettings/edit/faq.html',{'faqs':faqs})

class SettingsManagementFaqView(TemplateView):
    def get(self, request, *args,**kwargs):
        faqs=Faq.objects.all()
        return render(request,'asettings/view/faq.html',{'faqs':faqs})
class SettingsManagementAboutUsView(TemplateView):
    def get(self,request,*args,**kwargs):
        aboutus=AboutUs.objects.all().first()
        return render(request,'asettings/view/about-us.html',{'aboutus':aboutus})
class SettingsManagementPrivacyPolicyView(TemplateView):
    def get(self,request,*args,**kwargs):
        ppolicy=PrivacyPolicy.objects.all().first()
        return render(request,'asettings/view/privacy-policy.html',{'ppolicy':ppolicy})
class SettingsManagementTermsAndConditionView(TemplateView):
    def get(self,request,*args,**kwargs):
        tacond=TermsAndCondition.objects.all().first()
        return render(request,'asettings/view/terms-conditions.html',{'tacond':tacond})
class SettingsManagementHelpView(TemplateView):
    def get(self,request,*args,**kwargs):
        helps=Help.objects.all().first()
        return render(request,'asettings/view/help.html',{'helps':helps})
class SettingsManagementLegalView(TemplateView):
    def get(self,request,*args,**kwargs):
        legal=Legal.objects.all().first()
        return render(request,'asettings/view/legal.html',{'legal':legal})

# class SettingsManagementFaq_ArView(TemplateView):
#     def get(self, request, *args,**kwargs):
#         faqs=Faq.objects.all()
#         return render(request,'asettings/view_ar/faq.html',{'faqs':faqs})
# class SettingsManagementAboutUs_ArView(TemplateView):
#     def get(self,request,*args,**kwargs):
#         aboutus=AboutUs.objects.all().first()
#         return render(request,'asettings/view_ar/about-us.html',{'aboutus':aboutus})
# class SettingsManagementPrivacyPolicy_ArView(TemplateView):
#     def get(self,request,*args,**kwargs):
#         ppolicy=PrivacyPolicy.objects.all().first()
#         return render(request,'asettings/view_ar/privacy-policy.html',{'ppolicy':ppolicy})
# class SettingsManagementTermsAndCondition_ArView(TemplateView):
#     def get(self,request,*args,**kwargs):
#         tacond=TermsAndCondition.objects.all().first()
#         return render(request,'asettings/view_ar/terms-conditions.html',{'tacond':tacond})
# class SettingsManagementHelp_ArView(TemplateView):
#     def get(self,request,*args,**kwargs):
#         helps=Help.objects.all().first()
#         return render(request,'asettings/view_ar/help.html',{'helps':helps})
# class SettingsManagementLegal_ArView(TemplateView):
#     def get(self,request,*args,**kwargs):
#         legal=Legal.objects.all().first()
#         return render(request,'asettings/view_ar/legal.html',{'legal':legal})