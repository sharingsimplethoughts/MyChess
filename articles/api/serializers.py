from rest_framework import serializers
from rest_framework.exceptions import APIException
from accounts.models import *
from usubscription.models import *
# from category.models import *
from articles.models import *
from django.contrib.sites.shortcuts import get_current_site
# from ffmpy import FFmpeg
import cv2
import datetime
from datetime import date
# from urllib.request import urlretrieve
# from django.core.files import File


class ArticlesListSerializer(serializers.ModelSerializer):
    article_file = serializers.SerializerMethodField()
    preview_image = serializers.SerializerMethodField()
    is_video=serializers.SerializerMethodField()
    class Meta:
        model = Article
        fields = ('id','article_file','title','description','created_on','author','preview_image','is_video')
    def get_article_file(self,instance):        
        current_site = get_current_site(self.context['request'])                    
        if instance.article_file_url:
            if 'http' in instance.article_file_url:
                return instance.article_file_url
            return 'http://'+str(current_site.domain)+instance.article_file_url
        return ''
    def get_preview_image(self,instance):  
        current_site = get_current_site(self.context['request'])                    
        if instance.preview_image_url:
            if 'http' in instance.preview_image_url:
                return instance.preview_image_url
            return 'http://'+str(current_site.domain)+instance.preview_image_url
        return ''
    def get_is_video(self,instance):
        if instance.is_video:
            return instance.is_video
        if instance.article_file_url:
            url=instance.article_file_url
            extension = url.split('.')[-1]
            if extension in ['mp4','avi','flv','wmv','mov']:
                return "true"        
        return "false"
        

        # if instance.article_file:
        #     url=instance.article_file.url
        #     print(url)
        #     extension = url.split('.')[-1]
        #     allowed_extensions = ['mp4','avi','flv','wmv','mov']
        #     check=0
        #     if extension.lower() in allowed_extensions:
        #         check=1
        #         print('hi')
        #         # print(instance.article_file.url)
        #         # print(instance.article_file.path)
        #         cam = cv2.VideoCapture(instance.article_file.path)
        #         print(cam)
        #         if cam.isOpened():
        #             print('hello')
        #             ret,frame = cam.read()
        #             print(cam.read())
        #             name = "media_cdn/articles/preview/output"+str(instance.id)+".jpg"
        #             cv2.imwrite(name, frame)
        #             # instance.preview_image='articles/preview/7.jpg'
        #             instance.preview_image="/media/articles/preview/output"+str(instance.id)+".jpg"
        #             instance.save()
        #     else:
        #         check=0
        #         instance.preview_image=instance.article_file.url
        #         instance.save()
        # if instance.preview_image:
        #     # if check==0:
        #         # return instance.preview_image
        #     request=self.context['request']
        #     current_site = get_current_site(request)            
        #     return 'http://'+str(current_site.domain)+instance.preview_image
        # return ''

class GetCommentSerializer(serializers.ModelSerializer):
    user_name=serializers.SerializerMethodField()
    user_country=serializers.SerializerMethodField()
    user_profile_photo=serializers.SerializerMethodField()
    num_of_days=serializers.SerializerMethodField()
    comment_country_flag=serializers.SerializerMethodField()

    class Meta:
        model=Comment
        fields=('created_on','comment','user_name','user_country','user_profile_photo','num_of_days','comment_country_flag')
    def get_user_name(self,instance):
        return instance.user.name
    def get_user_country(self,instance):
        return instance.user.country
    def get_user_profile_photo(self,instance):
        current_site = get_current_site(self.context['request'])                    
        if instance.user.profile_image:
            return 'http://'+str(current_site.domain)+instance.user.profile_image.url
        return ''
    def get_num_of_days(self,instance):
        d1 = instance.created_on
        d2 = datetime.datetime.now().date()
        delta = d2-d1
        return delta.days
    def get_comment_country_flag(self,instance):
        print(instance.user.country)
        if instance.user.country:
            country = CountryCode.objects.filter(country__iexact=instance.user.country).last()
            return "https://www.countryflags.io/"+country.count_code+"/flat/64.png"
        return ''

class ArticleDetailSerializer(serializers.ModelSerializer):
    comments=serializers.SerializerMethodField()
    article_file=serializers.SerializerMethodField()
    preview_image=serializers.SerializerMethodField()
    author_profile_photo=serializers.SerializerMethodField()
    is_video=serializers.SerializerMethodField()
    country_flag=serializers.SerializerMethodField()
    class Meta:
        model=Article
        fields=('preview_image','article_file','title','description','created_on','number_of_views',
                'author','author_country','country_flag','author_profile_photo','comments','is_video')
    def get_article_file(self,instance):
        current_site = get_current_site(self.context['request'])                    
        if instance.article_file_url:
            if 'http' in instance.article_file_url:
                return instance.article_file_url
            return 'http://'+str(current_site.domain)+instance.article_file_url
        return ''
    def get_preview_image(self,instance):  
        current_site = get_current_site(self.context['request'])                    
        if instance.preview_image_url:
            if 'http' in instance.preview_image_url:
                return instance.preview_image_url
            return 'http://'+str(current_site.domain)+instance.preview_image_url
        return ''
    def get_author_profile_photo(self,instance):        
        current_site = get_current_site(self.context['request'])                    
        if instance.author_profile_photo_url:
            if 'http' in instance.author_profile_photo_url:
                return instance.author_profile_photo_url
            return 'http://'+str(current_site.domain)+instance.author_profile_photo_url
        return ''
    def get_comments(self,instance):
        request = self.context['request']
        queryset = Comment.objects.filter(article=instance)
        serializer = GetCommentSerializer(queryset,many=True,context={'request':request})        
        return serializer.data
    def get_is_video(self,instance):
        if instance.is_video:
            return instance.is_video
        if instance.article_file_url:
            url=instance.article_file_url
            extension = url.split('.')[-1]
            if extension in ['mp4','avi','flv','wmv','mov']:
                return "true"
        return "false"
    def get_country_flag(self,instance):
        print(instance.author_country)
        if instance.author_country:
            country = CountryCode.objects.filter(country__iexact=instance.author_country).last()
            return "https://www.countryflags.io/"+country.count_code+"/flat/64.png"
        return ''

class CreateArticleSrializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('article_file','title','description','created_on','author','author_country','preview_image')
    def validate(self,data):        
        title=data['title']
        decsription=data['description']        
        author=data['author'] 
        author_country=data['author_country']       
        
        if not title or title=="":
            raise APIException({
                'message':'title is required',
                'success':'False',
            })
        if not decsription or decsription=="":
            raise APIException({
                'message':'description is required',
                'success':'False',
            })
        if not author or author=="":
            raise APIException({
                'message':'author is required',
                'success':'False',
            })
        if not author_country or author_country=="":
            raise APIException({
                'message':'author country is required',
                'success':'False',
            })
        return data

    def create(self, validated_data):
        article_file = self.context['request'].FILES.get('article_file')
        title=validated_data['title']
        description=validated_data['description']
        author=validated_data['author']
        author_country=validated_data['author_country']

        print(article_file.name)
        a = Article(
            article_file=article_file,
            title=title,
            description=description,
            author=author,
            author_country=author_country,
        )
        a.save()
        # extension = article_file.name.split('.')[-1]
        # allowed_extensions = ['mp4','avi','flv','wmv','mov']

        # if extension in allowed_extensions:
        #     cam = cv2.VideoCapture('http://127.0.0.1:8000/media_cdn/articles/file_example_MP4_480_1_5MG.mp4')
        #     if cam.isOpened():
        #         print('hi')  
        validated_data['article_file']=a.article_file
        validated_data['created_on']=a.created_on
        validated_data['preview_image']=a.preview_image
        return validated_data
        #

class VideoSerializer(serializers.ModelSerializer):
    category_id=serializers.SerializerMethodField()
    country_flag=serializers.SerializerMethodField()
    created_on=serializers.SerializerMethodField()
    vfileurl=serializers.SerializerMethodField()
    vpreviewurl=serializers.SerializerMethodField()
    authorpicurl=serializers.SerializerMethodField()
    class Meta:
        model=Video
        fields=('id','name','category_id','category','vfileurl','vpreviewurl','description','authorname','authorpicurl','authorcountry','created_on','is_blocked','country_flag')
    def get_created_on(self,instance):
        created_on = datetime.datetime.timestamp(instance.created_on)
        created_on=int(created_on)
        # if 'T' in created_on:
        #     created_on = created_on.split('T')[0]
        # elif ' ' in created_on:
        #     created_on = created_on.split(' ')[0]
        return created_on
    def get_category_id(self,instance):
        return instance.category.id
    def get_country_flag(self,instance):
        print(instance.authorcountry)
        if instance.authorcountry:
            country = CountryCode.objects.filter(country__iexact=instance.authorcountry).last()
            return "https://www.countryflags.io/"+country.count_code+"/flat/64.png"
        return ''
    def get_vfileurl(self,instance):
        if not instance.vfileurl or instance.vfileurl=="":
            return ""
        if 'http' not in instance.vfileurl:
            return 'baseurl'+str(instance.vfileurl)
        return instance.vfileurl
    def get_vpreviewurl(self,instance):
        if not instance.vpreviewurl or instance.vpreviewurl=="":
            return ""
        if 'http' not in instance.vpreviewurl:
            return 'baseurl'+str(instance.vpreviewurl)
        return instance.vpreviewurl
    def get_authorpicurl(self,instance):
        if not instance.authorpicurl or instance.authorpicurl=="":
            return ""
        if 'http' not in 'authorpicurl':
            return 'baseurl'+str(instance.authorpicurl)
        return instance.authorpicurl
class VideoSerializerShort(serializers.ModelSerializer):
    watched=serializers.SerializerMethodField()
    class Meta:
        model=Video
        fields=('name','id','watched')
    def get_watched(self,instance):
        user=self.context['user']
        obj=VideoWatchHistory.objects.filter(video=instance,user=user).first()
        if obj:
            return "True"
        return "False"

class VideoCategoryListSerializer(serializers.ModelSerializer):
    # last_video_detail=serializers.SerializerMethodField()
    category=serializers.SerializerMethodField()
    category_id=serializers.SerializerMethodField()
    video_list=serializers.SerializerMethodField()
    class Meta:
        model=VideoCategory
        fields=('category','category_id','video_list',)#'last_video_detail',
    # def get_last_video_detail(self,instance):
    #     user=self.context['user']
    #     request=self.context['request']
    #     vwobj=VideoWatchHistory.objects.filter(user=user).order_by('-created_on').first()   
    #     if vwobj:     
    #         serializer = VideoSerializer(vwobj.video,context={'request':request})
    #         if serializer:
    #             return serializer.data
    #     return ''
    def get_category(self,instance):
        return instance.name
    def get_category_id(self,instance):
        return instance.id
    def get_video_list(self,instance):
        request=self.context['request']
        user=self.context['user']
        queryset=Video.objects.filter(category=instance,is_blocked=False)        
        serializer=VideoSerializerShort(queryset,many=True,context={'request':request,'user':user})
        if serializer:
            return serializer.data
        return ''

class VideoCommentSerializer(serializers.ModelSerializer):
    user_name=serializers.SerializerMethodField()
    user_country=serializers.SerializerMethodField()
    user_profile_photo=serializers.SerializerMethodField()
    num_of_days=serializers.SerializerMethodField()
    comment_country_flag=serializers.SerializerMethodField()

    class Meta:
        model=VideoComment
        fields=('created_on','comment','user_name','user_country','user_profile_photo','num_of_days','comment_country_flag')
    def get_user_name(self,instance):
        return instance.user.name
    def get_user_country(self,instance):
        return instance.user.country
    def get_user_profile_photo(self,instance):
        current_site = get_current_site(self.context['request'])                    
        if instance.user.profile_image:
            return 'http://'+str(current_site.domain)+instance.user.profile_image.url
        return ''
    def get_num_of_days(self,instance):
        d1 = instance.created_on
        d2 = datetime.datetime.now().date()
        delta = d2-d1
        return delta.days
    def get_comment_country_flag(self,instance):
        print(instance.user.country)
        if instance.user.country:
            country = CountryCode.objects.filter(country__iexact=instance.user.country).last()
            return "https://www.countryflags.io/"+country.count_code+"/flat/64.png"
        return ''

class VideoDetailSerializer(serializers.ModelSerializer):
    category_id=serializers.SerializerMethodField()
    country_flag=serializers.SerializerMethodField()
    comment_detail=serializers.SerializerMethodField()
    created_on=serializers.SerializerMethodField()
    vfileurl=serializers.SerializerMethodField()
    vpreviewurl=serializers.SerializerMethodField()
    authorpicurl=serializers.SerializerMethodField()

    class Meta:
        model=Video
        fields=('name','category_id','category','vfileurl','vpreviewurl','description','authorname','authorpicurl','authorcountry','created_on','is_blocked','country_flag','comment_detail')
    def get_created_on(self, instance):
        created_on = str(instance.created_on)
        if 'T' in created_on:
            created_on = created_on.split('T')[0]
        elif ' ' in created_on:
            created_on = created_on.split(' ')[0]
        return created_on
    def get_category_id(self,instance):
        return instance.category.id
    def get_country_flag(self,instance):
        print(instance.authorcountry)
        if instance.authorcountry:
            country = CountryCode.objects.filter(country__iexact=instance.authorcountry).last()
            return "https://www.countryflags.io/"+country.count_code+"/flat/64.png"
        return ''
    def get_comment_detail(self,instance):
        request=self.context["request"]
        queryset=VideoComment.objects.filter(video=instance)
        serializer=VideoCommentSerializer(queryset,many=True,context={"request":request})
        if serializer:
            return serializer.data
        return ''
    def get_vfileurl(self,instance):
        if not instance.vfileurl or instance.vfileurl=="":
            return ""
        if 'http' not in instance.vfileurl:
            return 'baseurl'+str(instance.vfileurl)
        return instance.vfileurl
    def get_vpreviewurl(self,instance):
        if not instance.vpreviewurl or instance.vpreviewurl=="":
            return ""
        if 'http' not in instance.vpreviewurl:
            return 'baseurl'+str(instance.vpreviewurl)
        return instance.vpreviewurl
    def get_authorpicurl(self,instance):
        if not instance.authorpicurl or instance.authorpicurl=="":
            return ""
        if 'http' not in instance.authorpicurl:
            return 'baseurl'+str(instance.authorpicurl)
        return instance.authorpicurl

