from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import HTTP_HEADER_ENCODING, exceptions
from rest_framework.authtoken.models import Token  # Add this import

class TokenHeaderAuthentication(TokenAuthentication):
    keyword = 'Token'
    model = Token  # Assign the Token model to the model attribute

    # Rest of the class definition


    def authenticate(self, request):
        """
        Authenticate the request and return a two-tuple of (user, token).
        """
        auth = request.headers.get('Authorization')
        print(request.headers)
        if not auth:
            raise AuthenticationFailed('No Authorization header provided')

        if auth.startswith(self.keyword):
            auth = auth[len(self.keyword):].strip()

        try:
            token = self.model.objects.get(key=auth)
        except self.model.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token')

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted')

        return (token.user, token)
