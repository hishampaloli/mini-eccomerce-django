from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from .serializers import SignUpSerializer, UserSerializer
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

# Create your views here.


@api_view(['POST'])
def register(request):
    data = request.data

    user = SignUpSerializer(data=data)

    if user.is_valid():
        if not User.objects.filter(username=data['email']).exists():
            user = User.objects.create(
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                username=data['email'],
                password=make_password(data['password']),
            )
            return Response({'details': 'User Registered'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'details': 'User already exists'})
    else:
        return Response(user.errors)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):

    user = UserSerializer(request.user)
    return Response(user.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_me(request):

    user = request.user
    data = request.data

    user.first_name = data['first_name']
    user.last_name = data['last_name']
   

    if data['password'] != "":
        user.password = make_password(data['password'])

    user.save()
    serializer = UserSerializer(user, many = False)
    return Response(serializer.data)    




@api_view(['POST'])
def forgot_password(request):
    data = request.data
    user = get_object_or_404(User, email=data['email'])

    token = get_random_string(40)
    expire_date = datetime.now() + timedelta(minutes=30)

    user.profile.reset_password_token = token
    user.profile.reset_password_expire = expire_date

    user.profile.save()
    host = get_current_host(request)

    link = "{host}/api/reset_password/{token}".format(host=host, token=token)
    body = f'Your password reset link is: {link}'

    send_mail(
        "Password reser for ecommerce",
        body,
        "noreply@ecom.com",
        [data['email']]
    )

    return Response({'details': 'Reset link send to: {email}'.format(email=data['email'])})


@api_view(['POST'])
def reset_password(request, token):
    data = request.data

    user = get_object_or_404(User, profile__reset_password_token=token)
    if user.profile.reset_password_expire.replace(tzinfo=None) < datetime.now():
        return Response({'error': 'Token is expired'}, status=status.HTTP_400_BAD_REQUEST)

    if data['password'] != data['confirmPassword']:
        return Response({'error': 'Password not matching'}, status=status.HTTP_400_BAD_REQUEST)

    user.password = make_password(data['password'])
    user.profile.reset_password_token = ""
    user.profile.reset_password_expire = None
    user.profile.save()
    user.save()

    return Response({'details': 'Password reset successfully'}, status=status.HTTP_201_CREATED) 




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_users(request):

    users = User.objects.all()
    serializer = UserDataSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAdminUser])
def block_user(request,pk):

    user = get_object_or_404(User, id=pk)
    data = request.data
    if user:
        user.profile.isBlocked = data["isBlocked"]
        user.profile.save()
        user.save()

    serializer = UserDataSerializer(user, many=False)    
    return Response(serializer.data)    
