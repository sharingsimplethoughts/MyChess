from rest_framework import serializers
from rest_framework.exceptions import APIException
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import User
import datetime
from accounts.models import *
from game.models import *
from tournament.models import *
api_key = ""

class SearchFriendListSerializer(serializers.ModelSerializer):
    id=serializers.SerializerMethodField()
    name=serializers.SerializerMethodField()
    profile_image=serializers.SerializerMethodField()
    class Meta:
        model=Friends
        fields=('id','name','profile_image','status')
    def get_id(self,instance):
        return instance.friend.id
    def get_name(self,instance):
        return instance.friend.name
    def get_profile_image(self,instance):
        url=''
        if instance.friend.profile_image:
            url=instance.friend.profile_image.url
        if not url or url=="":
            return ''
        if 'http' not in url:
            return 'baseurl'+url
        return instance.friend.profile_image.url

class SpecificUserDetailSerializer(serializers.ModelSerializer):
    country_flag = serializers.SerializerMethodField()
    request_status = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('id','name','profile_image','country_flag','request_status')

    def get_country_flag(self,instance):
        country=CountryCode.objects.filter(country=instance.country).first()
        if country:
            return 'https://www.countryflags.io/'+country.count_code+'/flat/64.png'
    def get_request_status(self,instance):
        user=self.context['request'].user
        friend=instance
        obj = Friends.objects.filter(player=user,friend=friend).first()
        if obj:
            return obj.status
        return ''

class MultipleUserDetailSerializer(serializers.ModelSerializer):
    country_flag = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('id','name','profile_image','country_flag')

    def get_country_flag(self,instance):
        country=CountryCode.objects.filter(country=instance.country).first()
        if country:
            if country.count_code=='':
                country=CountryCode.objects.filter(country=instance.country).last()
            return 'https://www.countryflags.io/'+country.count_code+'/flat/64.png'

class SubmitGameDataSerializer(serializers.ModelSerializer):
    game_id=serializers.CharField(max_length=50)
    is_winner=serializers.CharField(max_length=50)
    type=serializers.CharField(max_length=10)     #0-solo game, 1-tournament, 2-other(not implemented yet)
    tournament_id=serializers.CharField(max_length=50,required=False)
    winning_streak=serializers.CharField(max_length=100,required=False)
    point=serializers.CharField(max_length=50)
    
    class Meta:
        model=Game
        fields=('game_id','is_winner','type','tournament_id','winning_streak','point')
    
    def validate(self,data):
        game_id=data['game_id']
        is_winner=data['is_winner']
        type=data['type']
        point=data['point']
        
        if not game_id or game_id=="":
            raise APIException({
                'message':'Please provide game id',
                'success':'False',
            })
        if not is_winner or is_winner=="":
            raise APIException({
                'message':'Please provide is winner',
                'success':'False',
            })
        if not type or type=="":
            raise APIException({
                'message':'Please provide type',
                'success':'False',
            })
        g = Game.objects.filter(id=game_id).first()
        if not g:
            raise APIException({
                'message':'Please provide valid game id',
                'success':'False',
            })
        if is_winner not in ['0','1','2']:
            raise APIException({
                'message':'Is winner must be within 0 or 1 or 2',
                'success':'False',
            })
        if type not in ['0','1']:
            raise APIException({
                'message':'Type must be 0 or 1',
                'success':'False',
            })
        if type=='1':
            if 'tournament_id' not in data.keys():
                raise APIException({
                    'message':'Please provide tournament_id',
                    'success':'False',
                })
            if 'winning_streak' not in data.keys():
                raise APIException({
                    'message':'Please provide winning_streak',
                    'success':'False',
                })
            tournament_id=data['tournament_id']
            winning_streak=data['winning_streak']
            if not tournament_id or tournament_id=="":
                raise APIException({
                    'message':'Please provide tournament_id',
                    'success':'False',
                })
            if not winning_streak or winning_streak=="":
                raise APIException({
                    'message':'Please provide winning_streak',
                    'success':'False',
                })
            tourn=Tournament.objects.filter(id=tournament_id)
            if not tourn:
                raise APIException({
                    'message':'Please provide valid tournament_id',
                    'success':'False',
                })
        if not point or point=="":
            raise APIException({
                'message':'Please provide point',
                'success':'False',
            })

        return data
    def create(self,validated_data):
        game_id=validated_data['game_id']
        is_winner=validated_data['is_winner']

        type=validated_data['type']
        point=validated_data['point']
        
        ref_id=''
        winning_streak=''
        tourn=''
        if type=='1':
            ref_id=validated_data['tournament_id']
            winning_streak=validated_data['winning_streak']
            tourn=Tournament.objects.filter(id=ref_id).first()
        
        player=self.context['request'].user
        g = Game.objects.filter(id=game_id).first()
        if g:
            if is_winner=='0':
                if g.player1.id == player.id:
                    g.winner=g.player2
                else:
                    g.winner=g.player1
            elif is_winner=='1':
                g.winner=player
            else:
                g.winner=None
            g.status='5'
            if g.player1.id == player.id:
                g.player1_point=point
            else:
                g.player2_point=point
            g.save()
        if tourn:
            tgm=TournamentGameManager(
                game=g,
                tournament=tourn,
                winning_streak=winning_streak
            )
            tgm.save()
            tpm=TournamentPlayerManager.objects.filter(tournament=tourn,player=player).first()
            tpm.total_games_played=tpm.total_games_played+1
            if is_winner=='1':
                tpm.total_games_won=tpm.total_games_won+1
            elif is_winner=='0':
                tpm.total_games_lost=tpm.total_games_lost+1
            else:
                tpm.total_games_drawn=tpm.total_games_drawn+1
            
            tpm.points=tpm.points+int(point)
            tpm.save()
        
        

        #Here1 -------------------------------
        
        #today
        todate=datetime.datetime.now().date()
        q1=PlayerPoint.objects.filter(created_on=todate).values_list('player',flat=True).annotate(sumofpoint=Sum('point')).order_by('-sumofpoint')[:10]
        q1 = set(q1)
    
        #week
        todate=datetime.datetime.now().date()
        sevendaysearlierdate=(datetime.datetime.now()-datetime.timedelta(days=7)).date()
        q2=PlayerPoint.objects.filter(created_on__range=(todate,sevendaysearlierdate)).values_list('player',flat=True).annotate(sumofpoint=Sum('point')).order_by('-sumofpoint')[:10]
        q2 = set(q2)
    
        #all
        q3=PlayerPoint.objects.values_list('player',flat=True).annotate(sumofpoint=Sum('point')).order_by('-sumofpoint')[:10]
        q3 = set(q3)

        player.total_points = player.total_points+int(point)
        player.save()
        pp=PlayerPoint(
            player=player,
            point=int(point),
        )
        pp.save()

        #today
        todate=datetime.datetime.now().date()
        q4=PlayerPoint.objects.filter(created_on=todate).values_list('player',flat=True).annotate(sumofpoint=Sum('point')).order_by('-sumofpoint')[:10]
        q4 = set(q4)
    
        #week
        todate=datetime.datetime.now().date()
        sevendaysearlierdate=(datetime.datetime.now()-datetime.timedelta(days=7)).date()
        q5=PlayerPoint.objects.filter(created_on__range=(todate,sevendaysearlierdate)).values_list('player',flat=True).annotate(sumofpoint=Sum('point')).order_by('-sumofpoint')[:10]
        q5 = set(q5)
    
        #all
        q6=PlayerPoint.objects.values_list('player',flat=True).annotate(sumofpoint=Sum('point')).order_by('-sumofpoint')[:10]
        q6 = set(q6)

        l1 = list(q1-q4)
        l2 = list(q2-q5)
        l3 = list(q3-q6)
        l1.append(l2)
        l1.append(l3)
        l1 = list(set(l1))

        if l1:
            ulist = User.objects.filter(id__in=l1).values_list('device_token',flat=True)
            api_key=''
            if api_key!='':
                push_service_sp = FCMNotification(api_key=api_key)
                push_service = FCMNotification(api_key=api_key)
                registration_ids=ulist
                message_title="KishMalik Notification"
                message_body='Your rank has been changed in leaderboard'
                result=push_service.notify_multiple_devices(registration_id=registration_ids, message_title=message_title, message_body=message_body)

                us = User.objects.filter(id__in=l1)
                for s in us:
                    un=UserNotification(
                        user=s.user,
                        notification=notification_msg,
                        req_type='11',
                    )
                    un.save()

        return validated_data

class UpdatePointSerializer(serializers.ModelSerializer):
    point=serializers.CharField(max_length=10)
    
    class Meta:
        model=User
        fields=('point',) #,'type','ref_id'
    def validate(self,data):
        point=data['point']
        # type=data['type']
        if not point or point=="":
            raise APIException({
                'message':'Please provide point',
                'success':'False',
            })
        
        return data
    def create(self,validated_data):
        point=validated_data['point']

        #Here1
        #today
        todate=datetime.datetime.now().date()
        q1=PlayerPoint.objects.filter(created_on=todate).values_list('player',flat=True).annotate(sumofpoint=Sum('point')).order_by('-sumofpoint')[:10]
        q1 = set(q1)
    
        #week
        todate=datetime.datetime.now().date()
        sevendaysearlierdate=(datetime.datetime.now()-datetime.timedelta(days=7)).date()
        q2=PlayerPoint.objects.filter(created_on__range=(todate,sevendaysearlierdate)).values_list('player',flat=True).annotate(sumofpoint=Sum('point')).order_by('-sumofpoint')[:10]
        q2 = set(q2)
    
        #all
        q3=PlayerPoint.objects.values_list('player',flat=True).annotate(sumofpoint=Sum('point')).order_by('-sumofpoint')[:10]
        q3 = set(q3)

        player=self.context['request'].user
        player.total_points = player.total_points+int(point)
        player.save()
        pp=PlayerPoint(
            player=player,
            point=int(point),
        )
        pp.save()

        #today
        todate=datetime.datetime.now().date()
        q4=PlayerPoint.objects.filter(created_on=todate).values_list('player',flat=True).annotate(sumofpoint=Sum('point')).order_by('-sumofpoint')[:10]
        q4 = set(q4)
    
        #week
        todate=datetime.datetime.now().date()
        sevendaysearlierdate=(datetime.datetime.now()-datetime.timedelta(days=7)).date()
        q5=PlayerPoint.objects.filter(created_on__range=(todate,sevendaysearlierdate)).values_list('player',flat=True).annotate(sumofpoint=Sum('point')).order_by('-sumofpoint')[:10]
        q5 = set(q5)
    
        #all
        q6=PlayerPoint.objects.values_list('player',flat=True).annotate(sumofpoint=Sum('point')).order_by('-sumofpoint')[:10]
        q6 = set(q6)

        l1 = list(q1-q4)
        l2 = list(q2-q5)
        l3 = list(q3-q6)
        l1.append(l2)
        l1.append(l3)
        l1 = list(set(l1))

        if l1:
            ulist = User.objects.filter(id__in=l1).values_list('device_token',flat=True)
            api_key=''
            if api_key!='':
                push_service_sp = FCMNotification(api_key=api_key)
                push_service = FCMNotification(api_key=api_key)
                registration_ids=ulist
                message_title="KishMalik Notification"
                message_body='Your rank has been changed in leaderboard'
                result=push_service.notify_multiple_devices(registration_id=registration_ids, message_title=message_title, message_body=message_body)

                us = User.objects.filter(id__in=l1)
                for s in us:
                    un=UserNotification(
                        user=s.user,
                        notification=notification_msg,
                        req_type='11',
                    )
                    un.save()




        return validated_data


class RecentOpponentSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    profile_image = serializers.SerializerMethodField()
    result = serializers.SerializerMethodField()
    # country_flag = serializers.SerializerMethodField()

    class Meta:
        model = Game
        fields = ('id','name','profile_image','result')#'country_flag')

    def get_id(self,instance):
        request=self.context['request']
        user=request.user
        if instance.player1 == user:
            return instance.player2.id
        return instance.player1.id
    def get_name(self,instance):
        request=self.context['request']
        user=request.user
        if instance.player1 == user:
            return instance.player2.name
        return instance.player1.name
    def get_profile_image(self,instance):
        request=self.context['request']
        user=request.user
        if instance.player1 == user:
            if instance.player2.profile_image:
                return instance.player2.profile_image.url
            return ''
        if instance.player1.profile_image:
            return instance.player1.profile_image.url
        return ''
    def get_result(self,instance):
        user=self.context['request'].user
        if instance.winner == user:
            return "Won"
        return "Lost"
    # def get_country_flag(self,instance):
    #     request=self.context['request']
    #     user=request.user
    #     if instance.player1 == user:
    #         return instance.player2.id
    #     return instance.player1.profile_image

class GetGameDetailSerializer(serializers.ModelSerializer):
    created_on=serializers.SerializerMethodField()
    duration=serializers.SerializerMethodField()
    class Meta:
        model=Game
        fields=('id','game_type','player1','player2','winner','duration','room_id','created_on','status')
    def get_created_on(self,instance):
        return int(datetime.datetime.timestamp(instance.created_on))
    def get_duration(self,instance):
        return instance.duration.duration

class NotificationListSerializer(serializers.ModelSerializer):
    created_on=serializers.SerializerMethodField()
    from_detail=serializers.SerializerMethodField()
    class Meta:
        model=UserNotification
        fields=('id','notification','created_on','status','req_type','from_detail')
    def get_created_on(self,instance):
        return int(datetime.datetime.timestamp(instance.created_on))
    def get_from_detail(self,instance):
        ref_id=instance.ref_id
        serializer=''
        if instance.req_type=='1':
            user = User.objects.filter(id=ref_id).first()
            serializer = MultipleUserDetailSerializer(user,context={'request':self.context['request']})
        elif instance.req_type=='2':
            game = Game.objects.filter(id=ref_id).first()
            serializer = GetGameDetailSerializer(game,context={'request':self.context['request']})
        if serializer:
            return serializer.data
        return ''

class GameDurationListSerializer(serializers.ModelSerializer):
    duration = serializers.SerializerMethodField()
    class Meta:
        model = GameDuration
        fields = ('id','duration')

    def get_duration(self,instance):
        duration = instance.duration
        return duration