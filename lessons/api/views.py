from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (AllowAny,IsAuthenticated,)
from accounts.api.permissions import IsTokenValid
from rest_framework_jwt.authentication import  JSONWebTokenAuthentication
from lessons.models import *
from .serializers import *

class BlockUnblockLessonView(APIView):
    def post(self,request,*args, **kwargs):
        id = self.kwargs['pk']
        les = Lesson.objects.filter(id=id).first()
        if not les:
            return Response({
                'message':'Invalid lession id',
                'success':'False',
            },status=400,)
        if les.is_blocked:
            les.is_blocked=False
        else:
            les.is_blocked=True
        les.save()
        return Response({
            'message':'Blocked successfully',
            'success':'True',
        },status=200,)
class DeleteLessonView(APIView):
    def post(self,request,*args, **kwargs):
        id = self.kwargs['pk']
        les = Lesson.objects.filter(id=id).first()
        if not les:
            return Response({
                'message':'Invalid lession id',
                'success':'False',
            },status=400,)
        les.delete()
        return Response({
            'message':'Deleted successfully',
            'success':'True',
        },status=200,)
class BlockUnblockLessonCatView(APIView):
    def post(self,request,*args, **kwargs):
        id = self.kwargs['pk']
        lc = LessonCategory.objects.filter(id=id).first()
        if not lc:
            return Response({
                'message':'Invalid lesson category id',
                'success':'False',
            },status=400,)
        objs = Lesson.objects.filter(category=lc)
        if lc.is_blocked:
            lc.is_blocked=False
            lc.save()
            for o in objs:
                o.is_blocked=False
                o.save()
        else:
            lc.is_blocked = True
            lc.save()
            for o in objs:
                o.is_blocked=True
                o.save()
        return Response({
            'message':'Blocked successfully',
            'success':'True',
        },status=200,)
class DeleteLessonCatView(APIView):
    def post(self,request,*args, **kwargs):
        id = self.kwargs['pk']
        lc = LessonCategory.objects.filter(id=id).first()
        if not lc:
            return Response({
                'message':'Invalid lesson category id',
                'success':'False',
            },status=400,)
        objs = Lesson.objects.filter(category=lc)
        lc.delete()

        return Response({
            'message':'Deleted successfully',
            'success':'True',
        },status=200,)


class LessonCatListView(APIView):
    # permission_classes=[IsAuthenticated,IsTokenValid,]
    # authentication_classes=[JSONWebTokenAuthentication,]
    def get(self,request,*args,**kwargs):
        user=request.user
        serializer1=''
        serializer2=''
        serializer3=''
        
        queryset=LessonCategory.objects.filter(is_blocked=False)
        serializer1 = LessonCatSerializer(queryset,many=True,context={'request':request})



        if not user.is_anonymous:
            print('======================================')
            lm = LessonManagement.objects.filter(player=request.user).order_by('-created_on').first()
            if lm:
                lcat = lm.lesson.category
                fless = Lesson.objects.filter(category=lcat).order_by('id').first()
                serializer2 = LessonSerializer(fless,context={'request':request})
            

            serializer3 = LessonCatUserDetail(request.user)
       

        if serializer1 and serializer2 and serializer3:
            return Response({
                'success':'True',
                'message':'Data retrieved successfully',
                'data':{
                    'Last_Lesson':serializer2.data,
                    'Categories':serializer1.data,
                    'User_Detail':serializer3.data
                },
            },status=200,)
        elif serializer1 and serializer3 and serializer2=='':
            return Response({
                'success':'True',
                'message':'Data retrieved successfully',
                'data':{
                    'Last_Lesson':{
                        "id": '',
                        "category_id": '',
                        "name": "",
                        "category": '',
                        "videourl": "",
                        "videopreviewurl": "",
                        "description": "",
                        "hint": "",
                        "explanation": "",
                        "learned": "",
                        "created_on": ""
                    },
                    'Categories':serializer1.data,
                    'User_Detail':serializer3.data
                },
            },status=200,)
        elif serializer1 and serializer3=='' and serializer2=='':
            return Response({
                'success':'True',
                'message':'Data retrieved successfully',
                'data':{
                    'Last_Lesson':{
                        "id": '',
                        "category_id": '',
                        "name": "",
                        "category": '',
                        "videourl": "",
                        "videopreviewurl": "",
                        "description": "",
                        "hint": "",
                        "explanation": "",
                        "learned": "",
                        "created_on": ""
                    },
                    'Categories':serializer1.data,
                    'User_Detail':{
                        "id": '',
                        "name": "",
                        "profile_image": "",
                        "total_completed_lessons": 0
                    }
                },
            },status=200,)
        
class LessonCatDetailView(APIView):
    # permission_classes=[IsAuthenticated,IsTokenValid,]
    # authentication_classes=[JSONWebTokenAuthentication,]
    def get(self,request,*args,**kwargs):
        id=self.kwargs['pk']
        queryset=LessonCategory.objects.filter(id=id).first()
        if queryset:
            serializer1 = LessonCatSerializer(queryset,context={'request':request})
            ls = Lesson.objects.filter(category=queryset).order_by('id')
            serializer2=''
            if ls:
                print('hellooooo')
                serializer2 = LessonSerializer(ls,many=True,context={'request':request})
            if serializer1 and serializer2:
                return Response({
                    'success':'True',
                    'message':'Data retrieved successfully',
                    'data':{
                        'category_detail':serializer1.data,
                        'lessons':serializer2.data
                    },
                },status=200,)
            else:
                return Response({
                    'success':'True',
                    'message':'Data retrieved successfully',
                    'data':{
                        'category_detail':serializer1.data,
                        'lessons':''
                    },
                },status=200,)
        return Response({
            'success':'False',
            'message':'Invalid id provided',
        },status=400,)
class LessonListView(APIView):
    # permission_classes=[IsAuthenticated,IsTokenValid,]
    # authentication_classes=[JSONWebTokenAuthentication,]
    def get(self,request,*args,**kwargs):
        queryset=Lesson.objects.filter(is_blocked=False)
        serializer = LessonSerializer(queryset,many=True,context={'request':request})
        if serializer:
            return Response({
                'success':'True',
                'message':'Data retrieved successfully',
                'data':serializer.data,
            },status=200,)
class LessonDetailView(APIView):
    # permission_classes=[IsAuthenticated,IsTokenValid,]
    # authentication_classes=[JSONWebTokenAuthentication,]
    def get(self,request,*args,**kwargs):
        id=self.kwargs['pk']
        queryset=Lesson.objects.filter(id=id).first()
        if queryset:
            serializer = LessonSerializer(queryset,context={'request':request})
            if serializer:
                return Response({
                    'success':'True',
                    'message':'Data retrieved successfully',
                    'data':serializer.data,
                },status=200,)
        return Response({
            'success':'False',
            'message':'Invalid id provided',
        },status=400,)

class LessonDetailTempView(APIView):
    def get(self,request,*args,**kwargs):
        lesson_id=self.kwargs['pk']
        if not lesson_id or lesson_id=="":
            return Response({
                'message':'Please provide lesson id',
                'success':'False',
            },status=400)
        lesson=Lesson.objects.filter(id=lesson_id).first()
        if not lesson:
            return Response({
                'message':'Invalid lesson id',
                'success':'False',
            },status=400)
        if lesson.videopreviewurl:
            return Response({
                'message':'Data retrieved successfully',
                'success':'True',
                'data': [{
                    'video_preview_url': 'baseurl'+lesson.videopreviewurl
                }]
            },status=200)
        else:
            return Response({
                'message':'Data retrieved successfully',
                'success':'True',
                'data': ''
            },status=200)
        

class LessonSolvedView(APIView):
    permission_classes=[IsAuthenticated,IsTokenValid,]
    authentication_classes=[JSONWebTokenAuthentication,]
    def post(self,request,*args,**kwargs):
        lesson_id=request.data['lesson_id']
        if not lesson_id or lesson_id=="":
            return Response({
                'message':'Please provide lesson id',
                'success':'False',
            },status=400)
        player=request.user
        lesson=Lesson.objects.filter(id=lesson_id).first()
        if not lesson:
            return Response({
                'message':'Invalid lesson id',
                'success':'False',
            },status=400)
        lm=LessonManagement(
            lesson=lesson,
            player=player
        )
        lm.save()
        return Response({
            'message':'Data saved successfully',
            'success':'True',
        },status=200)