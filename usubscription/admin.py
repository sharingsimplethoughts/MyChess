from django.contrib import admin
from usubscription.models import *

# Register your models here.

admin.site.register(SubscriptionPlan)
admin.site.register(PlanBenifits)
admin.site.register(UserSubscription)
admin.site.register(Transaction)
admin.site.register(PaymentDetail)
