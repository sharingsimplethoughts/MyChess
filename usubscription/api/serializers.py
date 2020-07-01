from rest_framework import serializers
from rest_framework.exceptions import APIException
from accounts.models import *
from usubscription.models import *

class GetPlanBenifitSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanBenifits
        fields = ['benifit']

class GetPlanListSerializer(serializers.ModelSerializer):
    # benifits = serializers.SerializerMethodField()
    class Meta:
        model = SubscriptionPlan
        fields = ['id','plan_name','price_m','price_y','description']
        # fields = ['id','plan_name','price_m','price_y','benifits']

    # def get_benifits(self,instance):
    #     queryset = PlanBenifits.objects.filter(plan=instance)
    #     serializer = GetPlanBenifitSerializer(queryset,many=True)
    #     if serializer:
    #         return serializer.data
    #     else:
    #         raise APIException({
    #             'success':'False',
    #             'message':'Failed to retrieve data',
    #         })