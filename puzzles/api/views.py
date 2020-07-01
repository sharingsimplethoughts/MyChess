from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (AllowAny,IsAuthenticated,)
from accounts.api.permissions import IsTokenValid
from rest_framework_jwt.authentication import  JSONWebTokenAuthentication
from puzzles.models import *
from .serializers import *

class BlockUnblockPuzzleView(APIView):
    def post(self,request,*args, **kwargs):
        id = self.kwargs['pk']
        les = Puzzle.objects.filter(id=id).first()
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
class DeletePuzzleView(APIView):
    def post(self,request,*args, **kwargs):
        id = self.kwargs['pk']
        les = Puzzle.objects.filter(id=id).first()
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
class BlockUnblockPuzzleCatView(APIView):
    def post(self,request,*args, **kwargs):
        id = self.kwargs['pk']
        lc = PuzzleCategory.objects.filter(id=id).first()
        if not lc:
            return Response({
                'message':'Invalid puzzle category id',
                'success':'False',
            },status=400,)
        objs = Puzzle.objects.filter(category=lc)
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
class DeletePuzzleCatView(APIView):
    def post(self,request,*args, **kwargs):
        id = self.kwargs['pk']
        lc = PuzzleCategory.objects.filter(id=id).first()
        if not lc:
            return Response({
                'message':'Invalid puzzle category id',
                'success':'False',
            },status=400,)
        objs = Puzzle.objects.filter(category=lc)
        lc.delete()

        return Response({
            'message':'Deleted successfully',
            'success':'True',
        },status=200,)


class PuzzleCatListView(APIView):
    # permission_classes=[IsAuthenticated,IsTokenValid,]
    # authentication_classes=[JSONWebTokenAuthentication,]
    def get(self,request,*args,**kwargs):
        queryset=PuzzleCategory.objects.filter(is_blocked=False)
        serializer = PuzzleCatSerializer(queryset,many=True,context={'request':request})
        if serializer:
            return Response({
                'success':'True',
                'message':'Data retrieved successfully',
                'data':serializer.data,
            },status=200,)
class PuzzleCatDetailView(APIView):
    # permission_classes=[IsAuthenticated,IsTokenValid,]
    # authentication_classes=[JSONWebTokenAuthentication,]
    def get(self,request,*args,**kwargs):
        id=self.kwargs['pk']
        queryset=PuzzleCategory.objects.filter(id=id).first()
        if queryset:
            serializer = PuzzleCatSerializer(queryset,context={'request':request})
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
class PuzzleListView(APIView):
    # permission_classes=[IsAuthenticated,IsTokenValid,]
    # authentication_classes=[JSONWebTokenAuthentication,]
    def get(self,request,*args,**kwargs):
        queryset=Puzzle.objects.filter(is_blocked=False)
        serializer = PuzzleSerializer(queryset,many=True,context={'request':request})
        if serializer:
            return Response({
                'success':'True',
                'message':'Data retrieved successfully',
                'data':serializer.data,
            },status=200,)
class PuzzleDetailView(APIView):
    # permission_classes=[IsAuthenticated,IsTokenValid,]
    # authentication_classes=[JSONWebTokenAuthentication,]
    def get(self,request,*args,**kwargs):
        id=self.kwargs['pk']
        queryset=Puzzle.objects.filter(id=id).first()
        if queryset:
            serializer = PuzzleSerializer(queryset,context={'request':request})
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

class PuzzleSolvedView(APIView):
    permission_classes=[IsAuthenticated,IsTokenValid,]
    authentication_classes=[JSONWebTokenAuthentication,]
    def post(self,request,*args,**kwargs):
        puzzle_id=request.data['puzzle_id']
        if not puzzle_id or puzzle_id=="":
            return Response({
                'message':'Please provide puzzle id',
                'success':'False',
            },status=400)
        player=request.user
        puzzle=Puzzle.objects.filter(id=puzzle_id).first()
        if not puzzle:
            return Response({
                'message':'Invalid puzzle id',
                'success':'False',
            },status=400)
        pm=PuzzleManagement(
            puzzle=puzzle,
            player=player
        )
        pm.save()
        return Response({
            'message':'Data saved successfully',
            'success':'True',
        },status=200)