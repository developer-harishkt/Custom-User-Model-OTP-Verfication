from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions, status, generics
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import User, PhoneOTP
import random
from .serializers import CreateUserSerializer, LoginSerializer

from knox.views import LoginView as KnoxLoginView
from knox.auth import TokenAuthentication

from django.contrib.auth import login
# Create your views here.

class ValidatePhoneSendOTP(APIView):

    def setUrl(self, var1, var2, to):
        url = "https://2factor.in/API/R1/?module=TRANS_SMS&apikey={** API-KEY **}&to={}&from={** YOUR SENDER ID **}&templatename={** Template Name **}&var1={}&var2={}".format(var1, var2, to)
        return url

    def post(self, request, *args, **kwargs):

        phone_number = request.data.get('phone')
        if phone_number:
            phone = str(phone_number)
            user = User.objects.filter(phone__iexact = phone)
            if user.exists():
                return Response({
                    'status': False,
                    'detail': 'Phone Number Already Exists'
                })
            else:
                key = send_otp(phone)
                if key:
                    old = PhoneOTP.objects.filter(phone__iexact = phone)
                    if old.exists():
                        old = old.first()
                        count = old.count
                        if count > 1:
                            return Response({
                                'status': False,
                                'detail': 'Sending OTP Error. Limit Exceeded'
                            })

                        old.count = count + 1
                        old.save()
                        print("count increase", count)

                        url = self.setUrl(phone, "developer", key)
                        requests.get(url)

                        return Response({
                            'status': True,
                            'detail': '{} is your OTP'.format(key)
                        })
                    else:

                        PhoneOTP.objects.create(
                            phone = phone,
                            otp = key
                        )

                        url = self.setUrl("developer", key, phone)
                        requests.get(url)

                        return Response({
                            'status': True,
                            'detail': '{} is your OTP'.format(key)
                        })

                else:
                    return Response({
                        'status' : False,
                        'detail' : 'Sending otp error'
                    })

        else:
            return Response({
                'status': False,
                'detail': 'Missing paramater - phone_number'
            })



def send_otp(phone):
    if phone:
        key = random.randint(999, 9999)
        return key
    else:
        return False


class ValidateOTP(APIView):

    def post(self, request, *args, **kwards):

        phone = request.data.get('phone', False)
        otp_sent = request.data.get('otp', False)

        if phone and otp_sent:
            old = PhoneOTP.objects.filter(phone__iexact=phone)
            if old.exists():
                old = old.first()
                otp = old.otp
                if str(otp_sent) == str(otp):
                    old.validated = True
                    old.save()
                    return Response({
                        'status': True,
                        'detail': 'OTP Matched, Please Proceed For Registration'
                    })
            else:
                return Response({
                    'status': False,
                    'detail': 'Incorrect OTP, Please Try Again'
                })

        else:
            return Response({
                'status': False,
                'detail': 'Parameters Missing - Phone/OTP'
            })


class Register(APIView):

    def post(self, request, *args, **kwards):
        phone = request.data.get('phone', False)
        password = request.data.get('password', False)

        if phone and password:
            old = PhoneOTP.objects.filter(phone__iexact=phone)
            if old.exists():
                old = old.first()
                validated = old.validated

                if validated:
                    temp_data = {
                        'phone' : phone,
                        'password' : password
                    }

                    serializer = CreateUserSerializer(data = temp_data)
                    serializer.is_valid(raise_exception=True)
                    user = serializer.save()
                    old.delete()

                    return Response({
                        'status': True,
                        'detail': 'Account Registration Successful'
                    })
                else:
                    return Response({
                        'status': False,
                        'detail': 'please verify phone first'
                    })
        else:
            return Response({
                'status': False,
                'detail': 'Incorrect Parameters'
            })


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, format=None):

        serializer = LoginSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        user = serializer.validated_data['user']
        login(request, user)
        return super().post(request, format=None)
