from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (AllowAny,IsAuthenticated,)
from accounts.api.permissions import IsTokenValid
from rest_framework_jwt.authentication import  JSONWebTokenAuthentication
from accounts.models import *
# from category.models import *
from articles.models import *
from .serializers import *
import openpyxl
#..........

import logging
logger = logging.getLogger('accounts')

class ArticlesListView(APIView):
    # permission_classes=[IsAuthenticated, IsTokenValid,]
    # authentication_classes=[JSONWebTokenAuthentication,]
    def get(self,request,*args,**kwargs):
        queryset = Article.objects.all()
        serializer = ArticlesListSerializer(queryset,many=True,context={'request':request})
        if serializer:
            return Response({
                'message':'Data retrieved successfully',
                'success':'True',
                'data':serializer.data,
            },200)
        return Response({
            'message':'Failed to retrieve data',
            'success':'False',
        },400)

class ArticleDetailView(APIView):
    # permission_classes=[IsAuthenticated, IsTokenValid,]
    # authentication_classes=[JSONWebTokenAuthentication,]
    def get(self,request,*args,**kwargs):
        id = self.kwargs['pk']
        article = Article.objects.filter(id=id).first()
        serializer = ArticleDetailSerializer(article,context={'request':request})
        if serializer:
            return Response({
                'message':'Data retrieved successfully',
                'success':'True',
                'data':serializer.data,
            },200)
        return Response({
            'message':'Failed to retrieve data',
            'success':'False',
        },400)


class CreateArticleView(APIView):    
    def post(self, request, *args,**kwargs):
        serializer = CreateArticleSrializer(data=request.data,context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message':'Data saved successfully',
                'success':True,
                'data':serializer.data,
            },200)
        return Response({
            'message':'Failed to save data',
            'success':False,
        },400)

class DeleteArticleView(APIView):
    def post(self,request,*args,**kwargs):
        pk = self.kwargs['pk']
        article = Article.objects.filter(id=pk).first()
        if article:
            article.delete()
            return Response({
                'message':'Successfully deleted record',
                'success':'True'
            },200)
        else:
            return Response({
                'message':'Not item available to delete',
                'success':'False'
            },400)


class VideoCategoryListView(APIView):
    # permission_classes=[IsAuthenticated, IsTokenValid,]
    # authentication_classes=[JSONWebTokenAuthentication,]
    def get(self,request,*args,**kwargs):
        user=request.user
        serializer1=''
        if not user.is_anonymous:
            print('======================================')
            queryset1=VideoWatchHistory.objects.filter(user=user,video__is_blocked=False).order_by('-created_on').first()
            # if queryset1:
            #     if queryset1.video.is_blocked==True:
            #         queryset1=VideoWatchHistory.objects.filter(user=user,).order_by('-created_on').first()

            if queryset1:
                serializer1=VideoSerializer(queryset1.video,context={'request':request})        
        queryset2=VideoCategory.objects.filter(is_blocked=False).exclude(name='~')   
        for qtemp in queryset2:
            vidcount=Video.objects.filter(category=qtemp).count()
            print(vidcount)
            if vidcount==0:
                queryset2=queryset2.exclude(id=qtemp.id)
        serializer2=VideoCategoryListSerializer(queryset2,many=True,context={'request':request,'user':user})
        if serializer2:

            if not serializer1=='':
                data={
                    'earlier_video_detail':serializer1.data,
                    'category_list':serializer2.data,
                    'is_subscribed':"False",
                }
            else:
                data={
                    'earlier_video_detail':{
                        'id':'',
                        'name':'',
                        'category_id':'',
                        'category':'',
                        'vfileurl':'',
                        'vpreviewurl':'',
                        'description':'',
                        'authorname':'',
                        'authorpicurl':'',
                        'authorcountry':'',
                        'created_on':'',
                        'is_blocked':'',
                        'country_flag':'',
                    },
                    'category_list':serializer2.data,
                    'is_subscribed':"False",
                }
            return Response({
                'message':'Data retrieved successfully',
                'success':'True',
                'data':data,
            },status=200,)
        return Response({
            'message':'Unable to retrieve data',
            'success':'False',            
        },status=400,)

class VideoDetailView(APIView):
    # permission_classes=[IsAuthenticated, IsTokenValid,]
    # authentication_classes=[JSONWebTokenAuthentication,]
    def get(self,request,*args,**kwargs):
        id=self.kwargs['pk']
        queryset = Video.objects.filter(id=id).first()
        if not queryset:
        	return Response({
        		'message':'video id invalid',
        		'success':'False'
        	},status=400)
        # vwh = VideoWatchHistory.objects.filter(video=queryset,user=request.user).first()
        if not request.user.is_anonymous:
            vwh = VideoWatchHistory(
                user = request.user,
                video = queryset,
            )
            vwh.save()
        serializer=VideoDetailSerializer(queryset,context={'request':request})
        if serializer:
            return Response({
                'message':'Data retrieved successfully',
                'success':'True',
                'data':serializer.data,
            },status=200,)
        return Response({
            'message':'Unable to retrieve data',
            'success':'False',            
        },status=400,)

class AddVideoCommentView(APIView):
    permission_classes=[IsAuthenticated, IsTokenValid,]
    authentication_classes=[JSONWebTokenAuthentication,]
    def post(self,request,*args,**kwargs):
        video_id=request.data['video_id']
        comment=request.data['comment']

        if not video_id or video_id=="":
            return Response({
                'message':'Please provide video_id',
                'success':'False'
            },status=400)
        if not comment or comment=="":
            return Response({
                'message':'Please provide comment',
                'success':'False'
            },status=400)

        video_obj=Video.objects.filter(id=int(video_id)).first()
        if not video_id:
            return Response({
                'message':'Video id not available',
                'success':'False'
            },status=400)
        
        vc = VideoComment(
            video=video_obj,
            comment=comment,
            user=request.user,
        )
        vc.save()

        # serializer = VideoCommentSerializer(vc,context={'request':request})
        # if serializer:
        return Response({
            'message':'Comment added successfully',
            'success':'True',
            # 'data':serializer.data,
        },status=200)    

        
        return Response({
            'message':'Unable to serialize data',
            'success':'False',
        },status=400)

class VideoCategoryDeleteView(APIView):
    def post(self,request,*args,**kwargs):
        pk = self.kwargs['pk']
        videocat = VideoCategory.objects.filter(id=pk).first()
        if videocat:
            videocat.delete()
            return Response({
                'message':'Successfully deleted record',
                'success':'True'
            },200)
        else:
            return Response({
                'message':'Not item available to delete',
                'success':'False'
            },400)

class BlockUnblockVideoCategoryView(APIView):
    def post(self,request,*args,**kwargs):
        pk=self.kwargs['pk']
        videocat = VideoCategory.objects.filter(id=pk).first()
        if videocat:
            if videocat.is_blocked:
                videocat.is_blocked=False
                vids = Video.objects.filter(category=videocat)
                for v in vids:
                    v.is_blocked=False
                    v.save()
            else:
                videocat.is_blocked=True
                vids = Video.objects.filter(category=videocat)
                for v in vids:
                    v.is_blocked=True
                    v.save()
            videocat.save()
            return Response({
                'message':'Updated successfully',
                'success':'True',
            },200)
        return Response({
            'message':'Id does not exists',
            'success':'False',
        },400)

class VideoDeleteView(APIView):
    def post(self,request,*args,**kwargs):
        pk = self.kwargs['pk']
        video = Video.objects.filter(id=pk).first()
        if video:
            video.delete()
            return Response({
                'message':'Successfully deleted record',
                'success':'True'
            },200)
        else:
            return Response({
                'message':'Not item available to delete',
                'success':'False'
            },400)

class BlockUnblockVideoView(APIView):
    def post(self,request,*args,**kwargs):
        pk=self.kwargs['pk']
        video = Video.objects.filter(id=pk).first()
        if video:
            if video.is_blocked:
                video.is_blocked=False
            else:
                video.is_blocked=True
            video.save()
            return Response({
                'message':'Updated successfully',
                'success':'True',
            },200)
        return Response({
            'message':'Id does not exists',
            'success':'False',
        },400)
