from rest_framework import generics
from .serializers import SignUpSerializer, User
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings

class SignUpApi(generics.GenericAPIView):
    serializer_class = SignUpSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = User.objects.get(email=serializer.data.get('email'))
        token = RefreshToken.for_user(user=user).access_token
        
        current_site = get_current_site(request=request).domain

        relativeLink = reverse('email-verify')

        absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
        email_body = 'Hi '+user.username+' Use link below to verify your email \n'+absurl
        data = {'email_body': email_body, 'subject':'Verify Your Email', 'to':user.email}

        Util.send_mail(data)
        return Response(data=serializer.data, status=201)


class VerifyEmail(generics.GenericAPIView):

    def get(self, request):
        token = request.query_params.get('token')
        try:
            payload = jwt.decode(token,settings.SECRET_KEY)
            user = User.objects.get(pk= payload.get('user_id'))
            user.is_active = True
            user.save()
            return Response({'detail':'Thank you for verifying the email'}, status=200)
        except jwt.ExpiredSignatureError:
            return Response({'detail':'Link is expired'}, status=400)
        except jwt.exceptions.DecodeError:
            return Response({'detail':'Token is invalid'}, status=400)

