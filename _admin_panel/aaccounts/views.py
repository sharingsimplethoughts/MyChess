from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login ,logout
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy,reverse
from django.contrib.auth import views as auth_views

# from accounts.api.password_reset_form_api import MyPasswordResetForm
from accounts.api.password_reset_form import MyPasswordResetForm
from .forms import *
from game.models import SampleImageStore


class AdminHomeView(LoginRequiredMixin,TemplateView):
    login_url='ap_accounts:alogin'
    template_name='home/dashboard.html'

class AdminLoginView(TemplateView):
    def get(self, request, *args, **kwargs):
        form = LoginForm
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('ap_accounts:ahome'))
        return render(request, 'aaccounts/login.html', {'form':form})

    def post(self,request,*args,**kwargs):
        form = LoginForm(data=request.POST or None)
        em=request.POST['email']
        print(em)
        if form.is_valid():
            em=request.POST['email']
            user_qs= User.objects.get(email=em, is_active=True, is_staff=True, is_superuser=True)
            if not request.POST.getlist('rememberChkBox'):
                request.session.set_expiry(0)
            login(request,user_qs,backend='django.contrib.auth.backends.ModelBackend')
            response = HttpResponseRedirect(reverse('ap_accounts:ahome'))
            # response.set_cookie['role_admin']
            response.set_cookie(key='id', value=1)
            return response

        return render(request,'aaccounts/login.html', {'form':form})

class AdminLogoutView(LoginRequiredMixin, TemplateView):
    login_url='ap_accounts:alogin'
    def get(self, request):
        logout(request)
        response = HttpResponseRedirect(reverse('ap_accounts:ahome'))
        response.delete_cookie(key='id')
        return response

class ResetPasswordView(auth_views.PasswordResetView):
    form_class = MyPasswordResetForm

class AdminProfileView(LoginRequiredMixin, TemplateView):
    login_url='ap_accounts:alogin'
    def get(self, request):
        return render(request,'aaccounts/profile.html',)

class AdminProfileEditView(LoginRequiredMixin, TemplateView):
    login_url='ap_accounts:alogin'
    def get(self, request):
        user=request.user
        if user.profile_image:
            context = {
                'name':user.name,
                'email':user.email,
                'mobile':user.mobile,
                'profile_image':user.profile_image.url,
                'country':user.country,
                'about':user.about,
            }
        else:
            context = {
                'name':user.name,
                'email':user.email,
                'mobile':user.mobile,
                'profile_image':'',
                'country':user.country,
                'about':user.about,
            }
        return render(request,'aaccounts/edit-profile.html',{'context':context})
    def post(self,request,*args,**kwargs):
        user=request.user
        form=AdminProfileEditForm(data=request.POST or None, user=request.user)
        name=request.POST['name']
        email=request.POST['email']
        mobile=request.POST['mobile']
        profile_image=request.FILES.get('profileimg')
        country=request.POST['country']
        about=request.POST['about']

        if profile_image:
            print('inside sample image save')
            sampObj = SampleImageStore.objects.filter(unique_identification='ad_profile').first()
            if sampObj:
                sampObj.sample_image=profile_image,
                sampObj.unique_identification='ad_profile'
                sampObj.save()
            else:
                print('1-----------')
                sampObj = SampleImageStore(
                    sample_image=profile_image,
                    unique_identification='ad_profile'
                )
                sampObj.save()
            profile_image=sampObj.sample_image.url
        else:
            sampObj = SampleImageStore.objects.filter(unique_identification='ad_profile').first()
            if sampObj:
                profile_image=sampObj.sample_image.url
            else:
                profile_image=user.profile_image.url

        if form.is_valid():
            print('inside post valid form')
            
            first_name=''
            last_name=''
            if ' ' in name:
                first_name = name.split(' ')[0]
                last_name = name.split(' ')[1]
            else:
                first_name = name
            # countryobj = CountryCode.objects.filter(country_iexact = country).first()

            user.email=email
            user.name=name
            user.first_name=first_name
            user.last_name=last_name
            user.mobile=mobile
            user.country=country
            user.about=about
            user.save()
            if profile_image:
                if '/media' in profile_image:
                    profile_image = profile_image.split('/media')[1]

                user.profile_image=profile_image
                user.save()
                
                sampObj = SampleImageStore.objects.filter(unique_identification='ad_profile').first()
                if sampObj:
                    print('2------------')
                    sampObj.delete()

            return HttpResponseRedirect(reverse('ap_accounts:aprofile'))

        

        context = {
            'name':name,
            'email':email,
            'mobile':mobile,
            'profile_image':profile_image,
            'country':country,
            'about':about,
        }
        print(form.errors)
        return render(request,'aaccounts/edit-profile.html',{'form':form,'context':context})

class ChangePasswordView(LoginRequiredMixin, TemplateView):
    login_url='ap_accounts:alogin'
    def get(self, request):
        form = ChangePasswordForm(user=request.user)
        return render(request,'aaccounts/change-password.html',{'form':form})
    def post(self,request,*args,**kwargs):
        user = request.user
        form = ChangePasswordForm(request.POST or None, user=request.user)

        if form.is_valid():
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            return HttpResponseRedirect(reverse('ap_accounts:alogin'))
        return render(request, 'aaccounts/change-password.html',{'form': form}) 