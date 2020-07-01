from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
gender_choices=(('1','Male'),('2','Female'))
login_type_choices=(('1','Normal'),('2','Facebook'),('3','Google'))
device_type_choices=(('1','Android'),('2','Ios'),('3','Web'))


class CountryCode(models.Model):
    country=models.CharField(max_length=50,blank=True,null=True)
    count_code=models.CharField(max_length=50,blank=True,null=True,default='')
    code=models.CharField(max_length=10,blank=True,null=True)
    def __str__(self):
        return self.country

class User(AbstractUser):
    name=models.CharField(max_length=70)
    about=models.CharField(max_length=200,blank=True,null=True)
    profile_image=models.ImageField(upload_to='user/profile_image',blank=True,null=True)
    gender=models.CharField(max_length=15, choices=gender_choices,blank=True,null=True)

    country_code=models.CharField(max_length=5,blank=True,null=True)
    mobile=models.CharField(max_length=200)

    lat=models.CharField(max_length=50,blank=True,null=True)
    lon=models.CharField(max_length=50,blank=True,null=True)
    zipcode=models.CharField(max_length=50,blank=True,null=True)
    street=models.CharField(max_length=200,blank=True,null=True)
    area=models.CharField(max_length=100,blank=True,null=True)
    city=models.CharField(max_length=50,blank=True,null=True)
    country=models.CharField(max_length=50,blank=True,null=True)

    social_id=models.CharField(max_length=200,blank=True,null=True)
    login_type=models.CharField(max_length=10,choices=login_type_choices)
    device_type=models.CharField(max_length=10,choices=device_type_choices)
    device_token=models.CharField(max_length=200,blank=True,null=True)

    # level=models.ForeignKey(Level,on_delete=models.CASCADE,related_name='pl_level',blank=True,null=True)
    total_points=models.PositiveIntegerField(default=0)

    created_on=models.DateTimeField(auto_now_add=True)

    is_all_level_completed=models.BooleanField(default=False)
    is_online=models.PositiveIntegerField(default=0)  #0-offline, 1-online, 2-resume
    is_engaged = models.BooleanField(default=False)
    is_mail_verify = models.BooleanField(default=False)
    is_num_verify = models.BooleanField(default=False)
    is_profile_created = models.BooleanField(default=False)
    is_social_active = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_deleted=models.BooleanField(default=False)
    is_approved=models.BooleanField(default=False)    
    is_subscribed=models.BooleanField(default=False)
    is_guest=models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)+self.name

class OTPStorage(models.Model):
    country_code=models.CharField(max_length=10,blank=True,null=True)
    mobile=models.CharField(max_length=20,blank=True,null=True)
    otp=models.CharField(max_length=10,blank=True,null=True)
    is_used=models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

class SkillLevels(models.Model):
    type=models.CharField(max_length=50,blank=True,null=True)

    def __str__(self):
        return self.type

class UserSkillLevels(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name="uskill_user")
    total_point=models.PositiveIntegerField(default=0)
    skill=models.ForeignKey(SkillLevels, on_delete=models.CASCADE, related_name='uskill_skill')

    def __str__(self):
        return self.user.name+' '+self.skill.type

class BlackListedToken(models.Model):
    token = models.CharField(max_length=500)
    user = models.ForeignKey(User, related_name="token_user", on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("token", "user")

notification_status=(('1','active'),('2','inactive'),('3','expired'))
req_type=(
    ('1','friend request'),('2','game request'),('3','from admin'),
    ('4','new chat'),('5','new message'),('6','new article'),('7','new achievement'),
    ('8','new tournament'),('9','new rank'),('10','tournament winner'),('11','subscription')
)

# notification_status=(('1','active'),('2','inactive'),('3','expired'))
# req_type=(('1','game request'),('2','join group request'),('3','other'),('4','friend request'),('5','from admin'))
class UserNotification(models.Model):
    notification=models.CharField(max_length=500,null=True,blank=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='n_user')
    created_on=models.DateTimeField(auto_now=True)
    req_type=models.CharField(max_length=50,choices=req_type,default='1')
    ref_id=models.CharField(max_length=100,default='')
    status=models.CharField(max_length=50,choices=notification_status,default='1')
    def __str__(self):
        return self.user.name+'--'+self.notification

class NotificationGroup(models.Model):
    name=models.CharField(max_length=100,default='')
    max_users=models.PositiveIntegerField(default=2)
    users=models.ManyToManyField(User, related_name='ngusers')
    created_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class PlayerPoint(models.Model):
    player=models.ForeignKey(User,on_delete=models.CASCADE,related_name='pp_player')
    point=models.PositiveIntegerField(default=0)
    created_on=models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.id)