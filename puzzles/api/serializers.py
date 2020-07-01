from rest_framework import serializers
from puzzles.models import *


class PuzzleCatSerializer(serializers.ModelSerializer):
    iconurl = serializers.SerializerMethodField()
    class Meta:
        model = PuzzleCategory
        fields = ('id','name','iconurl','created_on')
    def get_iconurl(self,instance):
        return 'baseurl'+instance.iconurl

class PuzzleSerializer(serializers.ModelSerializer):
    videourl = serializers.SerializerMethodField()
    videopreviewurl = serializers.SerializerMethodField()
    class Meta:
        model = Puzzle
        fields = ('id','name','category','videourl','videopreviewurl','description','hint',
                'explanation','learned','created_on')
    def get_videourl(self,instance):
        return 'baseurl'+instance.videourl
    def get_videopreviewurl(self,instance):
        return 'baseurl'+instance.videopreviewurl
    