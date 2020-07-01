from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.filters import (SearchFilter, OrderingFilter,)
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.permissions import (AllowAny, IsAuthenticated,)
from accounts.api.permissions import IsTokenValid
from rest_framework_jwt.authentication import  JSONWebTokenAuthentication
from pyfcm import FCMNotification
from django.contrib.sites.shortcuts import get_current_site

from accounts.models import *
# from category.models import *
from articles.models import *
from game.models import *
from .serializers import *

from twilio.rest import Client

account = "sda"
token = "we"
from_no = "ewr"
client = Client(account, token)

import logging
logger = logging.getLogger('accounts')

def send_message(friend,notification_msg):
    try:
        country_code=friend.country_code
        mobile_number=friend.mobile
        message = client.messages.create(
            to=country_code+mobile_number,
            from_=from_no,
            body=notification_msg
        )
        print('end of try')
    except:
        return 0
    return 1

class SearchByUserNameView(APIView):
    permission_classes=[IsAuthenticated, IsTokenValid,]
    authentication_classes=[JSONWebTokenAuthentication,]
    # serializer_class=MultipleUserDetailSerializer
    # def get_queryset(self,request,*args,**kwargs):
    #     query=self.request.GET.get('q',None)
    #     friends=''
    #     if query:
    #         friends=User.objects.filter(Q(name__icontains=query)|Q(first_name__icontains=query)|Q(last_name__icontains=query))
    #     return friends
    def post(self,request,*args,**kwargs):
        # qs=self.get_queryset(request)
        username=request.data['username']
        friends=''
        if username:
            friends=User.objects.filter(Q(name__icontains=username)|Q(first_name__icontains=username)|Q(last_name__icontains=username))
            if friends:
                serializer=SpecificUserDetailSerializer(friends,many=True,context={'request':request})
                if serializer:
                    return Response({
                        'message':'Data Retrieved successfully',
                        'success':'True',
                        'data':serializer.data,
                    },status=200)
                return Response({
                    'message':'Data Retrieve failed',
                    'success':'False',
                },status=400)
            return Response({
                'message':'No user with this username',
                'success':'False',
            },status=400)
        return Response({
            'message':'Please provide username',
            'success':'False',
        },status=400)
class SearchByEmailView(ListAPIView):
    permission_classes=[IsAuthenticated, IsTokenValid,]
    authentication_classes=[JSONWebTokenAuthentication,]
    # serializer_class=MultipleUserDetailSerializer
    # def get_queryset(self,request,*args,**kwargs):
    #     query=self.request.GET.get('q',None)
    #     friends=''
    #     if query:
    #         friends=User.objects.filter(Q(email=query))
    #     return friends
    def post(self,request,*args,**kwargs):
        # qs=self.get_queryset(request)
        email=request.data['email']
        friends=''
        if email:
            friends=User.objects.filter(Q(email=email)).first()
            if friends:
                serializer=SpecificUserDetailSerializer(friends,context={'request':request})
                if serializer:
                    return Response({
                        'message':'Data Retrieved successfully',
                        'success':'True',
                        'data':serializer.data,
                    },status=200)
                return Response({
                    'message':'Data Retrieve failed',
                    'success':'False',
                },status=400)
            return Response({
                'message':'No user with this email',
                'success':'False',
            },status=400)
        return Response({
            'message':'Please provide email',
            'success':'False',
        },status=400)
class SearchFriendView(ListAPIView):
    permission_classes=[IsAuthenticated, IsTokenValid,]
    authentication_classes=[JSONWebTokenAuthentication,]
    serializer_class=SearchFriendListSerializer
    filter_backends=(SearchFilter,OrderingFilter,)
    # search_fields=['slug1','slug2','state','city','country','service_type','service_subtype',]
    def get_queryset(self,request,*args,**kwargs):
        user=request.user
        queryset_list=Friends.objects.filter(player=user,status='2')
        
        query=self.request.GET.get('q',None)

        print('----------------')
        print(query)
        if query:
            queryset_list=queryset_list.filter(
                Q(friend__name__icontains=query)|
                Q(friend__email__icontains=query)|
                Q(friend__mobile__icontains=query)
            ).distinct()
        print(queryset_list)
        return queryset_list
    def list(self,request,*args,**kwargs):
        logger.debug('friend search list called')
        logger.debug(self.request.data)
        qs=self.get_queryset(request)
        data=SearchFriendListSerializer(qs,many=True,context={'request':request}).data
        print(data)
        return Response({
            'message':'data retrieved successfully',
            'success':'True',
            'data':data,
        },status=200,)

#--------------------------------------------

class SendFriendRequestView(APIView):
    permission_classes=[IsAuthenticated, IsTokenValid,]
    authentication_classes=[JSONWebTokenAuthentication,]
    def post(self,request,*args,**kwargs):
        user=request.user
        fid=request.data['friend_id']
        friend=User.objects.filter(id=fid).first()
        if not friend:
            return Response({
                'message':'Invalid friend id',
                'success':'False',
            },status=400)

        exists=Friends.objects.filter(player=user,friend=friend).first()
        exists1=Friends.objects.filter(player=friend,friend=user).first()
        if exists or exists1:
            return Response({
                'message':'This friend already exists in list',
                'success':'False',
            },status=400)

        fr = Friends(
            player=user,
            friend=friend,
        )
        fr.save()
        # Adding vice verse friend
        fr1 = Friends(
            player=friend,
            friend=user,
        )
        fr1.save()

        notification_msg="Notification-from KishMalik-Friend request from "+user.name
        un=UserNotification(
            user=friend,
            notification=notification_msg,
            req_type='1',
            ref_id=user.id,
        )
        un.save()

        if api_key!='':
            print('inside push notification')
            push_service= FCMNotification(api_key=api_key)
            registration_id=friend.device_token
            message_title="KishMalik Notification"
            message_body=notification_msg
            result=push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)
            

        # sms notification
        res=send_message(friend,notification_msg)
        if res:
            return Response({
                'message':'Friend request sent successfully',
                'success':'True',
            },status=200)
        else:
            return Response({
                'message':'Friend request sent but unable to send sms',
                'success':'False'
            },status=400)
class FriendInvitationListView(APIView):
    permission_classes=[IsAuthenticated, IsTokenValid,]
    authentication_classes=[JSONWebTokenAuthentication,]
    def get(self,request,*args,**kwargs):
        user=request.user
        queryset=UserNotification.objects.filter(user=user,req_type='1')
        serializer=NotificationListSerializer(queryset,many=True,context={'request':request})
        if serializer:
            return Response({
                'message':'Data retrieved successfully',
                'success':'True',
                'data':serializer.data,
            },status=200)
        return Response({
            'message':'Data retrieve failed',
            'success':'False',
        },status=400)
class AcceptFriendRequestView(APIView):
    permission_classes=[IsAuthenticated, IsTokenValid,]
    authentication_classes=[JSONWebTokenAuthentication,]
    def post(self,request,*args,**kwargs):
        user=request.user
        request_id=request.data['request_id']
        un = UserNotification.objects.filter(id=request_id).first()
        if not un:
            return Response({
                'message':'Request id is not valid',
                'success':'False',
            },status=400,)
        friend=User.objects.filter(id=un.ref_id).first()

        fr = Friends.objects.filter(player=user,friend=friend).first()
        fr1 = Friends.objects.filter(player=friend,friend=user).first()
        
        fr.status='2'
        fr1.status='2'
        fr.save()
        fr1.save()

        un.status='2'
        un.save()

        return Response({
            'message':'Request accepted successfully',
            'success':'True'
        },status=200,)
class DeclineFriendRequest(APIView):
    permission_classes=[IsAuthenticated, IsTokenValid,]
    authentication_classes=[JSONWebTokenAuthentication,]
    def post(self,request,*args,**kwargs):
        user=request.user
        request_id=request.data['request_id']
        un = UserNotification.objects.filter(id=request_id).first()
        if not un:
            return Response({
                'message':'Request id is not valid',
                'success':'False',
            },status=400,)
        friend=User.objects.filter(id=un.ref_id).first()

        fr = Friends.objects.filter(player=user,friend=friend).first()
        fr1 = Friends.objects.filter(player=friend,friend=user).first()
        fr.status='3'
        fr1.status='3'
        fr.save()
        fr1.save()

        un.status='2'
        un.save()
        
        return Response({
            'message':'Request declined successfully',
            'success':'True'
        },status=200,)

#--------------------------------------------

class SendGameRequestView(APIView):
    permission_classes=[IsAuthenticated, IsTokenValid,]
    authentication_classes=[JSONWebTokenAuthentication,]
    def post(self,request,*args,**kwargs):
        user=request.user
        game_type=request.data['game_type']
        gt=GameType.objects.filter(id=game_type).first()
        if not gt:
            return Response({
                'message':'Game type is not valid',
                'success':'False',
            },status=400)

        fid=request.data['friend_id']
        friend=User.objects.filter(id=fid).first()
        if not friend:
            return Response({
                'message':'Invalid friend id',
                'success':'False',
            },status=400)

        dur=request.data['duration']
        duration = GameDuration.objects.filter(id=dur).first()
        if not duration:
            return Response({
                'message':'Invalid game duration',
                'success':'False',
            },status=400)
        room_id=request.data['room_id']

        exists=Friends.objects.filter(player=user,friend=friend).first()
        if not exists:
            return Response({
                'message':'Requested user is not in friend list',
                'success':'False',
            },status=400)
        
        g=Game(
            game_type=gt,
            player1=user,
            player2=friend,
            duration=duration,
            room_id=room_id,
        )
        g.save()

        notification_msg="Notification-from KishMalik-You are invited by "+user.name
        serializer=GetGameDetailSerializer(g)
        data=serializer.data
        ndata=data
        ndata['message']=notification_msg
        
        un=UserNotification(
            user=friend,
            # notification=ndata,
            notification=notification_msg,
            req_type='2',
            ref_id=g.id,
        )
        un.save()

        api_key=''
        if api_key!='':
            push_service= FCMNotification(api_key=api_key)
            registration_id=friend.device_token
            message_title="KishMalik Notification"
            message_body=notification_msg
            result=push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)

        res=send_message(friend,notification_msg)
        if res:
            return Response({
                'message':'Request sent successfully',
                'success':'True',
                'data':serializer.data,
            },status=200)
        else:
            return Response({
                'message':'Game request sent but unable to send sms',
                'success':'False'
            },status=400)
class NotificationListView(APIView):
    permission_classes=[IsAuthenticated, IsTokenValid,]
    authentication_classes=[JSONWebTokenAuthentication,]
    def get(self,request,*args,**kwargs):
        user=request.user
        queryset=UserNotification.objects.filter(user=user)
        serializer=NotificationListSerializer(queryset,many=True,context={'request':request})
        if serializer:
            return Response({
                'message':'Data retrieved successfully',
                'success':'True',
                'data':serializer.data,
            },status=200)
        return Response({
            'message':'Data retrieve failed',
            'success':'False',
        },status=400)
class AcceptGameRequestView(APIView):
    permission_classes=[IsAuthenticated, IsTokenValid,]
    authentication_classes=[JSONWebTokenAuthentication,]
    def post(self,request,*args,**kwargs):
        request_id=request.data['request_id']
        un=UserNotification.objects.filter(id=request_id).first()
        g=Game.objects.filter(id=un.ref_id).first()
        g.status='2'
        g.save()
        un.status='2'
        un.save()
        return Response({
            'message':'Status updated successfully',
            'success':'True',
        },status=200)
class DeclineGameRequest(APIView):
    permission_classes=[IsAuthenticated, IsTokenValid,]
    authentication_classes=[JSONWebTokenAuthentication,]
    def post(self,request,*args,**kwargs):
        request_id=request.data['request_id']
        un=UserNotification.objects.filter(id=request_id).first()
        g=Game.objects.filter(id=un.ref_id).first()
        g.status='3'
        g.save()
        un.status='2'
        un.save()
        return Response({
            'message':'Status updated successfully',
            'success':'True',
        },status=200)
class TimeOutHitView(APIView):
    permission_classes=[IsAuthenticated, IsTokenValid,]
    authentication_classes=[JSONWebTokenAuthentication,]
    def post(self,request,*args,**kwargs):
        game_id=request.data['game_id']
        g=Game.objects.filter(id=game_id).first()
        if not g:
            return Response({
                'message':'Invalid game id',
                'success':'False',
            },status=400)
        g.status='4'
        g.save()
        return Response({
            'message':'Status updated successfully',
            'success':'True',
        },status=200)

#--------------------------------------------

class GetGameDetailView(APIView):
    permission_classes=[IsAuthenticated, IsTokenValid,]
    authentication_classes=[JSONWebTokenAuthentication,]
    def get(self,request,*args,**kwargs):
        game_id=self.kwargs['pk']
        queryset = Game.objects.filter(id=game_id).first()
        if not queryset:
            return Response({
                'message':'Invalid game id',
                'success':'False',
            },status=400)    
        serializer=GetGameDetailSerializer(queryset,context={'request':request})
        if serializer:
            return Response({
                'message':'Data retrieved successfully',
                'success':'True',
                'data':serializer.data,
            },status=200)
        return Response({
            'message':'Data retrieve failed',
            'success':'False',
        },status=400)

class GetMultipleUserDetailView(APIView):
    def post(self,request,*args,**kwargs):
        ids=request.data['ids']
        if not ids or ids=="":
            return Response({
                'message':'Please provide ids',
                'success':'False',
            },status=400)
        if ',' in ids:
            id_list=ids.split(',')
        else:
            id_list=[ids]
        queryset=User.objects.filter(id__in=id_list)
        serializer=MultipleUserDetailSerializer(queryset,many=True,context={'request':request})
        if serializer.data:
            return Response({
                'message':'Data retrieved successfully',
                'success':'True',
                'data':serializer.data,
            },status=200)
        return Response({
            'message':'Data retrieve failed',
            'success':'False',
        },status=400)

class GetUserDetailTempView(APIView):
    def get(self,request,*args,**kwargs):
        id = self.kwargs['pk']
        queryset=User.objects.filter(id=id).first()
        if not queryset:
            return Response({
            'message':'Please provide valid user id',
            'success':'False',
        },status=400)
        serializer=MultipleUserDetailSerializer(queryset,context={'request':request})
        if serializer.data:
            return Response({
                'message':'Data retrieved successfully',
                'success':'True',
                'data':serializer.data,
            },status=200)
        return Response({
            'message':'Data retrieve failed',
            'success':'False',
        },status=400)



class SubmitBeforeGameView(APIView):
    permission_classes=[IsAuthenticated, IsTokenValid,]
    authentication_classes=[JSONWebTokenAuthentication,]
    def post(self,request,*args, **kwargs):
        user = request.user
        if 'some_text' in request.data.keys():
            some_text = request.data['some_text']
            if not some_text or some_text=="":
                return Response({
                    'message':'some_text is missing',
                    'success':'False'
                },status=400,)    
        else:
            return Response({
                'message':'some_text is missing',
                'success':'False'
            },status=400,)
        if user:
            user.is_online=2
            user.save()
            return Response({
                'message':'Data saved successfully',
                'success':'True',
            },status=200)
        return Response({
            'message':'No user found',
            'success':'False',
        },status=400)

class SubmitGameDataView(APIView):
    permission_classes=[IsAuthenticated, IsTokenValid,]
    authentication_classes=[JSONWebTokenAuthentication,]
    def post(self,request,*args,**kwargs):
        serializer=SubmitGameDataSerializer(data=request.data,context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message':'Data saved successfully',
                'success':'True',
            },status=200)
        return Response({
            'message':'Dvvcxvxcvxata submit failed',
            'success':'False',
        },status=400)

class UpdatePointView(APIView):
    permission_classes=[IsAuthenticated, IsTokenValid,]
    authentication_classes=[JSONWebTokenAuthentication,]
    def post(self,request,*args,**kwargs):
        serializer=UpdatePointSerializer(data=request.data,context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message':'Data saved successfully',
                'success':'True',
            },status=200)
        # return Response({
        #     'message':'Data submit failed',
        #     'success':'False',
        # },status=400)


class RecentOpponentView(APIView):
    permission_classes=[IsAuthenticated, IsTokenValid,]
    authentication_classes=[JSONWebTokenAuthentication,]
    def get(self, request, *args, **kwargs):
        user=request.user
        queryset=Game.objects.filter(Q(player1=user)|Q(player2=user)).exclude(status='finished').order_by('-created_on')[:5]
        serializer=RecentOpponentSerializer(queryset,many=True,context={'request':request})
        if serializer:
            return Response({
                'message':'Data retrieved successfully',
                'success':'True',
                'data':serializer.data,
            },status=200)
        return Response({
            'message':'Data retrieve failed',
            'success':'False',
        },status=400)




class UploadImageTemporaryApiRequiredByAbhishekOnlyView(APIView):
    def post(self,request,*args,**kwargs):
        sample_image = request.FILES.get('sample_image')
        if not sample_image or sample_image=='':
            return Response({
            'message':'Had he year, sample image to do..',
            'success':'False',
        },status=400,)
        samp = SampleImageStore(
            sample_image=sample_image,
        )
        samp.save()
        current_site = get_current_site(request)
        print(current_site.domain)
        return Response({
            'message':'Kar diya save. url niche he, le lo.',
            'success':'True',
            'data':'http://'+str(current_site)+samp.sample_image.url,
        },status=200,)

class DeleteNotificationUserView(APIView):
    def post(self,request,*args, **kwargs):
        id = self.kwargs['pk']
        id = ','+str(id)+','
        u = SampleImageStore.objects.filter(unique_identification='un_ap_1').first()
        
        if not u:
            return Response({
                'message':'The id is not valid',
                'success':'False',
            },status=400,)
        if u:
            str1 = u.sample_data.replace(id,',')
            u.sample_data = str1
            u.save()
        return Response({
            'message':'deleted successfully',
            'success':'True',
        },status=200,)

class DeleteNotificationGroupView(APIView):
    def post(self,request,*args, **kwargs):
        pid = self.kwargs['pk']
        id = ','+str(id)+','
        g = SampleImageStore.objects.filter(unique_identification='un_ap_2').first()
        if not g:
            return Response({
                'message':'The id is not valid',
                'success':'False'
            },status=400,)
        if g:
            str1 = g.sample_data.replace(id,',')
            g.sample_data = str1
            g.save()
        return Response({
            'message':'deleted successfully',
            'success':'True',
        },status=200,)

#----------------------------------------------

class GameDurationListView(APIView):
    def get(self,request,*args,**kwargs):
        queryset = GameDuration.objects.filter(is_active=True)
        serializer = GameDurationListSerializer(queryset,many=True,context={'request':request})
        if serializer:
            return Response({
                'message':'Successfully retrieved data',
                'success':'True',
                'data':serializer.data,
            },status=200)
        return Response({
            'message':'Data retrieve failed',
            'success':'False',
        },status=400)
class GameDurationDeleteView(APIView):
    def post(self,request,*args, **kwargs):
        id = self.kwargs['pk']
        if id:
            obj = GameDuration.objects.filter(id=id).first()
            if obj:
                obj.delete()
                return Response({
                    'message':'Duration deleted successfully',
                    'success':'True'
                },status=200)
            return Response({
                'message':'Please provide valid duration id',
                'success':'False'
            },status=400)
        return Response({
            'message':'Please provide duration id',
            'success':'False'
        },status=400)
class GameDurationBlockUnblockView(APIView):
    def post(self,request,*args, **kwargs):
        id = self.kwargs['pk']
        if id:
            obj = GameDuration.objects.filter(id=id).first()
            if obj:
                if obj.is_active:
                    obj.is_active = False
                else:
                    obj.is_active = True
                obj.save()
                return Response({
                    'message':'Duration updated successfully',
                    'success':'True'
                },status=200)
            return Response({
                'message':'Please provide valid duration id',
                'success':'False'
            },status=400)
        return Response({
            'message':'Please provide duration or id',
            'success':'False'
        },status=400)