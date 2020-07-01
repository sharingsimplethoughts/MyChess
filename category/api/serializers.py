from rest_framework import serializers
from rest_framework.exceptions import APIException
from accounts.models import *
from usubscription.models import *
from category.models import *

video_detail_url=serializers.HyperlinkedIdentityField(
    view_name='category:video_detail',lookup_field='pk')


class GetCommentsSerializer(serializers.ModelSerializer):
    user_image = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()
    user_country = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ['text','created_on','user_image','user_name','user_country']
    def get_user_image(self,instance):
        if instance.user.profile_image:
            return instance.user.profile_image
        return ''
    def get_user_name(self,instance):
        return instance.user.name
    def get_user_country(self,instance):
        return instance.user.country_code

class VideoDetailSerializer(serializers.ModelSerializer):
    user_image = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()
    user_country = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    class Meta:
        model = Video
        fields = ['title','video_file','user_image','user_name','user_country','detail','comments']
    def get_user_image(self,instance):
        if instance.user.profile_image:
            return instance.user.profile_image
        return ''
    def get_user_name(self,instance):
        return instance.user.name
    def get_user_country(self,instance):
        return instance.user.country_code
    def get_comments(self,instance):
        request=self.context['request']
        queryset = Comment.objects.filter(video=instance)
        serializer = GetCommentsSerializer(queryset,many=True,context={'request':request})
        return serializer.data
    
class GetVideoTitleSerializer(serializers.ModelSerializer):
    video_detail_url = video_detail_url
    class Meta:
        model=Video
        fields=['title','video_detail_url']

class CategoryListSerializer(serializers.ModelSerializer):
    video = serializers.SerializerMethodField()     
    class Meta:
        model=Category
        fields=['category_name','video']

    def get_video(self,instance):
        request=self.context['request']
        queryset = Video.objects.filter(category=instance)
        serializer = GetVideoTitleSerializer(queryset,many=True,context={'request':request})
        return serializer.data
