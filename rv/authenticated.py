from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import jwt
from django.conf import settings
from .models import Users

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get('Authorization')
        
        if not token:
            raise AuthenticationFailed('Authentication credentials were not provided.')
        
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')
        
        user = Users.objects.filter(id=payload['id']).first()
        if user is None:
            raise AuthenticationFailed('User not found')
        
        return (user, None)
