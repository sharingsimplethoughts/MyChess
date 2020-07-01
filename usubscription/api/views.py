from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (AllowAny,IsAuthenticated,)
from accounts.api.permissions import IsTokenValid
from rest_framework_jwt.authentication import  JSONWebTokenAuthentication
from accounts.models import *
from usubscription.models import *
from .serializers import *

import logging
logger = logging.getLogger('accounts')

class GetPlanListView(APIView):
    permission_classes=[IsAuthenticated,IsTokenValid,]
    authentication_classes=[JSONWebTokenAuthentication,]
    def get(self,request,*args,**kwargs):
        queryset = SubscriptionPlan.objects.all()
        serializer = GetPlanListSerializer(queryset,many=True)
        if serializer:
            return Response({
                'success':'True',
                'message':'Data retrieved successfully',
                'data':serializer.data,
            },status=200)
        return Response({
            'success':'False',
            'message':'Failed to retrieve data',            
        },status=400)

class BlockUnclockSubscriptionView(APIView):
    def get(self,request,*args, **kwargs):
        id=self.kwargs['pk']
        ach = SubscriptionPlan.objects.filter(id=id).first()
        if ach:
            if ach.is_blocked:
                ach.is_blocked=False
            else:
                ach.is_blocked=True
            ach.save()
            return Response({
                'message':'Data deleted successfully',
                'success':'True',
            },status=200,)
        else:
            return Response({
                'message':'id is invalid',
                'success':'False',
            },status=400,)
class DeleteSubscriptionView(APIView):
    def get(self,request,*args, **kwargs):
        id=self.kwargs['pk']
        ach = SubscriptionPlan.objects.filter(id=id).first()
        if ach:
            ach.is_deleted=True
            ach.save()
            return Response({
                'message':'Data deleted successfully',
                'success':'True',
            },status=200,)
        else:
            return Response({
                'message':'id is invalid',
                'success':'False',
            },status=400,)
