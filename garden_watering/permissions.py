from rest_framework import permissions
from rest_framework.authtoken.models import Token

class IsAuthenticatedWithToken(permissions.BasePermission):
    def has_permission(self, request, view):
        token = request.META.get('HTTP_AUTHORIZATION')
        first = False
        if not token:
            first = True
            token = request.GET.get('token')
            if not token:
                return False
        
        print(token)
        try:
            if not first:
                token = token.split(' ')[1]
            token_obj = Token.objects.get(key=token)
            request.user = token_obj.user
            return True
        except Token.DoesNotExist:
            return False

