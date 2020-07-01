from django.db import models
from accounts.models import *
# Create your models here.
Period_Choices = (('1','Yearly'),('2','Monthly'))
class SubscriptionPlan(models.Model):
    plan_name = models.CharField(max_length=50,blank=True,null=True)
    # period_m = models.CharField(max_length=50, choices=Period_Choices, blank=True, null=True)
    price_m = models.CharField(max_length=50,blank=True, null=True, default='')
    # period_y = models.CharField(max_length=50, choices=Period_Choices, blank=True, null=True)
    price_y = models.CharField(max_length=50,blank=True, null=True, default='')
    description = models.CharField(max_length=1000,blank=True,null=True,default='')
    is_blocked = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    
    def __str__(self):
        return self.plan_name

class PlanBenifits(models.Model):
    plan = models.ForeignKey(SubscriptionPlan,on_delete=models.CASCADE, related_name="benifits_plan")
    benifit = models.CharField(max_length=200,blank=True,null=True)

    def __str__(self):
        return str(self.plan.id)+'--'+self.benifit

'''
on subscription renewal old subscription entry should be updated instead of creating new one
is_subscribed key in User model needs to be updated when - 
    1. subscription done for the first time(do inside api)
    2. subscription expired(use celery or middleware or trigger)
    3. subscription renewed(do inside api)
'''

class UserSubscription(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='us_user')
    sub=models.ForeignKey(SubscriptionPlan,on_delete=models.CASCADE,related_name='us_sub')
    created_on=models.DateTimeField(auto_now=True)
    exp_date=models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user.id)+'--'+str(self.sub.id)

# Payment Models------------------------------------------------------------------

payment_status_choices=(('Completed','1'),('Declined','2'),('Cancelled','3'),('Pending','4'))
payment_mode=(('Credit Card','1'),('Debit Card','2'),('Netbanking','3'),('Paypal','4'),('Terl','5'))
# TID,Date,UID,User Name,Mobile,Subscription,Payment Mode,Amount

class Transaction(models.Model):
    tid=models.CharField(max_length=300,blank=True)

class PaymentDetail(models.Model):
    transaction= models.ForeignKey(Transaction,on_delete=models.SET_NULL,related_name='sp_tran',null=True)
    player=models.ForeignKey(User,on_delete=models.SET_NULL,related_name='sp_pay',null=True)
    amount=models.DecimalField(max_digits=10,decimal_places=2,default='0.00',)
    subscription_plan=models.ForeignKey(SubscriptionPlan,on_delete=models.SET_NULL,related_name='splan_pay',null=True)
    payment_mode=models.CharField(max_length=10,choices=payment_mode)
    status=models.CharField(max_length=10,choices=payment_status_choices)
    created_on=models.DateTimeField(auto_now_add=True)
    is_deleted=models.BooleanField(default=False)

    def __str__(self):
        return str(self.transaction.tid)




#----------------------------------------------------------------------------------------------
    # def save(self,*args,**kwargs):
    #     pm1=cache.get('pm1')
    #     if pm1:
    #         cache.delete('pm1')
    #     super(PaymentDetail,self).save(*args,**kwargs)
    # def delete(self,*args,**kwargs):
    #     pm1=cache.get('pm1')
    #     if pm1:
    #         cache.delete('pm1')
    #     super(PaymentDetail,self).delete(*args,**kwargs)

# class TelrDetail(models.Model):
#     ivp_method=models.CharField(max_length=10,blank=True)
#     ivp_store=models.PositiveIntegerField()
#     ivp_authkey=models.CharField(max_length=50,blank=True)
#     ivp_cart=models.CharField(max_length=20,blank=True)
#     ivp_test=models.PositiveIntegerField()
#     ivp_amount=models.DecimalField(max_digits=10,decimal_places=2,default='0.00',)
#     ivp_currency=models.CharField(max_length=5,blank=True)
#     ivp_desc=models.CharField(max_length=100,blank=True)
#     return_auth=models.CharField(max_length=300,blank=True)
#     return_can=models.CharField(max_length=300,blank=True)
#     return_decl=models.CharField(max_length=300,blank=True)
#     ivp_trantype=models.CharField(max_length=10,blank=True)
#     bill_custref=models.PositiveIntegerField()
#     status=models.CharField(max_length=20,blank=True,default='get api got hit')
#     telr_ref=models.CharField(max_length=300,blank=True)
#     created_on=models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return str(self.bill_custref)