from rest_framework import serializers
from lessons.models import *


class LessonCatSerializer(serializers.ModelSerializer):
    iconurl = serializers.SerializerMethodField()
    total_lessons = serializers.SerializerMethodField()
    completed_lessons = serializers.SerializerMethodField()
    
    class Meta:
        model = LessonCategory
        fields = ('id','name','iconurl','created_on','total_lessons','completed_lessons')
    def get_iconurl(self,instance):
        return 'baseurl'+instance.iconurl
    def get_total_lessons(self,instance):
        return Lesson.objects.filter(category=instance).count()
    def get_completed_lessons(self,instance):
        request = self.context['request']
        user = request.user
        if user.is_anonymous:
            return 0
        return LessonManagement.objects.filter(player=user,lesson__category=instance).count()
    


class LessonSerializer(serializers.ModelSerializer):
    videourl = serializers.SerializerMethodField()
    videopreviewurl = serializers.SerializerMethodField()
    category_id = serializers.SerializerMethodField()
    class Meta:
        model = Lesson
        fields = ('id','category_id','name','category','videourl','videopreviewurl','description','hint',
                'explanation','learned','created_on')
    def get_videourl(self,instance):
        return 'baseurl'+instance.videourl
    def get_videopreviewurl(self,instance):
        return 'baseurl'+instance.videopreviewurl
    def get_category_id(self,instance):
        return instance.category.id

class LessonCatUserDetail(serializers.ModelSerializer):
    total_completed_lessons = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('id','name','profile_image','total_completed_lessons')
    def get_profile_image(self,instance):
        if instance.profile_image:
            return instance.profile_image.url
        return ''
    def get_total_completed_lessons(self,instance):
        return LessonManagement.objects.filter(player=instance).count()

# class LessonSlideWiseSerializer(serializers.ModelSerializer):
#     first_lesson_detail = serializers.ModelSerializer()
#     lesson_cat_detail = serializers.ModelSerializer()
#     user_detail = serializers.SerializerMethodField()
#     class Meta:
#         model = Lesson
#         fields = ('first_lesson_detail','lesson_cat_detail','user_detail')
#     def first_lesson_detail(self,instance):

    