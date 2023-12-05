import string

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import UserCreateSerializers
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import ConfirmCode
import random

@api_view(['POST'])
def register_api_view(request):
    serializer = UserCreateSerializers(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = request.data.get('username')
    password = request.data.get('password')
    user = User.objects.create_user(username=username, password=password, is_active=False)
    user_id = User.objects.get(username=username)
    code = ''.join(random.choice(string.digits) for i in range(6))
    code_obj = ConfirmCode.objects.create(code=code, user_id=user_id.id)
    return Response({
        'success': 'user created; confirmation required',
        'confirmation code': code_obj.code
    }, status=status.HTTP_201_CREATED
    )

@api_view(['POST'])
def activate_user_api_view(request):
    code = request.data.get('code')
    if ConfirmCode.objects.filter(code=code).exists():
        user_id = ConfirmCode.objects.get(code=code).id
        user = User.objects.get(id=user_id)
        user.is_active = True
        user.save()
        return Response({'success': 'user confirmed'})
    return Response({'error': 'invalid confirmation code'})

@api_view(['POST'])
def login_api_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
    return Response({'error': 'invalid credentials'},
                    status=status.HTTP_401_UNAUTHORIZED)