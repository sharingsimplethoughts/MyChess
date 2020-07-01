from rest_framework.permissions import BasePermission
from accounts.models import *
class IsTokenValid(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        is_allowed_user = True
        token = request.auth.decode("utf-8") 
        token = "JWT "+token        
        is_blackListed = BlackListedToken.objects.filter(user=user, token=token).first()
        print(is_blackListed)           
        if is_blackListed:
            is_allowed_user = False
            return is_allowed_user
            # return Response({
            #     'message':'Please login to continue',
            # })        
        is_allowed_user = True
        return is_allowed_user
