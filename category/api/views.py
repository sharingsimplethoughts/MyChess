from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (AllowAny,IsAuthenticated,)
from accounts.api.permissions import IsTokenValid
from rest_framework_jwt.authentication import  JSONWebTokenAuthentication
from accounts.models import *
from category.models import *
from .serializers import *

import logging
logger = logging.getLogger('accounts')

class CategoryListView(APIView):
    permission_classes=[IsAuthenticated,IsTokenValid]
    authentication_classes=[JSONWebTokenAuthentication,]
    def get(self,request,*args,**kwargs):
        logger.debug('Category list get called')
        logger.debug(request.data)
        queryset = Category.objects.all()
        serializer = CategoryListSerializer(queryset,many=True,context={'request':request})
        if serializer:
            return Response({
                'success':'True',
                'message':'Category list retrieved successfully',
                'data':serializer.data
            },status=200)
        return Response({
            'success':'False',
            'message':'Category list retrieve failed',            
        },status=400)

class VideoDetailView(APIView):
    permission_classes=[IsAuthenticated,IsTokenValid,]
    authentication_classes=[JSONWebTokenAuthentication,]
    def get(self,request,*args,**kwargs):
        logger.debug('Video detail get api called')
        logger.debug(request.data)
        id = self.kwargs['pk']
        queryset=Video.objects.filter(id=id).first()
        serializer=VideoDetailSerializer(queryset,context={'request':request})
        if serializer:
            return Response({
                'success':'True',
                'message':'Data retrieved successfully',
                'data':serializer.data,
            },status=200,)
        return Response({
            'success':'False',
            'message':'Data retrieve failed',
            'data':serializer.data,
        },status=200,)