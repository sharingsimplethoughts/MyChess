from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import User
from django.db.models import Max
from accounts.models import *
from django.utils.translation import ugettext_lazy as _
from . password_reset_form_api import MyPasswordResetForm
from django.conf import settings
import string
import random
from rest_framework.exceptions import APIException

class APIException400(APIException):
    status_code = 400
# account = "ACXXXXXXXXXXXXXXXXX"
# token = "YYYYYYYYYYYYYYYYYY"

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

def id_generator(size=4, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class CountryCodeListSerializer(serializers.ModelSerializer):
    flag = serializers.SerializerMethodField()
    class Meta:
        model=CountryCode
        fields=('id','country','count_code','code','flag')
    def get_flag(self,instance):
        return 'https://www.countryflags.io/'+instance.count_code+'/flat/64.png'

class RegisterUserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(allow_blank=True)
    country_code = serializers.CharField(allow_blank=True)
    mobile = serializers.CharField(allow_blank=True)
    password = serializers.CharField(allow_blank=True)
    social_id = serializers.CharField(allow_blank=True)

    login_type = serializers.CharField(allow_blank=True)
    device_type = serializers.CharField(allow_blank=True)
    device_key = serializers.CharField(allow_blank=True)

    country = serializers.CharField(read_only=True)
    u_id = serializers.CharField(read_only=True)
    token = serializers.CharField(read_only=True)
    created_on = serializers.CharField(read_only=True)

    is_mail_verify = serializers.CharField(read_only=True)
    is_num_verify = serializers.CharField(read_only=True)
    is_profile_created = serializers.CharField(read_only=True)
    is_social_active = serializers.CharField(read_only=True)
    is_verified = serializers.CharField(read_only=True)
    profile_image = serializers.CharField(read_only=True)
    country_flag = serializers.CharField(read_only=True)
    is_subscribed = serializers.CharField(read_only=True)

    class Meta:
        model=User
        fields=('email','country','country_code','mobile','social_id','password','login_type',
                'device_type','device_key','u_id','created_on','token','is_mail_verify',
                'is_num_verify','is_profile_created','is_social_active','is_verified',
                'profile_image', 'country_flag', 'is_subscribed')

    def validate(self,data):
        email=data['email']
        country_code=data['country_code']
        mobile=data['mobile']
        social_id=data['social_id']
        password=data['password']
        login_type=data['login_type']
        device_type=data['device_type']
        device_token=data['device_key']

        if not login_type or login_type=="":
            raise APIException({
                'success':'False',
                'message':'Please provide login type',
            })
        if login_type not in ('1','2','3'):
            raise APIException({
                'success':'False',
                'message':'Please provide a valid login type',
            })

        if login_type in ('2','3'):
            if not social_id or social_id=="":
                raise APIException({
                    'success':'False',
                    'message':'Please provide social id',
                })
            user=User.objects.filter(social_id=social_id).first()
            if user:
                #--------------SOCIAL ID Already exists--------------------
                pass
            else:
                data['email'] = email if email else str(social_id)+'@temporary.com'
                data['country_code'] = country_code if country_code else '+91'
                data['mobile'] = mobile if mobile else social_id
                data['password'] = password if password else 'tem'+str(social_id)
        else:
            if not email or email=="":
                raise APIException({
                    'success':'False',
                    'message':'Please provide email',
                })
            if not country_code or country_code=="":
                raise APIException({
                    'success':'False',
                    'message':'Please provide country code',
                })
            if not mobile or mobile=="":
                raise APIException({
                    'success':'False',
                    'message':'Please provide mobile',
                })
            
            if not password or password=="":
                raise APIException({
                    'success':'False',
                    'message':'Please provide password',
                })
            if email:
                if '@' not in email:
                    raise APIException({
                        'success':'False',
                        'message':'Email id is not valid',
                    })
                else:
                    temp_email = email.split('@')[1]
                    if '.' not in temp_email:
                        raise APIException({
                            'success':'False',
                            'message':'Email id is not valid',
                        })
                user=User.objects.filter(email=email).first()
                if user:
                    raise APIException({
                        'success':'False',
                        'message':'Email id is already registered',
                    })
            if mobile:
                user=User.objects.filter(country_code=country_code,mobile=mobile).first()
                if user:
                    raise APIException({
                        'success':'False',
                        'message':'Mobile number is already registered',
                    })
            

        ##-------------COMMON VALIDATIONs---------------------------------------

        if not device_type or device_type=="":
            raise APIException({
                'success':'False',
                'message':'Please provide device type',
            })
        if device_type not in ('1','2','3'):
            raise APIException({
                'success':'False',
                'message':'Please provide a valid device type',
            })
        if not device_token or device_token=="":
            raise APIException({
                'success':'False',
                'message':'Please provide device key',
            })
        return data

    def create(self,validated_data):
        email=validated_data['email']
        country_code=validated_data['country_code']
        mobile=validated_data['mobile']
        social_id=validated_data['social_id']
        password=validated_data['password']
        login_type=validated_data['login_type']
        device_type=validated_data['device_type']
        device_token=validated_data['device_key']

        user=''
        country=''
        if social_id and login_type in ('2','3'):
            user=User.objects.filter(social_id=social_id).first()
        if country_code:
            country=CountryCode.objects.filter(code=country_code).first()
            country=country.country
        if not user or user=='':
            user=User(
                username=email,
                email=email,
                country_code=country_code,
                mobile=mobile,
                country=country,
                social_id=social_id,
                login_type=login_type,
                device_type=device_type,
                device_token=device_token,
                is_profile_created=False,
                is_social_active=True if social_id else False,
            )
            user.save()
            user.set_password(password)
            user.save()

        validated_data['u_id']=user.id
        validated_data['is_mail_verify']=user.is_mail_verify
        validated_data['is_num_verify']=user.is_num_verify
        validated_data['is_profile_created']=user.is_profile_created
        validated_data['is_social_active']=user.is_social_active
        validated_data['is_verified']=user.is_verified
        validated_data['created_on']=user.created_on
        validated_data['country']=user.country
        validated_data['is_subscribed']=user.is_subscribed
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        token = 'JWT '+token
        validated_data['token'] = token
        # validated_data['country'] = ''
        # if user.country:
        #     validated_data['country']=user.country

        validated_data['profile_image'] = ''
        if user.profile_image:
            validated_data['profile_image'] = user.profile_image.url
        cc = CountryCode.objects.filter(code=user.country_code).last()
        validated_data['country_flag'] = ''
        if cc:
            validated_data['country_flag'] = 'https://www.countryflags.io/'+cc.count_code+'/flat/64.png'

        return validated_data

class LoginSerializer(serializers.ModelSerializer):
    country_code=serializers.CharField(allow_blank=True)
    mobile=serializers.CharField(allow_blank=True)
    password=serializers.CharField(allow_blank=True)
    # social_id=serializers.CharField(allow_blank=True)

    # login_type = serializers.CharField(allow_blank=True)
    device_type = serializers.CharField(allow_blank=True)
    device_key = serializers.CharField(allow_blank=True)

    u_id = serializers.CharField(read_only=True)
    social_id = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    email = serializers.CharField(read_only=True)
    login_type = serializers.CharField(read_only=True)
    token = serializers.CharField(read_only=True)
    created_on = serializers.CharField(read_only=True)

    is_mail_verify = serializers.CharField(read_only=True)
    is_num_verify = serializers.CharField(read_only=True)
    is_profile_created = serializers.CharField(read_only=True)
    is_social_active = serializers.CharField(read_only=True)
    is_verified = serializers.CharField(read_only=True)
    profile_image = serializers.CharField(read_only=True)
    country_flag = serializers.CharField(read_only=True)
    country = serializers.CharField(read_only=True)
    is_subscribed = serializers.CharField(read_only=True)

    class Meta:
        model=User
        fields=('name','email','country_code','mobile','social_id','password','login_type',
                'device_type','device_key','u_id','created_on','token','is_mail_verify',
                'is_num_verify','is_profile_created','is_social_active','is_verified',
                'profile_image','country_flag','country','is_subscribed')

    def validate(self,data):
        country_code=data['country_code']
        mobile=data['mobile']
        password=data['password']
        # social_id=data['social_id']
        # login_type=data['login_type']
        device_type=data['device_type']
        device_token=data['device_key']

        # if not login_type or login_type=='':
        #     raise APIException400({
        #         'success':'False',
        #         'message':'Login type is required',
        #     })

        # if login_type not in ['1','2','3']:
        #     raise APIException400({
        #         'success':'False',
        #         'message':'Login type is not valid',
        #     })

        # if login_type in ['1','2']:
        #     if not social_id or social_id=='':
        #         raise APIException400({
        #             'success':'False',
        #             'message':'Social id is required',
        #         })
        #     user = User.objects.filter(social_id=social_id).first()
        #     if user:
        #         ##----RETURN EXISTING SOCIAL USER------
        #         pass
        #     else:
        #         ##------CREATE NEW SOCIAL USER-------
        #         pass

        if not country_code or country_code=='':
            raise APIException({
                'success':'False',
                'message':'Country code is required',
            })

        if not mobile or mobile=='':
            raise APIException({
                'success':'False',
                'message':'mobile is required',
            })

        if not password or password=='':
            raise APIException({
                'success':'False',
                'message':'password is required',
            })

        if not device_type or device_type=='':
            raise APIException({
                'success':'False',
                'message':'device_type is required',
            })

        if device_type not in ['1','2','3']:
            raise APIException({
                'success':'False',
                'message':'Please enter correct format of device_type',
            })

        if not device_token or device_token=='':
            raise APIException({
                'success':'False',
                'message':'Device token is required',
            })
        # password Validation
        if len(password)<8:
            raise APIException({
                'success':"false",
                'message':'Password must be at least 8 characters',
            })

        user = User.objects.filter(country_code=country_code,mobile=mobile).first()
        if user:
            if not user.check_password(password):
                raise APIException({
                    'success':'False',
                    'message':'Invalid password',
                })
        else:
            # raise serializers.ValidationError("This user is not registered with us")
            raise APIException({
                'success':'False',
                'message':'This user is not registered with us',
            })

        if not user.is_active:
            raise APIException({
                'success':'False',
                'message':'Your account has been blocked by admin',
            })

        data['u_id']=user.id
        data['social_id']=user.social_id
        data['name']=user.name
        data['email']=user.email
        data['login_type']=user.login_type
        data['created_on']=user.created_on

        data['is_mail_verify']=user.is_mail_verify
        data['is_num_verify']=user.is_num_verify
        data['is_profile_created']=user.is_profile_created
        data['is_social_active']=user.is_social_active
        data['is_verified']=user.is_verified
        data['country']=user.country
        data['is_subscribed']=user.is_subscribed

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        token = 'JWT '+token
        data['token'] = token

        data['profile_image'] = ''
        if user.profile_image:
            data['profile_image'] = user.profile_image.url
        cc = CountryCode.objects.filter(code=user.country_code).last()
        data['country_flag'] = ''
        if cc:
            data['country_flag'] = 'https://www.countryflags.io/'+cc.count_code+'/flat/64.png'

        return data

class ForgotPasswordSerializer(serializers.Serializer):
    newPassword = serializers.CharField(allow_blank=True)
    confPassword = serializers.CharField(allow_blank=True)
    country_code = serializers.CharField(allow_blank=True)
    mobile = serializers.CharField(allow_blank=True)
    def validate(self, data):
        newPassword = data['newPassword']
        confPassword = data['newPassword']
        country_code = data['country_code']
        mobile = data['mobile']

        if not newPassword or newPassword=='':
            raise APIException({
                'success':'False',
                'message':'New password is required'
            })
        if len(newPassword) < 8:
            raise APIException({
                'success':"False",
                'message':'New password must be at least 8 characters',
            })
        if not confPassword or confPassword=='':
            raise APIException({
                'success':'False',
                'message':'Confirm password is required',
            })
        if len(confPassword) < 8:
            raise APIException({
                'success':"False",
                'message':'Confirm password must be at least 8 characters',
            })
        if not country_code or country_code=="":
            raise APIException({
                'message':'Country code is required',
                'success':'False'
            })
        if not mobile or mobile=="":
            raise APIException({
                'success':'False',
                'message':'Mobile is required'
            })
        user = User.objects.filter(country_code=country_code,mobile=mobile)
        if not user:
            raise APIException({
                'success':'False',
                'message':'No user is registered with this mobile'
            })

        return data

class OTPSendSerializer(serializers.Serializer):
    country_code=serializers.CharField(allow_blank=True)
    mobile=serializers.CharField(allow_blank=True)

    def validate(self,data):
        country_code=data['country_code']
        mobile_number=data['mobile']
        if not country_code or country_code=='':
            raise APIException({
                'message':'Country code is required',
                'success':'False'
            })
        if not mobile_number or mobile_number=='':
            raise APIException({
                'message':'Mobile number is required',
                'success':'False'
            })
        user = User.objects.filter(country_code=country_code,mobile=mobile_number).first()
        if not user:
            raise APIException({
                'message':'This mobile is not registered with any account',
                'success':'False',
            })

        return data

class OTPVerifySerializer(serializers.Serializer):
	country_code=serializers.CharField(allow_blank=True)
	mobile=serializers.CharField(allow_blank=True)
	verification_code=serializers.CharField(allow_blank=True)
	# class Meta:
	# 	model = User
	# 	fields = ('country_code','mobile_number','verification_code')
	def validate(self,data):
		country_code=data['country_code']
		mobile_number=data['mobile']
		verification_code=data['verification_code']
		if not country_code or country_code=='':
			raise APIException({
				'message':'Country code is required',
				'success':'False'
			})
		if not mobile_number or mobile_number=='':
			raise APIException({
				'message':'Mobile number is required',
				'success':'False'
			})
		if not verification_code or verification_code=='':
			raise APIException({
				'message':'Verification code is required',
				'success':'False'
			})
		return data

class PasswordResetSerializer(serializers.Serializer):

	"""
	Serializer for requesting a password reset e-mail.
	"""

	email = serializers.EmailField(error_messages={'required':'email key is required', 'blank': 'email is required'})

	class Meta:
		model = User
		fields = [

			'email',
		]

	password_reset_form_class = MyPasswordResetForm

	def validate_email(self, value):
		# Create PasswordResetForm with the serializer
		self.reset_form = self.password_reset_form_class(data=self.initial_data)
		if not self.reset_form.is_valid():
			raise serializers.ValidationError(_('Error'))

		if not User.objects.filter(email=value).exists():
			raise serializers.ValidationError(_('This e-mail address is not linked with any account'))

		return value

	def save(self):
		request = self.context.get('request')
		# Set some values to trigger the send_email method.
		opts = {
			'use_https': request.is_secure(),
			'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
			'request': request,
		}
		self.reset_form.save(**opts)

class CreateProfileSerializer(serializers.Serializer):
    email = serializers.CharField(read_only=True)
    country_code = serializers.CharField(read_only=True)
    mobile = serializers.CharField(read_only=True)
    social_id = serializers.CharField(read_only=True)

    login_type = serializers.CharField(read_only=True)
    device_type = serializers.CharField(read_only=True)
    device_token = serializers.CharField(read_only=True)

    country = serializers.CharField(read_only=True)
    u_id = serializers.CharField(read_only=True)
    token = serializers.CharField(read_only=True)
    created_on = serializers.CharField(read_only=True)

    is_mail_verify = serializers.CharField(read_only=True)
    is_num_verify = serializers.CharField(read_only=True)
    is_profile_created = serializers.CharField(read_only=True)
    is_social_active = serializers.CharField(read_only=True)
    is_verified = serializers.CharField(read_only=True)
    is_subscribed = serializers.CharField(read_only=True)
    
    
    first_name = serializers.CharField(allow_blank=True,allow_null=True)
    last_name = serializers.CharField(allow_blank=True,allow_null=True)
    # country = serializers.CharField(allow_blank=True,allow_null=True)
    country_flag = serializers.CharField(read_only=True)
    profile_image = serializers.ImageField(required=False)

    class Meta:
        model=User
        # fields=('first_name','last_name','country_flag','profile_image')
        fields=('email','country_code','mobile','social_id','login_type','device_type','device_token',
                'first_name',
                'last_name',
                'country',
                'u_id',
                'created_on',
                'is_mail_verify',
                'is_num_verify',
                'is_profile_created',
                'is_social_active',
                'is_verified',
                'profile_image', 
                'country_flag','is_subscribed')

    def validate(self, data):
        first_name=data['first_name']
        last_name=data['last_name']

        if not first_name or first_name=="":
            raise APIException({
                'success':'False',
                'message':'First name is required',
            })
        if not last_name or last_name=="":
            raise APIException({
                'success':'False',
                'message':'Last name is required',
            })
        return data

    def create(self,validated_data):
        first_name=validated_data['first_name']
        last_name=validated_data['last_name']
        user = self.context['user']
        pimage = self.context['request'].FILES.get('profile_image')
        if user:
            print('hello')
            if not pimage:
                print('hello1')
                user.first_name=first_name
                user.last_name=last_name
                user.name = first_name+' '+last_name
                user.is_profile_created = True
                user.save()
            else:
                print('hello2')
                user.first_name=first_name
                user.last_name=last_name
                user.name = first_name+' '+last_name
                # user.country = country
                user.profile_image=pimage
                user.is_profile_created = True
                user.save()
            if user.profile_image:
                print('hello3')
                validated_data['profile_image']=user.profile_image
            else:
                print('hello4')
                udummy=User.objects.filter(mobile='00000000').first()
                validated_data['profile_image']=udummy.profile_image
        
        cc = CountryCode.objects.filter(code=user.country_code).last()
        validated_data['country_flag'] = ''
        if cc:
            validated_data['country_flag'] = 'https://www.countryflags.io/'+cc.count_code+'/flat/64.png'


        validated_data['email'] = user.email
        validated_data['country_code'] = user.country_code
        validated_data['mobile'] = user.mobile
        validated_data['social_id'] = user.social_id

        validated_data['login_type'] = user.login_type
        validated_data['device_type'] = user.device_type
        validated_data['device_token'] = user.device_token
        
        validated_data['u_id']=user.id
        validated_data['is_mail_verify']=user.is_mail_verify
        validated_data['is_num_verify']=user.is_num_verify
        validated_data['is_profile_created']=user.is_profile_created
        validated_data['is_social_active']=user.is_social_active
        validated_data['is_verified']=user.is_verified
        validated_data['created_on']=user.created_on
        validated_data['country']=user.country
        validated_data['is_subscribed']=user.is_subscribed
        
        return validated_data

class UpdateSkillLevelSerializer(serializers.Serializer):
    skill_id = serializers.CharField(allow_blank=True,allow_null=True)

    class Meta:
        model=SkillLevels
        fields=('skill_id')

    def validate(self,data):
        skill_id=data['skill_id']
        if not skill_id or skill_id=="":
            raise APIException({
                'success':'False',
                'message':'Please provide skill id',
            })
        skill = SkillLevels.objects.filter(id=skill_id).first()
        if not skill or skill=="":
            raise APIException({
                'success':'False',
                'message':'That skill id does not exists',
            })        
        return data
    def create(self,validated_data):
        skill_id=validated_data['skill_id']
        user=self.context['request'].user
        skill=UserSkillLevels.objects.filter(user=user).first()
        if skill:
            raise APIException({
                'success':'False',
                'message':'This user already has a skill level',
            })
        skill = SkillLevels.objects.filter(id=skill_id).first()
        uskill = UserSkillLevels(
            user=user,
            skill=skill,
        )        
        uskill.save()
        return validated_data

class GetSkillLevelListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillLevels
        fields = ['id','type']

class UserProfileSerializer(serializers.ModelSerializer):
    first_name=serializers.SerializerMethodField()
    last_name=serializers.SerializerMethodField()
    country_flag=serializers.SerializerMethodField()
    class Meta:
        model=User
        fields=('first_name','last_name','name','profile_image','country','country_flag')

    def get_first_name(self,instance):
        if instance.name:
            return instance.name.split(' ')[0]
        return ''
    def get_last_name(self,instance):
        if instance.name:
            return instance.name.split(' ')[1]
        return ''
    def get_country_flag(self,instance):
        cc = CountryCode.objects.filter(code=instance.country_code).last()
        if cc:
            return 'https://www.countryflags.io/'+cc.count_code+'/flat/64.png'
        return ''

class ViewNotificationGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','name')

class ManyUserListSerializer(serializers.ModelSerializer):
    country_flag = serializers.SerializerMethodField()
    duration = serializers.SerializerMethodField()
    profile_image = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('id','name','profile_image','country_flag','duration')
    def get_profile_image(self,instance):
        if instance.profile_image:
            return instance.profile_image.url
        return ''
    def get_country_flag(self,instance):
        cc = CountryCode.objects.filter(code=instance.country_code).last()
        if cc:
            return 'https://www.countryflags.io/'+cc.count_code+'/flat/64.png'
        return ''
    def get_duration(self,instance):
        dlist=[5,10,15,20,25,30]
        return random.choice(dlist)

class LeaderBoardSerializer(serializers.ModelSerializer):
    point = serializers.SerializerMethodField()
    player_detail = serializers.SerializerMethodField()
    class Meta:
        model = PlayerPoint
        fields = ('point','player_detail')
    def get_point(self,instance):
        return instance['sumofpoint']
    def get_player_detail(self,instance):
        id = instance['player']
        queryset = User.objects.filter(id=id).first()
        serializer = UserProfileSerializer(queryset,context={'request':self.context['request']})
        if serializer:
            return serializer.data
        return ''


from django.db.models import Q
from achievement.models import AchievementManager
from achievement.api.serializers import AchievementDetailSerializer
from game.models import Game
from lessons.models import LessonManagement
from articles.models import VideoWatchHistory
class ScoreboardSerializer(serializers.ModelSerializer):
    tmatches=0
    twins=0

    country_flag=serializers.SerializerMethodField()
    last_achivement=serializers.SerializerMethodField()
    achivements=serializers.SerializerMethodField()
    matches=serializers.SerializerMethodField()
    wins=serializers.SerializerMethodField()
    lose=serializers.SerializerMethodField()
    lessons=serializers.SerializerMethodField()
    videos=serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('name','profile_image','country_flag','last_achivement',
                'achivements','matches','wins','lose','lessons','videos')
    def get_country_flag(self,instance):
        cc = CountryCode.objects.filter(code=instance.country_code).last()
        if cc:
            return 'https://www.countryflags.io/'+cc.count_code+'/flat/64.png'
        return ''
    def get_last_achivement(self,instance):
        am=AchievementManager.objects.filter(player=instance).order_by('-created_on').first()
        serializer=AchievementDetailSerializer(am,context={'request':self.context['request']})
        if serializer:
            return serializer.data
        return ''
    def get_achivements(self,instance):
        achievements=AchievementManager.objects.filter(player=instance).count()
        return achievements
    def get_matches(self,instance):
        self.tmatches=Game.objects.filter(Q(player1=instance)|Q(player2=instance)).count()
        return self.tmatches
    def get_wins(self,instance):
        self.twins=Game.objects.filter(winner=instance).count()
        return self.twins
    def get_lose(self,instance):
        draws=Game.objects.filter(Q(player1=instance)|Q(player2=instance)&Q(winner=None)).count()
        loses=self.tmatches-(self.twins+draws)
        return loses
    def get_lessons(self,instance):
        lessons=LessonManagement.objects.filter(player=instance).count()
        return lessons
    def get_videos(self,instance):
        videos=VideoWatchHistory.objects.filter(user=instance).count()
        return videos