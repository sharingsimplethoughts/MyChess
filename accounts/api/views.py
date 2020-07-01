from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from accounts.api.tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from rest_framework.status import (
                                        HTTP_200_OK,
                                    	HTTP_400_BAD_REQUEST,
                                    	HTTP_204_NO_CONTENT,
                                    	HTTP_201_CREATED,
                                    	HTTP_500_INTERNAL_SERVER_ERROR,
                                )

from rest_framework.permissions import (AllowAny,IsAuthenticated,)
from .permissions import IsTokenValid
from rest_framework_jwt.authentication import  JSONWebTokenAuthentication
from accounts.models import *
from .serializers import *
from . password_reset_form_api import MyPasswordResetForm
from .settings import (
	PasswordResetSerializer,
)

from twilio.rest import Client
import random

account = "sasd"
token = "wqeq"
from_no = "sdas"
client = Client(account, token)


import logging
logger = logging.getLogger('accounts')

def id_generator(size=4):
    return random.randint(1000,9999)
def send_otp(country_code,mobile_number):
    verification_code = id_generator(size=4)
    try:
        message = client.messages.create(
            to=country_code+mobile_number,
            from_=from_no,
            body="Hello there! Your KishMalik otp is "+str(verification_code)
        )
        otp_obj=OTPStorage(
            country_code=country_code,
            mobile=mobile_number,
            otp=verification_code,
        )
        otp_obj.save()
        print('end of try')
    except:
        return 0
    return verification_code
def verify_otp(country_code,mobile_number,verification_code):
    otp_obj=OTPStorage.objects.filter(country_code=country_code,mobile=mobile_number,is_used=False).order_by('-id').first()
    if otp_obj:
        if otp_obj.otp==verification_code:
            otp_obj.is_used=True
            otp_obj.save()
            user = User.objects.filter(country_code=country_code,mobile=mobile_number).first()
            user.is_num_verify = True
            user.save()
            return 1
        return 0
    return 0

class CountryCodeListView(APIView):
    def get(self,request,*args,**kwargs):
        logger.debug('Country code list get called')
        logger.debug(request.data)
        q = request.GET.get('q')
        if q:
            queryset=CountryCode.objects.filter(code__startswith='+'+q.strip(' ')).exclude(count_code='').distinct().order_by('country')
        
        else:
            queryset=CountryCode.objects.all().exclude(count_code='').distinct().order_by('country')
        print(queryset.count())
        serializer=CountryCodeListSerializer(queryset,many=True)
        return Response({
            'message':'Data retrieved successfully',
            'success':'True',
            'data':serializer.data,
        },status=200,)

class RegisterUserView(APIView):
    def post(self,request,*args,**kwargs):
        logger.debug('Registration view post called')
        logger.debug(request.data)
        serializer=RegisterUserSerializer(data=request.data,context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success':'True',
                'message':'Registration Successfull',
                'data':serializer.data,
            },status=200)
        # else:
        #     return Response({
        #         'success':'False',
        #         'message':'Registration Failed',
        #     },status=400)

class LoginView(APIView):
    permission_classes=[AllowAny]
    def post(self,request,*args,**kwargs):
        logger.debug('User login post called')
        logger.debug(request.data)
        data=request.data
        serializer=LoginSerializer(data=data,context={'request':request})
        if serializer.is_valid():
            data=serializer.data
            return Response({
                'success':'True',
                'message':'Data retrieved successfully',
                'data':data
            },status=200)
        # return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        return Response({
            'success':'False',
            'message': serializer.errors,
        },status=400)

        # return Response({
        #     'success':'False',
        #     'message': serializer.errors['non_field_errors'][0],
        # },status=400)

class LogoutView(APIView):
    permission_classes=[IsAuthenticated,IsTokenValid,]
    authentication_classes=[JSONWebTokenAuthentication,]
    def post(self,request,*args,**kwargs):
        token = request.META['HTTP_AUTHORIZATION']
        logger.debug('logout api called')
        logger.debug(token)
        blackobj = BlackListedToken(
            user = request.user,
            token = token,
        )
        blackobj.save()
        return Response({
            'success':'True',
            'messa':'Logged out successfully',
        },status=200)

class ForgotPasswordView(APIView):
    def post(self,request,*args,**kwargs):
        logger.debug('Change password put called')
        logger.debug(request.data)
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            newPassword = serializer.data.get("newPassword")
            confPassword = serializer.data.get("confPassword")
            country_code = serializer.data.get('country_code')
            mobile = serializer.data.get('mobile')
            user = User.objects.filter(country_code=country_code,mobile=mobile).first()
            if newPassword == confPassword:
                user.set_password(newPassword)
                user.save()
                return Response({
                            'success':"True",
                            'message':'Your password change successfully',
                        },status=200)
            return Response({'success':"False","message":"New password and confirm password should be same"},
                            status=400)
        return Response(serializer.errors, status=400)

class OTPSendView(APIView):
    def post(self,request,*args,**kwargs):
        logger.debug('Otp send post called')
        logger.debug(request.data)
        serializer = OTPSendSerializer(data=request.data)
        if serializer.is_valid():
            country_code = serializer.data['country_code']
            mobile_number = serializer.data['mobile']
            res=send_otp(country_code,mobile_number)
            data={'verification_code':res}
            print('res is = '+str(res))
            if res!=0:
                message='Successfully sent otp'
                return Response({
                	'message':message,
                	'success':'True',
                	'data':data,
                },status=200)
            else:
                message='Invalid mobile number. Unable to send otp.'
                return Response({
                	'message':message,
                	'success':'False'
                },status=400)
        else:
            return Response({
            	'message':'Serializer not valid',
            	'success':'False',
            	'data':serializer.errors
            },status=400)

class OTPVerifyAPIView(APIView):
    def post(self,request,*args,**kwargs):
        logger.debug('Otp verify post called')
        logger.debug(request.data)
        serializer = OTPVerifySerializer(data=request.data)
        if serializer.is_valid():
            country_code = serializer.data['country_code']
            mobile_number = serializer.data['mobile']
            verification_code = serializer.data['verification_code']
            res = verify_otp(country_code,mobile_number,verification_code)
            if res==1:# or verification_code=='1234':
                return Response({
                	'message':'Verification successfull',
                	'success':'True'
                },status=200)
            return Response({
            	'message':'Verification failed',
            	'success':'False'
            },status=400)
        return Response({
        	'message':'Verification failed',
        	'success':'False',
        	'data':serializer.errors,
        },status=400)

class PasswordResetEmailView(GenericAPIView):
    """
    Calls Django Auth PasswordResetForm save method.
    Accepts the following POST parameters: email
    Returns the success/fail message.
    """
    serializer_class = PasswordResetSerializer

    def post(self, request):
        logger.debug('Password reset post called')
        logger.debug(request.data)
        # Create a serializer with request.data
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Return the success message with OK HTTP status
            return Response(
                {
                'message':"Password reset e-mail has been sent successfully"
                }, 200)

        error_keys = list(serializer.errors.keys())
        if error_keys:
            error_msg = serializer.errors[error_keys[0]]
            return Response({'message': error_msg[0]}, status=400)
        return Response(serializer.errors, status=400)

class VerifyEmailView(GenericAPIView):
    def post(self,request,*args,**kwargs):
        uemail=request.data['email']
        print(uemail)
        userObj=User.objects.filter(email__iexact=uemail).first()
        print(userObj)
        if userObj:
            current_site = get_current_site(request)
            subject = 'Verify Your KishMalik Account'
            message = render_to_string('account_activation_email.html', {
                'user': userObj,
                # 'domain':'localhost:8000',
                # 'domain':'ip:8000',
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(userObj.pk)),
                'token': account_activation_token.make_token(userObj),
            })
            plain_message = strip_tags(message)
            email = EmailMultiAlternatives(
                        subject, plain_message, 'KishMalik <webmaster@localhost>', to=[uemail]
            )
            email.attach_alternative(message, "text/html")
            email.send()
            # userObj.email_user(subject, message)
            return Response({
                'message':'Activation mail sent to your email',
                'success':'True',
            },status=200,)
        return Response({
            'message':'This email is not linked with any account',
            'success':'False',
        },status=400,)

class ChangePasswordView(APIView):
    pass
class CreateProfileView(APIView):
    permission_classes=[IsAuthenticated,IsTokenValid,]
    authentication_classes=[JSONWebTokenAuthentication,]
    def get(self,request,*args,**kwargs):
        user=request.user
        serializer=UserProfileSerializer(user,context={'request':request})
        if serializer:
            return Response({
                'message':'Data retrieved successfully',
                'success':'True',
                'data':serializer.data
            },status=200)
        return Response({
            'message':'Data retrieve failed',
            'success':'False',
        },status=400)
    def post(self,request,*args,**kwargs):
        user=request.user
        serializer=CreateProfileSerializer(data=request.data,context={'request':request,'user':user})
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success':'True',
                'message':'Profile created successfully',
                'data':serializer.data,
            },status=200)
        return Response({
            'success':'False',
            'message':'Profile creation failed',
        },status=400)

class GetSkillLevelListView(APIView):
    permission_classes=[IsAuthenticated,IsTokenValid,]
    authentication_classes=[JSONWebTokenAuthentication,]
    def get(self, request, *args, **kwargs):
        queryset = SkillLevels.objects.all()
        serializer = GetSkillLevelListSerializer(queryset,many=True)
        if serializer:
            return Response({
                'success':'True',
                'message':'Data retrieved successfully',
                'data':serializer.data
            },status=200,)
        return Response({
                'success':'False',
                'message':'Failed to retrieve data',                
            },status=400,)

class UpdateSkillLevelView(APIView):
    # permission_classes=(IsTokenValid,)
    permission_classes=[IsAuthenticated,IsTokenValid,]
    authentication_classes=[JSONWebTokenAuthentication,]
    def post(self,request,*args,**kwargs):
        serializer = UpdateSkillLevelSerializer(data=request.data,context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success':'True',
                'message':'Skill level saved successfully',
            },status=200)
        return Response({
            'success':'False',
            'message':'Can not update the skill level',
        },status=400)

class BlockUnblockUser(APIView):
    def post(self,request,*args,**kwargs):
        id=self.kwargs['pk']
        u = User.objects.filter(id=id).first()
        if not u:
            return Response({
                'message':'This user does not exists',
                'success':'False',
            },status=400)
        if u.is_active:
            u.is_active=False
        else:
            u.is_active=True
        u.save()
        return Response({
            'message':'Status updated successfully',
            'success':'True',
        },status=200)

class DeleteNotificationGroup(APIView):
    def post(self, request, *args, **kwargs):
        id=self.kwargs['pk']
        notgroup = NotificationGroup.objects.filter(id=id).first()
        if not notgroup:
            return Response({
                'message':'Invalid group id',
                'success':'False'
            },status=400)
        notgroup.delete()
        return Response({
            'message':'Successfully deleted group',
            'success':'True',
        },status=200)

class ViewNotificationGroup(APIView):
    def post(self, request, *args, **kwargs):
        id = self.kwargs['pk']
        notgroup = NotificationGroup.objects.filter(id=id).first()
        if not notgroup:
            return Response({
                'message':'Invalid group id',
                'success':'False'
            },status=400)
        queryset=notgroup.users.all().order_by('-id')
        serializer=ViewNotificationGroupSerializer(queryset, many=True, context={'request':request})
        if serializer:
            return Response({
                'message':'Successfully retrieved data',
                'success':'True',
                'data':serializer.data,
            },status=200)
        return Response({
            'message':'Failed to retrieve data',
            'success':'False',
        },status=400)

class ManyUserListView(APIView):
    def get(self,request,*args, **kwargs):
        queryset = User.objects.filter(is_active=True)
        serializer = ManyUserListSerializer(queryset,many=True,context={'request':request})
        if serializer:
            return Response({
                'message':'Data retrieved successfully',
                'success':'True',
                'data':serializer.data,
            },status=200,)
        return Response({
            'message':'Data retrieve failed',
            'success':'False',
        },status=400,)

class GetRandomOnlineUserView(APIView):
    permission_classes=[IsAuthenticated,IsTokenValid,]
    authentication_classes=[JSONWebTokenAuthentication,]
    def get(self,request,*args, **kwargs):
        uidlist = User.objects.filter(is_online=1).values_list('id',flat=True)
        if len(uidlist)>0:
            randomid = random.choice(uidlist)
            randomuser = User.objects.filter(id=randomid).first()
            if randomuser:
                serializer = ManyUserListSerializer(randomuser,context={'request':request})
                return Response({
                    'message':'Data retrieved successfully',
                    'success':'True',
                    'data':serializer.data,
                },status=200,)
            return Response({
                'message':'Sorry, No random user is available',
                'success':'False',
            },status=400,)
        return Response({
            'message':'Sorry, No random user is available',
            'success':'False',
        },status=400,)



from django.db.models import Sum
import datetime
class LeaderBoardView(APIView):
    permission_classes=[IsAuthenticated,IsTokenValid,]
    authentication_classes=[JSONWebTokenAuthentication,]
    def get(self,request,*args, **kwargs):
        player=request.user
        period = self.kwargs['pk']
        queryset=''
        if period==0:
            #today
            todate=datetime.datetime.now().date()
            queryset=PlayerPoint.objects.filter(created_on=todate).values('player').annotate(sumofpoint=Sum('point')).order_by('-sumofpoint')[:10]
        elif period==1:
            #week
            todate=datetime.datetime.now().date()
            sevendaysearlierdate=(datetime.datetime.now()-datetime.timedelta(days=7)).date()
            queryset=PlayerPoint.objects.filter(created_on__range=(todate,sevendaysearlierdate)).values('player').annotate(sumofpoint=Sum('point')).order_by('-sumofpoint')[:10]
        else:
            #all
            queryset=PlayerPoint.objects.values('player').annotate(sumofpoint=Sum('point')).order_by('-sumofpoint')[:10]
        serializer = LeaderBoardSerializer(queryset,many=True,context={'request':request})
        if serializer:
            return Response({
                'message':'Successfully retrieved data',
                'success':'True',
                'data':serializer.data
            },status=200)
        return Response({
            'message':'Data retrieve failed',
            'success':'False',
        },status=400)

class ScoreboardView(APIView):
    permission_classes=[IsAuthenticated,IsTokenValid,]
    authentication_classes=[JSONWebTokenAuthentication,]
    def get(self,request,*args, **kwargs):
        player=request.user
        serializer=ScoreboardSerializer(player,context={'request':request})
        if serializer:
            return Response({
                'message':'Successfully retrieved data',
                'success':'True',
                'data':serializer.data
            },status=200)
        return Response({
            'message':'Data retrieve failed',
            'success':'False',
        },status=400)



from pyfcm import FCMNotification
class SendNotificationView(APIView):
    permission_classes=[IsAuthenticated, IsTokenValid,]
    authentication_classes=[JSONWebTokenAuthentication,]
    def post(self,request,*args,**kwargs):
        user=request.user
        print(request.data.keys())
        if 'to_userid' not in request.data.keys():
            return Response({
                'message':'Please provide to user id',
                'success':'False',
            },status=400)
        if 'notification_msg' not in request.data.keys():
            return Response({
                'message':'Please provide to notification_msg',
                'success':'False',
            },status=400)
        if 'notification_type' not in request.data.keys():
            return Response({
                'message':'Please provide to notification_type',
                'success':'False',
            },status=400)

        uid=request.data['to_userid']
        if not uid or uid=='':
            return Response({
                'message':'Please provide to user id',
                'success':'False',
            },status=400)
        
        touser=User.objects.filter(id=uid).first()
        if not touser:
            return Response({
                'message':'Invalid to user id',
                'success':'False',
            },status=400)

        notification_msg=request.data['notification_msg']
        if not notification_msg or notification_msg=='':
            return Response({
                'message':'Please provide to notification_msg',
                'success':'False',
            },status=400)

        notification_type=request.data['notification_type']
        if not notification_type or notification_type=='':
            return Response({
                'message':'Please provide to notification_type',
                'success':'False',
            },status=400)
        if notification_type not in ('4','5'):
            return Response({
                'message':'Please provide valid notification_type',
                'success':'False',
            },status=400)

        
        
        api_key=''
        if api_key!='':
            print('inside push notification')
            push_service= FCMNotification(api_key=api_key)
            registration_id=friend.device_token
            message_title="KishMalik Notification"
            message_body=notification_msg
            result=push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)

            un=UserNotification(
                user=touser,
                notification=notification_msg,
                req_type=notification_type,
                ref_id=user.id,
            )
            un.save()
            
            return Response({
                'message':'Notification sent successfully',
                'success':'True',
            },status=200)
        else:
            return Response({
                'message':'Please provide firebase api key',
                'success':'False',
            },status=400)

        