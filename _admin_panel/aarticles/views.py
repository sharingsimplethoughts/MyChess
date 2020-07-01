from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login ,logout
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy,reverse
from django.contrib import messages
import datetime
from django.contrib.sites.shortcuts import get_current_site
import pytz
import openpyxl
import cv2
import re
from django.db.models import Q
from .forms import *
from django.contrib.auth import views as auth_views
from articles.models import *
# Create your views here.
class ArticleView(TemplateView):
    def get(self,request,*args,**kwargs):                
        articles = Article.objects.all().order_by('-created_on')
        return render(request,'aarticles/articles.html',{'articles':articles,})  

class DateWiseArticleView(TemplateView):
    def get(self, request, *args, **kwargs):        
        w1=request.GET.get('startdate')
        w2=request.GET.get('enddate')        

        if not w2:
            msg="End date is not valid"
            articles  = Article.objects.all()
            return render(request,'aarticles/articles.html',{'articles':articles,'msg':msg}) 
        
        # articles = Article.objects.all().order_by('-created_on')
        # if w1 and w2:
        w1=w1.split('/')
        w2=w2.split('/')
        
        # start_date = datetime.datetime.strptime(startdate, '%m/%d/%Y').strftime('%Y-%m-%d')
        # end_date = datetime.datetime.strptime(enddate, '%m/%d/%Y').strftime('%Y-%m-%d')
        if len(w1)==3:
            start_date = datetime.datetime(int(w1[2]), int(w1[0]), int(w1[1]), 0, 0, 0, 0, pytz.timezone('Asia/Dubai'))
        if len(w2)==3:
            end_date = datetime.datetime(int(w2[2]), int(w2[0]), int(w2[1]), 23, 59, 59, 999999, pytz.timezone('Asia/Dubai'))

        print(start_date)
        print(end_date)
        articles  = Article.objects.filter(Q(actually_created_on__range=(start_date,end_date))).order_by('-actually_created_on')
        return render(request,'aarticles/articles.html',{'articles':articles,})        
        
class AddArticleView(TemplateView):
    def get(self,request,*args,**kwargs):
        return render(request,'aarticles/article-add.html')
    def post(self, request, *args, **kwargs):
        form = CreateOrEditArticleForm(data=request.POST or None,)
        artName = request.POST['artName']
        artDate = request.POST['artDate']
        artAuthName = request.POST['artAuthName']
        artAuthCountry = request.POST['artAuthCountry']
        artFile = request.FILES.get('artFile')
        artAuthImage = request.FILES.get('artAuthImage')
        artDesc = request.POST['artDesc']
        x=0
        message=''
        if form.is_valid():
            if artFile:
                if artFile.size>10485760:
                    x=1
                    message="Video file size is not valid"
                if artFile.name.split('.')[-1].lower() not in ('mp4','avi','flv','wmv','mov'):
                    x=1
                    message="Video file extension is not valid"
            else:
                message="Please upload video file"
            if artAuthImage:
                if artAuthImage.size>5242880:
                    x=1
                    message="Author's image size is not valid"
                if artAuthImage.name.split('.')[-1].lower() not in ('jpg','jpeg','png'):
                    x=1
                    message="Author's image extension is not valid"

            if x==0 and artFile:                
            # try:
                artObj = Article(
                    article_file = artFile,
                    title = artName,
                    description = artDesc,
                    created_on = artDate,
                    author = artAuthName,
                    author_country = artAuthCountry,
                    author_profile_photo = artAuthImage,
                )
                artObj.save()

                if artObj.article_file:
                    artObj.article_file_url=artObj.article_file.url
                if artObj.author_profile_photo:
                    artObj.author_profile_photo_url=artObj.author_profile_photo.url
                artObj.save()

                ## Generate Preview
                if artObj.article_file:
                    url=artObj.article_file.url            
                    extension = url.split('.')[-1]
                    print(extension)
                    video_extensions = ['mp4','avi','flv','wmv','mov']                
                    if extension.lower() in video_extensions:
                        print('1')
                        cam = cv2.VideoCapture(artObj.article_file.path)
                        print(cam)
                        print(artObj.article_file.path)
                        print(cam.isOpened())
                        if cam.isOpened():
                            print('2')
                            ret,frame = cam.read()
                            print(frame)
                            name = "media_cdn/articles/preview/output"+str(artObj.id)+".jpg"
                            cv2.imwrite(name, frame)
                            # instance.preview_image='articles/preview/7.jpg'
                            artObj.preview_image_url="/media/articles/preview/output"+str(artObj.id)+".jpg"
                            artObj.is_video=True
                            artObj.save()
                    else:
                        artObj.preview_image=artObj.article_file
                        artObj.save()
                        artObj.preview_image_url=artObj.preview_image.url
                        artObj.save()

                        # current_site = get_current_site(request)            
                        # artObj.preview_image='http://'+str(current_site.domain)+artObj.article_file.url
                        # artObj.save()
                    # except:
                        # return render(request,'aarticles/article-add.html',)

                    send_notification_to_all()


                    message='Article updated successfully'
                    messages.add_message(request, messages.INFO, message)
                    return render(request,'aarticles/article-add.html',)
                    # else:
                    #     message='upload video and image file'
                    #     messages.add_message(request, messages.INFO, message)
                    #     return render(request,'aarticles/article-add.html',)
                # else:
                #     message='upload video and image file'

        context = {
            'artName':artName,
            'artDate':artDate,
            'artAuthName':artAuthName,
            'artAuthCountry':artAuthCountry,
            'artFile':artFile,
            'artDesc':artDesc,
            'artAuthImage':artAuthImage,
        }
        messages.add_message(request, messages.INFO, message)
        return render(request,'aarticles/article-add.html',{'form':form,'context':context})

class ViewArticleView(TemplateView):
    def get(self,request,*args,**kwargs):
        id = self.kwargs['pk']
        article = Article.objects.filter(id=id).first()
        return render(request,'aarticles/article-view.html',{'article':article})

class EditArticleView(TemplateView):
    def get(self,request,*args,**kwargs):
        id = self.kwargs['pk']
        article = Article.objects.filter(id=id).first()        
        context = {
            'id':article.id,
            'artName':article.title,
            'artDate':article.created_on,
            'artAuthName':article.author,
            'artAuthCountry':article.author_country,
            'artFile':article.article_file,
            'artFilePreview':article.preview_image,
            'artAuthImage':article.author_profile_photo,
            'artDesc':article.description,
            'artFileUrl':article.article_file_url,
            'artFilePreviewUrl':article.preview_image_url,
            'artAuthImageUrl':article.author_profile_photo_url,
        }
        return render(request,'aarticles/article-edit.html',{'context':context})

    def post(self, request, *args, **kwargs):
        form = CreateOrEditArticleForm(data=request.POST or None,)
        id = self.kwargs['pk']
        article = Article.objects.filter(id=id).first()
        artName = request.POST['artName']
        artDate = request.POST['artDate']
        artAuthName = request.POST['artAuthName']
        artAuthCountry = request.POST['artAuthCountry']
        artFile = request.FILES.get('artFile')
        artAuthImage = request.FILES.get('artAuthImage')
        artDesc = request.POST['artDesc']
        x=0
        message=''
        if form.is_valid():
            if artFile:
                if artFile.size>10485760:
                    x=1
                    message="Video file size is not valid"
                if artFile.name.split('.')[-1].lower() not in ('mp4','avi','flv','wmv','mov'):
                    x=1
                    message="Video file extension is not valid"
            if artAuthImage:
                if artAuthImage.size>5242880:
                    x=1
                    message="Author's image size is not valid"
                if artAuthImage.name.split('.')[-1].lower() not in ('jpg','jpeg','png'):
                    x=1
                    message="Author's image extension is not valid"
            if x==0:
                if artFile:
                    article.article_file = artFile
                article.title = artName
                article.description = artDesc
                article.created_on = artDate
                article.author = artAuthName
                article.author_country = artAuthCountry  
                if artAuthImage:
                    article.author_profile_photo = artAuthImage          
                # try:
                article.save()
                if article.article_file:
                    article.article_file_url=article.article_file.url
                if article.author_profile_photo:
                    article.author_profile_photo_url=article.author_profile_photo.url
                article.save()

                ##Generate Preview
                if artFile:
                    url=article.article_file.url
                    extension = url.split('.')[-1]
                    video_extensions = ['mp4','avi','flv','wmv','mov']
                    if extension.lower() in video_extensions:                    
                        cam = cv2.VideoCapture(article.article_file.path)
                        if cam.isOpened():                        
                            ret,frame = cam.read()                        
                            name = "media_cdn/articles/preview/output"+str(article.id)+"."+".jpg"
                            cv2.imwrite(name, frame)                        
                            article.preview_image_url="/media/articles/preview/output"+str(article.id)+".jpg"
                            article.is_video=True
                            article.save()
                    else:                    
                        article.preview_image=article.article_file
                        article.save()
                        article.preview_image_url=article.preview_image.url
                        article.is_video=False
                        article.save()
                    # except:
                    # return render(request,'aarticles/article-edit.html',)            

                return HttpResponseRedirect('/admin_panel/articles/view_article/'+str(article.id))
        
        context = {
            'id':id,
            'artName':artName,
            'artDate':artDate,
            'artAuthName':artAuthName,
            'artAuthCountry':artAuthCountry,            
            'artFile':artFile,
            'artFilePreview':article.preview_image,
            'artAuthImage':artAuthImage,
            'artDesc':artDesc,
            'artFileUrl':article.article_file_url,
            'artFilePreviewUrl':article.preview_image_url,
            'artAuthImageUrl':article.author_profile_photo_url,
        }
        messages.add_message(request, messages.INFO, message)
        return render(request,'aarticles/article-edit.html',{'form':form,'context':context})

# import urllib.request
# from django.core.files import File
# import os

class ImportArticleView(TemplateView):
    def get(self,request,*args,**kwargs):
        articles = Article.objects.all().order_by('-created_on')        
        return render(request,'aarticles/articles.html',{'articles':articles,})
    def post(self,request,*args,**kwargs):    
        message=''    
        excel_file = request.FILES["excel_file"]

        # you may put validations here to check extension or file size

        wb = openpyxl.load_workbook(excel_file)

        # getting a particular sheet by name out of many sheets
        worksheet = wb["Sheet1"]
        print(worksheet)
        
        excel_data = list()
        # iterating over the rows and
        # getting value from each cell in row
        for row in worksheet.iter_rows():
            row_data = list()
            for cell in row:
                row_data.append(str(cell.value))
            excel_data.append(row_data)

        status = validate_excel(excel_data)
        if status!="1":            
            messages.add_message(request, messages.INFO, status)
            return HttpResponseRedirect('/admin_panel/articles/article')
        
        # try:
        counter=0
        for row_data in excel_data:
            counter+=1            
            if counter!=1:
                isVideo=True if row_data[8]=="1" else False
                art = Article(                        
                        article_file_url=row_data[0],
                        preview_image_url=row_data[1],
                        title=row_data[2],
                        description=row_data[3],
                        created_on=row_data[4].split(' ')[0],
                        author=row_data[5],
                        author_country=row_data[6],
                        author_profile_photo_url=row_data[7],
                        is_video=isVideo,
                    )
                art.save()                                         
                message='Data saved successfully'
        # except:
            # messages=['Could not save articles..!!',]

        # articles = Article.objects.all().order_by('-created_on')
        messages.add_message(request, messages.INFO, message)
        return HttpResponseRedirect('/admin_panel/articles/article')
        # return render(request,'aarticles/articles.html',{'articles':articles,'messages':messages})


def validate_excel(excel_data):
    counter=0    
    if len(excel_data[0])<8:
        return 'Please use proper excel file format'
    for row_data in excel_data:
        print(row_data)
        print(row_data[0])
        counter += 1
        artFile=row_data[0]
        artPreviewImage=row_data[1]
        artName=row_data[2]
        artDesc=row_data[3]
        artDate=row_data[4]
        artAuthName=row_data[5]
        artAuthCountry=row_data[6]
        artAuthImage=row_data[7]
        isVideo=row_data[8]
        print(counter)
        if counter==1:
            if (artFile!='File Path' or artPreviewImage!='File Preview Image' 
            or artName!='Article Name' or artDesc!='Description' or artDate!='Posted On' 
            or artAuthName!='Author Name' or artAuthCountry!='Author Country' 
            or artAuthImage!='Author Image' or isVideo!='Is Video? [1=yes,0=no]'):
                return 'Please use proper excel file format'                    
        else:
            artDate=artDate.split(' ')[0]
            if not artFile or artFile=="":
                return 'Please provide article(video/image) file link'+' at row '+str(counter)
            if not artPreviewImage or artPreviewImage=="":
                return 'Please provide preview image file link'+' at row '+str(counter)
            if not artName or artName=="":
                return 'Please provide article name'+' at row '+str(counter)
            if not artDesc or artDesc=="":
                return 'Please provide article description'+' at row '+str(counter)
            if not artDate or artDate=="":
                return 'Please provide posted on date'+' at row '+str(counter)
            if not artAuthName or artAuthName=="":
                return "Please provide author's name"+' at row '+str(counter)
            if not artAuthCountry or artAuthCountry=="":
                return "Please provide author's country name"+' at row '+str(counter)
            if not artAuthImage or artAuthImage=="":
                return "Please provide author's image link"+' at row '+str(counter)
            if not isVideo or isVideo=="":
                return "Please provide is video option at row "+str(counter)
            if 'http' not in artFile:
                return "Please provide valid article file link"+' at row '+str(counter)
            if 'http' not in artPreviewImage:
                return "Please provide valid preview image link"+' at row '+str(counter)
            if '-' in artDate:
                if len(artDate.split('-'))==3:
                    try:
                        x = datetime.datetime.strptime(artDate, '%Y-%m-%d')
                        y = datetime.datetime.now().date()
                        if y<x.date():
                            return "Date can not be greater than today"+' at row '+str(counter)
                    except ValueError:
                        return "Incorrect data format, should be YYYY-MM-DD"+' at row '+str(counter)
                else:
                    return 'Date is not in proper format'+' at row '+str(counter)
            else:
                return 'Date is not in proper format'+' at row '+str(counter)
            pattern = re.compile("[A-Za-z ]+")
            if pattern.fullmatch(artAuthName) is None:
                return "Author's name is not valid"+' at row '+str(counter)
            country=None
            country = CountryCode.objects.filter(country__iexact=artAuthCountry)
            print(country)
            if not country or country=="":
                return "Author's Country is not valid"+' at row '+str(counter)
            if 'http' not in artAuthImage:
                return "Author's image link is not valid"+' at row '+str(counter)
            if len(artFile)>8500:
                return "Article file link length is exceeding at row "+str(counter)
            if len(artPreviewImage)>8500:
                return "Preview image link length is exceeding at row "+str(counter)
            if len(artName)>100:
                return "Article name length is exceeding at row "+str(counter)
            if len(artDesc)>500:
                return "Article description length is exceeding at row "+str(counter)
            if len(artAuthName)>15:
                return "Author's name length is exceeding at row "+str(counter)
            if len(artAuthImage)>8500:
                return "Author's image length is exceeding at row "+str(counter)            
            if isVideo not in ('1','0'):
                return "Is Video value is not correct at row "+str(counter)

    return "1"


from pyfcm import FCMNotification
def send_notification_to_all():
    api_key=''
    if api_key!='':
        print('inside push notification')
        ids = User.objects.filter(is_active=True,is_superuser=False).values_list('device_token',flat=True)
        ids = list(ids)

        push_service= FCMNotification(api_key=api_key)
        registration_ids=ids
        message_title="KishMalik Notification"
        message_body='Please check a new article added in the list'
        result=push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title, message_body=message_body)

        users = User.objects.filter(is_active=True,is_superuser=False)
        for u in users:
            un=UserNotification(
                user=u,
                notification=notification_msg,
                req_type='6',
            )
            un.save()
        return True
    return False






# import cv2

# def saveImage(url,art):    
#     extension = url.split('.')[-1]
#     allowed_extensions = ['mp4','avi','flv','wmv','mov']
#     check=0
#     if extension.lower() in allowed_extensions:
#         check=1
#         print('hi')
#         # print(instance.article_file.url)
#         # print(instance.article_file.path)
#         cam = cv2.VideoCapture(url)
#         print(cam)
#         if cam.isOpened():
#             print('hello')
#             ret,frame = cam.read()
#             print(cam.read())
#             name = "media_cdn/articles/vid"+str(instance.id)+"."+extension
#             cv2.imwrite(name, frame)
#             # instance.preview_image='articles/preview/7.jpg'
#             instance.preview_image="/media/articles/preview/output"+str(instance.id)+".jpg"
#             instance.save()
#     else:
#         check=0
#         instance.preview_image=instance.article_file.url
#         instance.save()



    


